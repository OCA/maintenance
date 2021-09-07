# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api, fields, models

from odoo.addons.base.models import ir_ui_view


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    stage_id = fields.Many2one("maintenance.stage", readonly=True)

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super().fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu,
        )
        if view_type == "form":
            doc = etree.XML(res["arch"])
            stages = self.env["maintenance.stage"].search([], order="sequence desc")
            header = doc.xpath("//form/header")[0]
            for stage in stages:
                node = stage._get_stage_node()
                self._setup_modifiers(node)
                header.insert(0, node)
            res["arch"] = etree.tostring(doc, encoding="unicode")
        return res

    def set_maintenance_stage(self):
        if not self.env.context.get("next_stage_id"):
            return {}
        return self._set_maintenance_stage(self.env.context.get("next_stage_id"))

    def _set_maintenance_stage(self, stage_id):
        self.write({"stage_id": stage_id})

    @api.model
    def _setup_modifiers(self, node):
        modifiers = {}
        ir_ui_view.transfer_node_to_modifiers(node, modifiers)
        ir_ui_view.transfer_modifiers_to_node(modifiers, node)
