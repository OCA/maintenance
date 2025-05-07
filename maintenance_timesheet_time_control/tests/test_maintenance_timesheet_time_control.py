# Copyright 2022-2024 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0

from odoo import exceptions, fields
from odoo.tests.common import users

from odoo.addons.project_timesheet_time_control.tests import (
    test_project_timesheet_time_control,
)


class TestMaintenanceTimesheetTimeControl(
    test_project_timesheet_time_control.TestProjectTimesheetTimeControlBase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user.groups_id |= cls.env.ref("maintenance.group_equipment_manager")
        cls.category = cls.env["maintenance.equipment.category"].create(
            {"name": "Test category"}
        )
        cls.team = cls.env["maintenance.team"].create({"name": "Test team"})
        cls.equipment = cls.env["maintenance.equipment"].create(
            {
                "name": "Test computer",
                "category_id": cls.category.id,
                "project_id": cls.project.id,
                "maintenance_team_id": cls.team.id,
            }
        )
        cls.request = cls.env["maintenance.request"].create(
            {"name": "Test computer request", "equipment_id": cls.equipment.id}
        )
        cls.line.maintenance_request_id = cls.request

    @users("test-user")
    def test_maintenance_request_time_control_flow(self):
        # Running line found, stop the timer
        self.line.button_end_work()
        with self.assertRaises(exceptions.UserError):
            self.request.button_end_work()
        # All lines stopped, start new one
        self.assertEqual(self.request.show_time_control, "start")
        start_action = self.request.button_start_work()
        wizard = self._create_wizard(start_action, self.line)
        self.assertLessEqual(wizard.date_time, fields.Datetime.now())
        self.assertEqual(wizard.name, self.line.name)
        self.assertEqual(wizard.project_id, self.request.project_id)
        self.assertEqual(
            wizard.analytic_line_id.account_id, self.request.project_id.account_id
        )
        self.assertEqual(wizard.analytic_line_id, self.line)
        new_act = wizard.with_context(show_created_timer=True).action_switch()
        new_line = self.env[new_act["res_model"]].browse(new_act["res_id"])
        self.assertEqual(new_line.employee_id, self.env.user.employee_id)
        self.assertEqual(new_line.project_id, self.project)
        self.assertEqual(new_line.maintenance_request_id, self.request)
        self.assertEqual(new_line.unit_amount, 0)
        self.assertTrue(self.line.unit_amount)
