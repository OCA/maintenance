# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests import common


class TestMaintenanceEquipmentScrap(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.Equipment = self.env["maintenance.equipment"]
        self.Category = self.env["maintenance.equipment.category"]
        self.Template = self.env["mail.template"]
        self.Wizard = self.env["wizard.perform.equipment.scrap"]

        self.template = self.env.ref(
            "maintenance_equipment_scrap.equipment_scrap_mail_template"
        )
        self.equipment1 = self.Equipment.create({"name": "Equipment 1"})
        self.equipment2 = self.Equipment.create({"name": "Equipment 2"})
        self.equipment_category = self.Category.create(
            {
                "name": "Equipment Category",
                "equipment_scrap_template_id": self.template.id,
            }
        )

    def test_01_wizard(self):
        wizard = self.Wizard.create(
            {"scrap_date": fields.Date.today(), "equipment_id": self.equipment1.id}
        )
        self.assertFalse(wizard.template_id)
        wizard.do_scrap()
        self.assertEqual(self.equipment1.scrap_date, wizard.scrap_date)

        action = self.equipment2.action_perform_scrap()
        action2 = self.env["ir.actions.act_window"]._for_xml_id(
            "maintenance_equipment_scrap.wizard_perform_equipment_scrap_action"
        )
        self.assertEqual(action, action2)

    def test_02_no_email_template(self):
        mail_ids = self.env["mail.mail"].search([])
        wizard = self.Wizard.create(
            {"scrap_date": fields.Date.today(), "equipment_id": self.equipment2.id}
        )
        # No template set if equipment has no category
        self.assertFalse(wizard.template_id)
        wizard.do_scrap()
        mail_id = self.env["mail.mail"].search([]) - mail_ids
        self.assertFalse(mail_id, "No mail should be created if no template is used")

    def test_03_email_template_manually_set(self):
        mail_ids = self.env["mail.mail"].search([])
        wizard = self.Wizard.create(
            {"scrap_date": fields.Date.today(), "equipment_id": self.equipment2.id}
        )
        # No template set if equipment has no category
        self.assertFalse(wizard.template_id)
        wizard.template_id = self.template
        wizard.do_scrap()
        mail_id = self.env["mail.mail"].search([]) - mail_ids
        self.assertEqual(len(mail_id), 1, "One mail should be created")
        self.assertRegex(
            mail_id.subject, f"Your equipment {self.equipment2.name} was scrapped"
        )

    def test_04_email_template_from_category(self):
        mail_ids = self.env["mail.mail"].search([])
        self.equipment2.category_id = self.equipment_category
        wizard = self.Wizard.create(
            {"scrap_date": fields.Date.today(), "equipment_id": self.equipment2.id}
        )
        # Template was set from category
        self.assertEqual(wizard.template_id, self.template)
        wizard.do_scrap()
        mail_id = self.env["mail.mail"].search([]) - mail_ids
        self.assertEqual(len(mail_id), 1, "One mail should be created")
        self.assertRegex(
            mail_id.subject, f"Your equipment {self.equipment2.name} was scrapped"
        )

    def test_05_wizard_default_values(self):
        # equipment without category => no template
        wizard = self.Wizard.with_context(
            default_equipment_id=self.equipment2.id
        ).create({})
        self.assertEqual(wizard.equipment_id, self.equipment2)
        self.assertEqual(wizard.scrap_date, fields.Date.today())
        self.assertFalse(wizard.template_id)
        # equipment with category => template from category
        self.equipment2.category_id = self.equipment_category
        wizard = self.Wizard.with_context(
            default_equipment_id=self.equipment2.id
        ).create({})
        self.assertEqual(wizard.equipment_id, self.equipment2)
        self.assertEqual(wizard.scrap_date, fields.Date.today())
        self.assertEqual(wizard.template_id, self.template)

    def test_06_copy_equipment(self):
        self.equipment1.scrap_date = fields.Date.today()
        equipment_copy = self.equipment1.copy()
        self.assertFalse(equipment_copy.scrap_date, "Scrap date should be cleared")
