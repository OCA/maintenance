# Copyright 2022-2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MaintenanceEquipmentUsage(models.Model):
    _name = "maintenance.equipment.usage"
    _description = "Maintenance Equipment Usage"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name desc"

    name = fields.Char(
        string="Equipment Usage", copy=False, readonly=True, default=lambda x: _("New")
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)], "reserved": [("readonly", False)]},
        tracking=True,
    )
    picking_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Picked up by",
        readonly=True,
        states={"draft": [("readonly", False)], "reserved": [("readonly", False)]},
        tracking=True,
    )
    return_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Returned by",
        states={
            "in_use": [("required", True)],
            "returned": [("readonly", True)],
            "cancel": [("readonly", True)],
        },
        tracking=True,
    )
    date_picking = fields.Datetime(
        string="Picking Date",
        copy=False,
        index=True,
        readonly=True,
        states={"draft": [("readonly", False)], "reserved": [("readonly", False)]},
        tracking=True,
    )
    date_return = fields.Datetime(
        string="Return Date",
        copy=False,
        index=True,
        states={"returned": [("readonly", True)], "cancel": [("readonly", True)]},
        tracking=True,
    )
    equipment_id = fields.Many2one(
        comodel_name="maintenance.equipment",
        string="Equipment",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)], "reserved": [("readonly", False)]},
        tracking=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Location",
        readonly=True,
        states={"draft": [("readonly", False)], "reserved": [("readonly", False)]},
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "New"),
            ("reserved", "Reserved"),
            ("in_use", "In Use"),
            ("returned", "Returned"),
            ("cancel", "Cancelled"),
        ],
        readonly=True,
        copy=False,
        default="draft",
        tracking=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        index=True,
        default=lambda self: self.env.company.id,
        readonly=True,
        states={"draft": [("readonly", False)], "reserved": [("readonly", False)]},
        tracking=True,
    )
    notes = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals["name"] == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "maintenance.equipment.usage"
                ) or _("New")
        return super().create(vals_list)

    def action_pick(self):
        to_pick = self.filtered(lambda x: x.state in ("draft", "reserved"))
        to_pick_with_date = to_pick.filtered(lambda x: not x.date_picking)
        to_pick_with_date.date_picking = fields.Datetime.now()
        to_pick.state = "in_use"
        return True

    def action_return(self):
        to_return = self.filtered(lambda x: x.state == "in_use")
        to_return_with_date = to_return.filtered(lambda x: not x.date_return)
        to_return_with_date.date_return = fields.Datetime.now()
        to_return.state = "returned"
        return True

    def action_cancel(self):
        to_cancel = self.filtered(lambda x: x.state not in ("returned", "cancel"))
        to_cancel.state = "cancel"
        return True

    @api.onchange("user_id")
    def _onchange_user_id(self):
        for usage in self:
            usage.picking_user_id = usage.user_id
            usage.return_user_id = usage.user_id

    @api.constrains("state")
    def _constrains_state(self):
        """Allow only one usage in use per equipment"""
        for equipment in self.mapped("equipment_id"):
            items = equipment.usage_ids.filtered(lambda x: x.state == "in_use")
            if len(items) > 1:
                raise UserError(
                    _("Every equipment can only be picked once at the same time!")
                )
