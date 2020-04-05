# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json

from lxml import etree

from odoo.tests.common import TransactionCase


class TestFlow(TransactionCase):
    def setUp(self):
        super().setUp()
        self.request = self.env["maintenance.request"].create({"name": "Request"})
        self.original_stage = self.request.stage_id
        self.last_stage = self.env["maintenance.stage"].create({"name": "Last state"})
        self.stage = self.env["maintenance.stage"].create(
            {"name": "New state", "next_stage_ids": [(4, self.last_stage.id)]}
        )
        self.original_stage.write({"next_stage_ids": [(4, self.stage.id)]})

    def test_inverse(self):
        self.assertIn(self.original_stage, self.stage.previous_stage_ids)

    def get_button(self, stage):
        data = self.request.fields_view_get(view_type="form")
        form = etree.XML(data["arch"])
        path = "//header/button[@name='set_maintenance_stage' and @id='%s']"
        button = form.xpath(path % stage.id)[0]
        self.assertTrue(etree.iselement(button))
        return button

    def test_nochange(self):
        self.request.set_maintenance_stage()
        self.assertEqual(self.original_stage, self.request.stage_id)

    def test_form(self):
        button_stage = self.get_button(self.stage)
        attr_stage = json.loads(button_stage.attrib["attrs"])
        self.assertNotIn(
            self.request,
            self.env["maintenance.request"].search(attr_stage["invisible"]),
        )
        button = self.get_button(self.last_stage)
        attr = json.loads(button.attrib["attrs"])
        self.assertIn(
            self.request, self.env["maintenance.request"].search(attr["invisible"])
        )
        getattr(
            self.request.with_context(json.loads(button_stage.attrib["context"])),
            button.attrib["name"],
        )()
        self.request.refresh()
        self.assertEqual(self.request.stage_id, self.stage)
        self.assertIn(
            self.request,
            self.env["maintenance.request"].search(attr_stage["invisible"]),
        )
        self.assertNotIn(
            self.request, self.env["maintenance.request"].search(attr["invisible"])
        )
