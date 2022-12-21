# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0

from datetime import datetime, timedelta

from odoo import exceptions, fields
from odoo.tests import common, new_test_user, users


class TestMaintenanceTimesheetTimeControl(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ctx = {
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        maintenance_group = "maintenance.group_equipment_manager"
        timesheet_group = "hr_timesheet.group_hr_timesheet_user"
        cls.user = new_test_user(
            cls.env,
            login="test-maintenance-user",
            groups="%s,%s" % (maintenance_group, timesheet_group),
            context=ctx,
        )
        cls.employee = cls.env["hr.employee"].create(
            {"name": "Test employee", "user_id": cls.user.id}
        )
        cls.project = cls.env["project.project"].create(
            {"name": "Test project", "allow_timesheets": True}
        )
        cls.equipment = cls.env["maintenance.equipment"].create(
            {
                "name": "Test computer",
                "category_id": cls.env.ref("maintenance.equipment_computer").id,
                "project_id": cls.project.id,
                "maintenance_team_id": cls.env.ref(
                    "maintenance.equipment_team_maintenance"
                ).id,
            }
        )

    def _create_analytic_line(self, request):
        return self.env["account.analytic.line"].create(
            {
                "date_time": datetime.now() - timedelta(hours=1),
                "maintenance_request_id": request.id,
                "project_id": request.project_id.id,
                "account_id": request.project_id.analytic_account_id.id,
                "name": "Test Maintenance Request Timesheet line",
                "user_id": self.env.user.id,
            }
        )

    def _create_wizard(self, action, active_record):
        self.assertEqual(action["res_model"], "hr.timesheet.switch")
        self.assertEqual(action["target"], "new")
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["view_mode"], "form")
        return (
            active_record.env[action["res_model"]]
            .with_context(
                active_id=active_record.id,
                active_ids=active_record.ids,
                active_model=active_record._name,
                **action.get("context", {}),
            )
            .create({})
        )

    @users("test-maintenance-user")
    def test_maintenance_request_time_control_flow(self):
        request = self.env["maintenance.request"].create(
            {"name": "Test computer request", "equipment_id": self.equipment.id}
        )
        analytic_line = self._create_analytic_line(request)
        # Running line found, stop the timer
        self.assertEqual(request.show_time_control, "stop")
        request.button_end_work()
        # No more running lines, cannot stop again
        with self.assertRaises(exceptions.UserError):
            request.button_end_work()
        # All lines stopped, start new one
        self.assertEqual(request.show_time_control, "start")
        start_action = request.button_start_work()
        wizard = self._create_wizard(start_action, request)
        self.assertFalse(wizard.amount)
        self.assertLessEqual(wizard.date_time, datetime.now())
        self.assertLessEqual(wizard.date, fields.Date.context_today(wizard))
        self.assertFalse(wizard.unit_amount)
        self.assertEqual(wizard.account_id, request.project_id.analytic_account_id)
        self.assertEqual(wizard.employee_id, self.env.user.employee_id)
        self.assertEqual(wizard.name, analytic_line.name)
        self.assertEqual(wizard.project_id, request.project_id)
        self.assertEqual(wizard.maintenance_request_id, request)
        new_act = wizard.with_context(show_created_timer=True).action_switch()
        new_line = self.env[new_act["res_model"]].browse(new_act["res_id"])
        self.assertEqual(new_line.employee_id, self.env.user.employee_id)
        self.assertEqual(new_line.project_id, self.project)
        self.assertEqual(new_line.maintenance_request_id, request)
        self.assertEqual(new_line.unit_amount, 0)
        self.assertTrue(analytic_line.unit_amount)
