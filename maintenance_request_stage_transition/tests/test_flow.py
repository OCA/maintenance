# Copyright 2019 Creu Blanca
# Copyright 2026 NuoBiT Solutions - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json

from lxml import etree

from odoo.tests.common import TransactionCase
from odoo.tools.safe_eval import safe_eval


class TestFlow(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.request = cls.env["maintenance.request"].create({"name": "Request"})
        cls.original_stage = cls.request.stage_id
        cls.last_stage = cls.env["maintenance.stage"].create({"name": "Last state"})
        cls.stage = cls.env["maintenance.stage"].create(
            {"name": "New state", "next_stage_ids": [(4, cls.last_stage.id)]}
        )
        cls.original_stage.write({"next_stage_ids": [(4, cls.stage.id)]})

    def test_inverse(self):
        self.assertIn(self.original_stage, self.stage.previous_stage_ids)

    def get_button(self, stage):
        data = self.request.get_view(view_type="form")
        form = etree.XML(data["arch"])
        path = "//header/button[@name='set_maintenance_stage' and @id='%s']"
        button = form.xpath(path % stage.id)[0]
        self.assertTrue(etree.iselement(button))
        return button

    def is_button_invisible(self, button):
        return bool(
            safe_eval(
                button.attrib["invisible"], {"stage_id": self.request.stage_id.id}
            )
        )

    def test_nochange(self):
        self.request.set_maintenance_stage()
        self.assertEqual(self.original_stage, self.request.stage_id)

    def test_form(self):
        button_stage = self.get_button(self.stage)
        self.assertFalse(self.is_button_invisible(button_stage))
        button = self.get_button(self.last_stage)
        self.assertTrue(self.is_button_invisible(button))
        getattr(
            self.request.with_context(**json.loads(button_stage.attrib["context"])),
            button.attrib["name"],
        )()
        self.env.invalidate_all()
        self.assertEqual(self.request.stage_id, self.stage)
        self.assertTrue(self.is_button_invisible(button_stage))
        self.assertFalse(self.is_button_invisible(button))
