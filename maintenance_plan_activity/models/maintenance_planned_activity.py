# Copyright 2019-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenancePlannedActivity(models.Model):
    _name = "maintenance.planned.activity"
    _description = "Maintenance Planned Activity"

    activity_type_id = fields.Many2one(
        comodel_name="mail.activity.type",
        string="Activity Type",
        required=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        default=lambda self: self.env.user,
    )
    date_before_request = fields.Integer(
        string="# Days before request",
        help="This is the number of days the due date of the activity will be"
        "set before the Maintenance request scheduled date",
    )
    maintenance_plan_id = fields.Many2one(
        comodel_name="maintenance.plan",
        string="Maintenance Plan",
    )
