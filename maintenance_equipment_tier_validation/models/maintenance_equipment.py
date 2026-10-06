# Copyright 2026 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _name = "maintenance.equipment"
    _inherit = ["maintenance.equipment", "tier.validation"]
    _state_from = ["draft"]
    _state_to = ["confirmed"]
    _cancel_state = "cancel"

    _tier_validation_manual_config = False

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        copy=False,
        tracking=True,
    )

    def action_validate_equipment(self):
        self.write({"state": "confirmed"})

    def action_reset_to_draft(self):
        self.write({"state": "draft"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view.type != "form":
            return arch, view
        # The core maintenance equipment form has no ``header`` element, so we
        # add one on the fly rather than depending on ``base_maintenance`` just
        # to get one. If a header is already present (e.g. because
        # ``base_maintenance`` is installed), we reuse it to avoid duplicating
        # it.
        header = arch.find(".//header")
        if header is None:
            sheet = arch.find(".//sheet")
            if sheet is None:
                return arch, view
            header = etree.Element("header")
            sheet.addprevious(header)
        buttons = [
            {
                "name": "action_validate_equipment",
                "string": "Validate Equipment",
                "class": "btn-primary",
                "invisible": "state != 'draft' or "
                "validation_status in ['pending', 'rejected']",
            },
            {
                "name": "action_reset_to_draft",
                "string": "Reset to Draft",
                "invisible": "state != 'cancel'",
            },
            {
                "name": "action_cancel",
                "string": "Cancel",
                "invisible": "state == 'cancel'",
            },
        ]
        for vals in buttons:
            button = etree.SubElement(header, "button")
            button.set("type", "object")
            for attr, value in vals.items():
                button.set(attr, value)
        statusbar = etree.SubElement(header, "field")
        statusbar.set("name", "state")
        statusbar.set("widget", "statusbar")
        statusbar.set("statusbar_visible", "draft,confirmed")
        return arch, view
