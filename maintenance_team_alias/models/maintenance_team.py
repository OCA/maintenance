# Copyright 2021 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class MaintenanceTeam(models.Model):
    _name = "maintenance.team"

    _inherit = ["maintenance.team", "mail.alias.mixin", "mail.alias"]
    alias_id = fields.Many2one(
        "mail.alias",
        string="Alias",
        ondelete="restrict",
        required=True,
        help="Internal email associated with this team. Incoming emails are "
        "automatically synchronized with maintenance resquests",
    )

    def get_alias_model_name(self, vals):
        return vals.get("alias_model", "maintenance.request")

    def get_alias_values(self):
        values = super(MaintenanceTeam, self).get_alias_values()
        values["alias_defaults"] = {"maintenance_team_id": self.id}
        return values

    @api.model
    def create(self, vals):
        self = self.with_context(mail_create_nosubscribe=True)
        maintenance = super(MaintenanceTeam, self).create(vals)
        return maintenance
