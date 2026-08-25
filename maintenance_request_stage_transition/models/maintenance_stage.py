# Copyright 2019 Creu Blanca
# Copyright 2026 NuoBiT Solutions - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json

from lxml import etree

from odoo import fields, models


class MaintenanceStage(models.Model):
    _inherit = "maintenance.stage"

    next_stage_ids = fields.Many2many(
        "maintenance.stage",
        string="Next stages",
        relation="maintenance_stage_next_stage",
        column1="stage_id",
        column2="next_stage_id",
    )
    previous_stage_ids = fields.Many2many(
        "maintenance.stage",
        string="Previous stages",
        relation="maintenance_stage_next_stage",
        column1="next_stage_id",
        column2="stage_id",
    )
    button_class = fields.Selection(
        [
            ("primary", "Primary"),
            ("info", "Info"),
            ("success", "Success"),
            ("warning", "Warning"),
            ("danger", "Danger"),
        ],
        help="For default, the system uses primary",
    )

    def _get_stage_node_invisible(self):
        return f"stage_id not in {self.previous_stage_ids.ids}"

    def _get_stage_node_name(self):
        return self.env._("To %s") % self.name

    def _get_stage_node(self):
        return etree.Element(
            "button",
            attrib={
                "name": "set_maintenance_stage",
                "id": str(self.id),
                "type": "object",
                "class": "btn-%s" % (self.button_class or "primary"),
                "context": json.dumps({"next_stage_id": self.id}),
                "invisible": self._get_stage_node_invisible(),
                "string": self._get_stage_node_name(),
            },
        )
