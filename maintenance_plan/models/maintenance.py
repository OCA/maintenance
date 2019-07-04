# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError


class MaintenanceKind(models.Model):

    _name = 'maintenance.kind'
    _description = 'Maintenance Kind'

    name = fields.Char('Name', required=True, translate=True)
    active = fields.Boolean('Active Kind', required=True, default=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)',
         "Maintenance kind name already exists.")]


class MaintenancePlan(models.Model):

    _name = 'maintenance.plan'
    _description = 'Maintenance Plan'

    equipment_id = fields.Many2one(string='Equipment',
                                   comodel_name='maintenance.equipment',
                                   ondelete='cascade')
    maintenance_kind_id = fields.Many2one(string='Maintenance kind',
                                          comodel_name='maintenance.kind',
                                          ondelete='restrict')

    period = fields.Integer(string='Period',
                            help='Days between each maintenance')
    duration = fields.Float(string='Duration',
                            help='Maintenance duration in hours')

    next_maintenance_date = fields.Date('Next maintenance date',
                                        compute='_compute_next_maintenance')

    @api.depends('period', 'maintenance_kind_id',
                 'equipment_id.maintenance_ids.request_date',
                 'equipment_id.maintenance_ids.close_date',
                 'equipment_id.maintenance_ids.maintenance_kind_id')
    def _compute_next_maintenance(self):

        date_now = fields.Date.context_today(self)
        today_date = fields.Date.from_string(date_now)

        for plan in self.filtered(lambda x: x.period > 0):

            period_timedelta = timedelta(days=plan.period)

            next_maintenance_todo = self.env['maintenance.request'].search([
                ('equipment_id', '=', plan.equipment_id.id),
                ('maintenance_type', '=', 'preventive'),
                ('maintenance_kind_id', '=', plan.maintenance_kind_id.id),
                ('stage_id.done', '!=', True),
                ('close_date', '=', False)], order="request_date asc", limit=1)
            last_maintenance_done = self.env['maintenance.request'].search([
                ('equipment_id', '=', plan.equipment_id.id),
                ('maintenance_type', '=', 'preventive'),
                ('maintenance_kind_id', '=', plan.maintenance_kind_id.id),
                ('stage_id.done', '=', True),
                ('close_date', '!=', False)], order="close_date desc", limit=1)
            if next_maintenance_todo and last_maintenance_done:
                next_date = next_maintenance_todo.request_date
                date_gap = fields.Date.from_string(
                    next_maintenance_todo.request_date) - \
                    fields.Date.from_string(last_maintenance_done.close_date)
                # If the gap between the last_maintenance_done and the
                # next_maintenance_todo one is bigger than 2 times the period
                # and next request is in the future
                # We use 2 times the period to avoid creation too closed
                # request from a manually one created
                if date_gap > max(timedelta(0), period_timedelta * 2) \
                        and fields.Date.from_string(
                            next_maintenance_todo.request_date) > today_date:
                    # If the new date still in the past, we set it for today
                    if fields.Date.from_string(
                            last_maintenance_done.close_date) + \
                            period_timedelta < today_date:
                        next_date = date_now
                    else:
                        next_date = fields.Date.to_string(
                            fields.Date.from_string(
                                last_maintenance_done.close_date) +
                            period_timedelta)
            elif next_maintenance_todo:
                next_date = next_maintenance_todo.request_date
                date_gap = fields.Date.from_string(
                    next_maintenance_todo.request_date) - today_date
                # If next maintenance to do is in the future, and in more than
                # 2 times the period, we insert an new request
                # We use 2 times the period to avoid creation too closed
                # request from a manually one created
                if date_gap > timedelta(0) and date_gap > period_timedelta * 2:
                    next_date = fields.Date.to_string(
                        today_date + period_timedelta)
            elif last_maintenance_done:
                next_date = fields.Date.from_string(
                    last_maintenance_done.close_date) + period_timedelta
                # If when we add the period to the last maintenance done and
                # we still in past, we plan it for today
                if next_date < today_date:
                    next_date = date_now
            else:
                next_date = fields.Date.to_string(
                    today_date + period_timedelta)

            plan.next_maintenance_date = next_date

    @api.multi
    def unlink(self):
        """ Restrict deletion of maintenance plan should there be maintenance
            requests of this kind which are not done for its equipment """
        for plan in self:
            request = plan.equipment_id.mapped('maintenance_ids').filtered(
                lambda r: (
                    r.maintenance_kind_id == plan.maintenance_kind_id and
                    not r.stage_id.done and
                    r.maintenance_type == 'preventive')
            )
            if request:
                raise UserError(_('The maintenance plan %s of equipment %s '
                                  'has generated a request which is not done '
                                  'yet. You should either set the request as '
                                  'done, remove its maintenance kind or '
                                  'delete it first.') % (
                    plan.maintenance_kind_id.name, plan.equipment_id.name))
        super(MaintenancePlan, self).unlink()

    _sql_constraints = [
        ('equipment_kind_uniq', 'unique (equipment_id, maintenance_kind_id)',
         "You cannot define multiple times the same maintenance kind on an "
         "equipment maintenance plan.")]


