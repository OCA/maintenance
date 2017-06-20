# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests import common


class TestMaintenanceEquipmentScrap(common.TransactionCase):

    def setUp(self):
        super(TestMaintenanceEquipmentScrap, self).setUp()
        self.Equipment = self.env['maintenance.equipment']
        self.Category = self.env['maintenance.equipment.category']
        self.Template = self.env['mail.template']
        self.Wizard = self.env['wizard.perform.equipment.scrap']

        self.template = self.env.ref(
            'maintenance_equipment_scrap.equipment_scrap_mail_template'
        )

        self.equipment1 = self.Equipment.create({
            'name': 'Equipment 1',
            'equipment_scrap_template_id': self.template.id,
        })

        self.equipment2 = self.Equipment.create({
            'name': 'Equipment 2',
        })

        self.equipment_category = self.Category.create({
            'name': 'Equipment Category',
            'equipment_scrap_template_id': self.template.id,
        })

    def test_01_wizard(self):
        wizard = self.Wizard.create({
            'scrap_date': fields.Date.today(),
            'equipment_id': self.equipment1.id,
        })
        wizard.do_scrap()
        self.assertEqual(self.equipment1.scrap_date, wizard.scrap_date)

        action = self.equipment2.action_perform_scrap()
        action2 = self.env.ref(
            'maintenance_equipment_scrap.wizard_perform_equipment_scrap_action'
        ).read()[0]
        self.assertEqual(action, action2)

    def test_02_onchange(self):
        self.assertFalse(self.equipment2.equipment_scrap_template_id)

        self.equipment2.category_id = self.equipment_category
        self.equipment2.onchange_category_id()
        self.assertEqual(
            self.equipment2.equipment_scrap_template_id,
            self.template
        )

        self.equipment2.category_id = None
        self.equipment2.onchange_category_id()
        self.assertFalse(self.equipment2.equipment_scrap_template_id)
