# Copyright 2017 Camptocamp SA
# Copyright 2019-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


def get_relativedelta(interval, step):
    if step == "day":
        return relativedelta(days=interval)
    elif step == "week":
        return relativedelta(weeks=interval)
    elif step == "month":
        return relativedelta(months=interval)
    elif step == "year":
        return relativedelta(years=interval)


class MaintenancePlan(models.Model):
    _name = "maintenance.plan"
    _description = "Maintenance Plan"

    name = fields.Char("Description")
    active = fields.Boolean(default=True)
    equipment_id = fields.Many2one(
        string="Equipment", comodel_name="maintenance.equipment", ondelete="cascade"
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.company,
    )
    maintenance_kind_id = fields.Many2one(
        string="Maintenance Kind", comodel_name="maintenance.kind", ondelete="restrict"
    )
    interval = fields.Integer(
        string="Frequency", default=1, help="Interval between each maintenance"
    )
    interval_step = fields.Selection(
        [
            ("day", "Day(s)"),
            ("week", "Week(s)"),
            ("month", "Month(s)"),
            ("year", "Year(s)"),
        ],
        string="Recurrence",
        default="year",
        help="Let the event automatically repeat at that interval step",
    )
    duration = fields.Float(
        string="Duration (hours)", help="Maintenance duration in hours"
    )
    start_maintenance_date = fields.Date(
        string="Start maintenance date",
        default=fields.Date.context_today,
        help="Date from which the maintenance will we active",
    )
    next_maintenance_date = fields.Date(
        "Next maintenance date", compute="_compute_next_maintenance", store=True
    )
    maintenance_plan_horizon = fields.Integer(
        string="Planning Horizon period",
        default=1,
        help="Maintenance planning horizon. Only the maintenance requests "
        "inside the horizon will be created.",
    )
    planning_step = fields.Selection(
        [
            ("day", "Day(s)"),
            ("week", "Week(s)"),
            ("month", "Month(s)"),
            ("year", "Year(s)"),
        ],
        string="Planning Horizon step",
        default="year",
        help="Let the event automatically repeat at that interval",
    )
    note = fields.Html("Note")
    maintenance_ids = fields.One2many(
        "maintenance.request", "maintenance_plan_id", string="Maintenance requests"
    )
    maintenance_count = fields.Integer(
        compute="_compute_maintenance_count", string="Maintenance", store=True
    )
    maintenance_open_count = fields.Integer(
        compute="_compute_maintenance_count", string="Current Maintenance", store=True
    )
    maintenance_team_id = fields.Many2one("maintenance.team")

    def name_get(self):
        result = []
        for plan in self:
            result.append(
                (
                    plan.id,
                    plan.name
                    or _("Unnamed %s plan (%s)")
                    % (plan.maintenance_kind_id.name or "", plan.equipment_id.name),
                )
            )
        return result

    @api.depends("maintenance_ids.stage_id.done")
    def _compute_maintenance_count(self):
        for equipment in self:
            equipment.maintenance_count = len(equipment.maintenance_ids)
            equipment.maintenance_open_count = len(
                equipment.maintenance_ids.filtered(lambda x: not x.stage_id.done)
            )

    @api.depends(
        "interval",
        "interval_step",
        "maintenance_kind_id",
        "equipment_id.maintenance_ids.request_date",
        "equipment_id.maintenance_ids.close_date",
        "equipment_id.maintenance_ids.maintenance_kind_id",
    )
    def _compute_next_maintenance(self):

        for plan in self.filtered(lambda x: x.interval > 0):

            interval_timedelta = get_relativedelta(plan.interval, plan.interval_step)

            next_maintenance_todo = self.env["maintenance.request"].search(
                [
                    ("equipment_id", "=", plan.equipment_id.id),
                    ("maintenance_type", "=", "preventive"),
                    ("maintenance_kind_id", "=", plan.maintenance_kind_id.id),
                    ("maintenance_plan_id", "=", plan.id),
                    ("stage_id.done", "!=", True),
                    ("close_date", "=", False),
                ],
                order="request_date asc",
                limit=1,
            )

            if next_maintenance_todo:
                plan.next_maintenance_date = next_maintenance_todo.request_date
            else:
                next_date = plan.start_maintenance_date
                while next_date < fields.Date.today():
                    next_date = next_date + interval_timedelta
                plan.next_maintenance_date = next_date

    @api.constrains("company_id", "equipment_id")
    def _check_company_id(self):
        for rec in self:
            if (
                rec.equipment_id.company_id
                and rec.company_id != rec.equipment_id.company_id
            ):
                raise ValidationError(
                    _("Maintenace Equipment must belong to the equipment's company")
                )

    def unlink(self):
        """Restrict deletion of maintenance plan should there be maintenance
        requests of this kind which are not done for its equipment"""
        for plan in self:
            request = plan.equipment_id.mapped("maintenance_ids").filtered(
                lambda r: (
                    r.maintenance_kind_id == plan.maintenance_kind_id
                    and not r.stage_id.done
                    and r.maintenance_type == "preventive"
                )
            )
            if request:
                raise UserError(
                    _(
                        "The maintenance plan %s of equipment %s "
                        "has generated a request which is not done "
                        "yet. You should either set the request as "
                        "done, remove its maintenance kind or "
                        "delete it first."
                    )
                    % (plan.maintenance_kind_id.name, plan.equipment_id.name)
                )
        super().unlink()

    _sql_constraints = [
        (
            "equipment_kind_uniq",
            "unique (equipment_id, maintenance_kind_id)",
            "You cannot define multiple times the same maintenance kind on an "
            "equipment maintenance plan.",
        )
    ]