class MaintenanceEquipment(models.Model):

    _inherit = 'maintenance.equipment'

    maintenance_plan_ids = fields.One2many(string='Maintenance plan',
                                           comodel_name='maintenance.plan',
                                           inverse_name='equipment_id')
    maintenance_team_required = fields.Boolean(
        compute='_compute_team_required')

    @api.depends('maintenance_plan_ids')
    def _compute_team_required(self):
        for equipment in self:
            equipment.maintenance_team_required = len(
                equipment.maintenance_plan_ids) >= 1

    def _prepare_request_from_plan(self, maintenance_plan):
        team = self.maintenance_team_id
        if not team:
            team = self.env['maintenance.request']._get_default_team_id()
        return {
            'name': _('Preventive Maintenance (%s) - %s') % (
                maintenance_plan.maintenance_kind_id.name, self.name),
            'request_date': maintenance_plan.next_maintenance_date,
            'schedule_date': maintenance_plan.next_maintenance_date,
            'category_id': self.category_id.id,
            'equipment_id': self.id,
            'maintenance_type': 'preventive',
            'owner_user_id': self.owner_user_id.id or self.env.user.id,
            'technician_user_id': self.technician_user_id.id,
            'maintenance_team_id': team.id,
            'maintenance_kind_id': maintenance_plan.maintenance_kind_id.id,
            'duration': maintenance_plan.duration,
        }

    def _create_new_request(self, maintenance_plan):
        self.ensure_one()
        vals = self._prepare_request_from_plan(maintenance_plan)
        self.env['maintenance.request'].create(vals)

    @api.model
    def _cron_generate_requests(self):
        """
            Generates maintenance request on the next_maintenance_date or
            today if none exists
        """
        for plan in self.env['maintenance.plan'].search([('period', '>', 0)]):
            equipment = plan.equipment_id
            next_requests = self.env['maintenance.request'].search(
                [('stage_id.done', '=', False),
                 ('equipment_id', '=', equipment.id),
                 ('maintenance_type', '=', 'preventive'),
                 ('maintenance_kind_id', '=', plan.maintenance_kind_id.id),
                 ('request_date', '=', plan.next_maintenance_date)])
            if not next_requests:
                equipment._create_new_request(plan)

    @api.depends('maintenance_plan_ids.next_maintenance_date',
                 'maintenance_ids.request_date')
    def _compute_next_maintenance(self):
        """ Redefine the function to display next_action_date in kanban view"""
        for equipment in self:
            next_plan_dates = equipment.maintenance_plan_ids.mapped(
                'next_maintenance_date')
            next_unplanned_dates = self.env['maintenance.request'].search([
                ('equipment_id', '=', equipment.id),
                ('maintenance_kind_id', '=', None),
                ('request_date', '>', fields.Date.context_today(self)),
                ('stage_id.done', '!=', True),
                ('close_date', '=', False)
            ]).mapped('request_date')
            if len(next_plan_dates + next_unplanned_dates) <= 0:
                equipment.next_action_date = None
            else:
                equipment.next_action_date = min(next_plan_dates +
                                                 next_unplanned_dates)


class MaintenanceRequest(models.Model):

    _inherit = 'maintenance.request'

    maintenance_kind_id = fields.Many2one(string='Maintenance kind',
                                          comodel_name='maintenance.kind',
                                          ondelete='restrict')
