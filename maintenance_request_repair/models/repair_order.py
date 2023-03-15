# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class RepairOrder(models.Model):

    _inherit = "repair.order"

    maintenance_request_ids = fields.One2many(
        "maintenance.request", "repair_order_id", string="Maintenance Requests"
    )

    maintenance_request_count = fields.Integer(
        compute="_compute_maintenance_request_count", string="# Maintenances"
    )

    @api.depends("maintenance_request_ids")
    def _compute_maintenance_request_count(self):
        for repair in self:
            repair.maintenance_request_count = len(repair.maintenance_request_ids)

    def action_view_maintenance_request(self):
        """This function returns an action that display existing maintenance requests
        of given repair order ids. When only one found, show the maintenance request
        immediately.
        """
        action = self.env.ref("maintenance.hr_equipment_request_action")
        result = action.read()[0]
        # override the context to get rid of the default filtering on repair order
        result["context"] = {"default_repair_order_id": self.id}
        maintenance_request_ids = self.mapped("maintenance_request_ids")
        # choose the view_mode accordingly
        if not maintenance_request_ids or len(maintenance_request_ids) > 1:
            result["domain"] = "[('id','in',%s)]" % (maintenance_request_ids.ids)
        elif len(maintenance_request_ids) == 1:
            res = self.env.ref("maintenance.hr_equipment_request_view_form", False)
            form_view = [(res and res.id or False, "form")]
            if "views" in result:
                result["views"] = form_view + [
                    (state, view) for state, view in result["views"] if view != "form"
                ]
            else:
                result["views"] = form_view
            result["res_id"] = maintenance_request_ids.id
        return result
