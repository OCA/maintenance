# Copyright 2017 Camptocamp SA
# Copyright 2019-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .maintenance_plan import get_relativedelta


class MaintenanceEquipment(models.Model):

    _inherit = "maintenance.equipment"

    maintenance_plan_ids = fields.One2many(
        string="Maintenance plan",
        comodel_name="maintenance.plan",
        inverse_name="equipment_id",
    )
    maintenance_plan_count = fields.Integer(
        compute="_compute_maintenance_plan_count",
        string="Maintenance Plan Count",
        store=True,
    )
    maintenance_team_required = fields.Boolean(compute="_compute_team_required")
    notes = fields.Text(string="Notes")

    @api.depends("maintenance_plan_ids", "maintenance_plan_ids.active")
    def _compute_maintenance_plan_count(self):
        for equipment in self:
            equipment.maintenance_plan_count = len(
                equipment.with_context(active_test=False).maintenance_plan_ids
            )

    @api.depends("maintenance_plan_ids")
    def _compute_team_required(self):
        for equipment in self:
            equipment.maintenance_team_required = (
                len(
                    equipment.maintenance_plan_ids.filtered(
                        lambda r: not r.maintenance_team_id
                    )
                )
                >= 1
            )

    @api.constrains("company_id", "maintenance_plan_ids")
    def _check_company_id(self):
        for rec in self:
            if rec.company_id and not all(
                rec.company_id == p.company_id for p in rec.maintenance_plan_ids
            ):
                raise ValidationError(
                    _(
                        "Some maintenance plan's company is incompatible with "
                        "the company of this equipment."
                    )
                )

    def _prepare_request_from_plan(self, maintenance_plan, next_maintenance_date):
        team = maintenance_plan.maintenance_team_id.id or self.maintenance_team_id.id
        if not team:
            team = self.env["maintenance.request"]._get_default_team_id()

        description = self.name if self else maintenance_plan.name
        kind = maintenance_plan.maintenance_kind_id.name or _("Unspecified kind")
        name = _("Preventive Maintenance (%s) - %s") % (kind, description)

        return {
            "name": name,
            "request_date": next_maintenance_date,
            "schedule_date": next_maintenance_date,
            "category_id": self.category_id.id,
            "equipment_id": self.id,
            "maintenance_type": "preventive",
            "owner_user_id": self.owner_user_id.id or self.env.user.id,
            "user_id": self.technician_user_id.id,
            "maintenance_team_id": team,
            "maintenance_kind_id": maintenance_plan.maintenance_kind_id.id,
            "maintenance_plan_id": maintenance_plan.id,
            "duration": maintenance_plan.duration,
            "note": maintenance_plan.note,
            "company_id": maintenance_plan.company_id.id or self.company_id.id,
        }

    def _create_new_request(self, maintenance_plan):
        # Compute horizon date adding to today the planning horizon
        horizon_date = fields.Date.from_string(fields.Date.today()) + get_relativedelta(
            maintenance_plan.maintenance_plan_horizon, maintenance_plan.planning_step
        )
        # We check maintenance request already created and create until
        # planning horizon is met
        furthest_maintenance_todo = self.env["maintenance.request"].search(
            [("maintenance_plan_id", "=", maintenance_plan.id)],
            order="request_date desc",
            limit=1,
        )
        if furthest_maintenance_todo:
            next_maintenance_date = fields.Date.from_string(
                furthest_maintenance_todo.request_date
            ) + get_relativedelta(
                maintenance_plan.interval, maintenance_plan.interval_step
            )
        else:
            next_maintenance_date = fields.Date.from_string(
                maintenance_plan.next_maintenance_date
            )
        requests = self.env["maintenance.request"]
        # Create maintenance request until we reach planning horizon
        while next_maintenance_date <= horizon_date:
            if next_maintenance_date >= fields.Date.from_string(fields.Date.today()):
                vals = self._prepare_request_from_plan(
                    maintenance_plan, next_maintenance_date
                )
                requests |= self.env["maintenance.request"].create(vals)
            next_maintenance_date = next_maintenance_date + get_relativedelta(
                maintenance_plan.interval, maintenance_plan.interval_step
            )
        return requests

    @api.model
    def _cron_generate_requests(self):
        """
            Generates maintenance request on the next_maintenance_date or
            today if none exists
        """
        for plan in self.env["maintenance.plan"].search([("interval", ">", 0)]):
            equipment = plan.equipment_id
            equipment._create_new_request(plan)

    @api.depends(
        "maintenance_plan_ids.next_maintenance_date", "maintenance_ids.request_date"
    )
    def _compute_next_maintenance(self):
        """ Redefine the function to display next_action_date in kanban view"""
        for equipment in self:
            next_plan_dates = equipment.maintenance_plan_ids.mapped(
                "next_maintenance_date"
            )
            next_unplanned_dates = (
                self.env["maintenance.request"]
                .search(
                    [
                        ("equipment_id", "=", equipment.id),
                        ("maintenance_kind_id", "=", None),
                        ("request_date", ">", fields.Date.context_today(self)),
                        ("stage_id.done", "!=", True),
                        ("close_date", "=", False),
                    ]
                )
                .mapped("request_date")
            )
            if len(next_plan_dates + next_unplanned_dates) <= 0:
                equipment.next_action_date = None
            else:
                equipment.next_action_date = min(next_plan_dates + next_unplanned_dates)
