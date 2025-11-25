# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import new_test_user

from odoo.addons.base.tests.common import BaseCommon


class TestMaintenanceSecurity(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.hr_user = new_test_user(
            cls.env,
            login="test-maintenance-user",
            groups="hr.group_hr_user",
        )

    def test_hr_user_no_maintenance_manager_group(self):
        self.assertNotIn(
            self.env.ref("maintenance.group_equipment_manager"), self.hr_user.groups_id
        )
