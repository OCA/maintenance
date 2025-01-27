# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import _, fields
from odoo.exceptions import UserError, ValidationError

from .common import TestMaintenancePlanBase


class TestMaintenancePlan(TestMaintenancePlanBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.today_date = fields.Date.from_string("2023-01-25")

    def test_name_get(self):
        self.assertEqual(
            self.maintenance_plan_1.name_get()[0][1],
            _(
                "Unnamed %(void)s plan (%(eqpmnt)s)",
                void="",
                eqpmnt=self.maintenance_plan_1.equipment_id.name,
            ),
        )
        self.assertEqual(
            self.maintenance_plan_2.name_get()[0][1],
            _(
                "Unnamed %(kind)s plan (%(eqpmnt)s)",
                kind=self.maintenance_plan_2.maintenance_kind_id.name,
                eqpmnt=self.maintenance_plan_2.equipment_id.name,
            ),
        )
        self.assertEqual(
            self.maintenance_plan_3.name_get()[0][1], self.maintenance_plan_3.name
        )

    def test_next_maintenance_date_01(self):
        # We set start maintenance date tomorrow and check next maintenance
        # date has been correctly computed
        self.maintenance_plan_1.start_maintenance_date = "2023-01-24"
        # Check next maintenance date is 1 month from start date
        self.assertEqual(
            self.maintenance_plan_1.next_maintenance_date,
            fields.Date.from_string("2023-02-24"),
        )

    def test_next_maintenance_date_02(self):
        self.cron.method_direct_trigger()
        # Check maintenance plan dates
        self.assertEqual(
            self.maintenance_plan_1.start_maintenance_date, self.today_date
        )
        self.assertEqual(self.maintenance_plan_1.next_maintenance_date, self.today_date)
        # Check information from generated_requests
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )
        self.assertEqual(len(generated_requests), 3)
        maintenance_1 = generated_requests[0]
        # First maintenance was planned 2023-01-25
        self.assertEqual(maintenance_1.request_date, self.today_date)
        # Complete request:
        maintenance_1.stage_id = self.done_stage
        # Check next one:
        maintenance_2 = generated_requests[1]
        # This should be expected 2023-02-25
        self.assertEqual(
            maintenance_2.request_date, fields.Date.from_string("2023-02-25")
        )
        # Complete request and Check next one:
        maintenance_2.stage_id = self.done_stage
        maintenance_3 = generated_requests[2]
        # This one should be expected 2023-03-25
        self.assertEqual(
            maintenance_3.request_date, fields.Date.from_string("2023-03-25")
        )
        # Move it to a date before `start_maintenance_date` (the request should
        # be ignored)
        past_date = fields.Date.from_string("2022-12-25")
        maintenance_3.request_date = past_date
        self.assertNotEqual(self.maintenance_plan_1.next_maintenance_date, past_date)
        self.assertEqual(
            self.maintenance_plan_1.next_maintenance_date,
            fields.Date.from_string("2023-03-25"),
        )
        # Move the request_date far into the future:
        future_date = fields.Date.from_string("2023-05-25")
        maintenance_3.request_date = future_date
        self.assertEqual(self.maintenance_plan_1.next_maintenance_date, future_date)
        # Complete request in that date, next expected date should be 1 month
        # after latest request done.:
        maintenance_3.stage_id = self.done_stage
        self.assertEqual(
            self.maintenance_plan_1.next_maintenance_date,
            fields.Date.from_string("2023-06-25"),
        )

    def test_generate_requests(self):
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )
        self.assertEqual(len(generated_requests), 3)
        self.assertEqual(
            fields.Date.to_date(generated_requests[0].schedule_date), self.today_date
        )
        self.assertEqual(
            fields.Date.to_date(generated_requests[1].schedule_date),
            fields.Date.from_string("2023-02-25"),
        )
        self.assertEqual(
            fields.Date.to_date(generated_requests[2].schedule_date),
            fields.Date.from_string("2023-03-25"),
        )
        generated_request = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_4.id)], limit=1
        )
        self.assertEqual(
            generated_request.name,
            _(
                "Preventive Maintenance (%(kind)s) - %(plan)s",
                kind=self.weekly_kind.name,
                plan=self.maintenance_plan_4.name,
            ),
        )

    def test_generate_requests2(self):
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )

        self.assertEqual(len(generated_requests), 3)
        # We set plan start_maintenanca_date to a future one. New requests should take
        # into account this new date.
        new_date = fields.Date.from_string("2023-04-25")
        self.maintenance_plan_1.next_maintenance_date = new_date
        self.maintenance_plan_1.maintenance_plan_horizon = 3
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )
        self.assertEqual(len(generated_requests), 4)
        self.assertEqual(generated_requests[-1].request_date, new_date)

    def test_generate_requests_no_equipment(self):
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_5.id)],
            order="schedule_date asc",
        )

        self.assertEqual(len(generated_requests), 3)

        # We set plan start_maintenanca_date to a future one. New requests should take
        # into account this new date.

        self.maintenance_plan_5.write(
            {
                "start_maintenance_date": fields.Date.to_string(
                    self.today_date + relativedelta(weeks=9)
                ),
                "maintenance_plan_horizon": 3,
            }
        )

        self.cron.method_direct_trigger()

        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_5.id)],
            order="schedule_date asc",
        )

        self.assertEqual(len(generated_requests), 4)
        self.assertEqual(
            generated_requests[-1].request_date,
            self.today_date + relativedelta(weeks=9),
        )
        self.assertFalse(generated_requests.mapped("equipment_id"))

    def test_get_relativedelta(self):
        plan = self.maintenance_plan_1
        result = plan.get_relativedelta(1, "day")
        self.assertEqual(relativedelta(days=1), result)
        result = plan.get_relativedelta(1, "week")
        self.assertEqual(relativedelta(weeks=1), result)
        result = plan.get_relativedelta(1, "month")
        self.assertEqual(relativedelta(months=1), result)
        result = plan.get_relativedelta(1, "year")
        self.assertEqual(relativedelta(years=1), result)

    def test_generate_requests_inactive_equipment(self):
        self.equipment_1.active = False
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )
        self.assertEqual(len(generated_requests), 0)
        self.equipment_1.active = True
        self.cron.method_direct_trigger()
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
        )
        self.assertEqual(len(generated_requests), 3)

    def test_maintenance_request_report(self):
        self.cron.method_direct_trigger()
        generated_request = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", self.maintenance_plan_1.id)],
            order="schedule_date asc",
            limit=1,
        )
        generated_request.note = "TEST-INSTRUCTIONS"
        res = self.report_obj._render_qweb_text(
            "base_maintenance.report_maintenance_request",
            generated_request.ids,
            False,
        )
        self.assertRegex(str(res[0]), "TEST-INSTRUCTIONS")

    def test_maintenance_plan_button_manual_request_generation(self):
        self.assertEqual(len(self.maintenance_plan_1.maintenance_ids), 0)
        self.maintenance_plan_1.button_manual_request_generation()
        self.assertEqual(len(self.maintenance_plan_1.maintenance_ids), 3)

    def test_maintenance_equipment_company_check(self):
        """Test company constraint between equipment and maintenance plans"""
        # Create a different company
        different_company = self.env["res.company"].create({"name": "Test Company"})

        # Create an equipment with a specific company
        test_equipment = self.maintenance_equipment_obj.create(
            {"name": "Test Equipment", "company_id": different_company.id}
        )

        # Try to create a maintenance plan with a different company
        with self.assertRaises(ValidationError):
            self.maintenance_plan_obj.create(
                {
                    "equipment_id": test_equipment.id,
                    "company_id": self.env.company.id,
                    "interval": 1,
                    "interval_step": "month",
                }
            )

    def test_maintenance_equipment_multiple_plans(self):
        """Test multiple maintenance plans on an equipment"""
        # Store the initial plan count
        initial_plan_count = len(self.equipment_1.maintenance_plan_ids)

        # Create additional maintenance plans for the existing equipment
        additional_plan = self.maintenance_plan_obj.create(
            {
                "equipment_id": self.equipment_1.id,
                "interval": 2,
                "interval_step": "month",
                "maintenance_plan_horizon": 2,
                "planning_step": "month",
                "name": "Additional Test Plan",
            }
        )

        # Verify the plan is correctly associated with the equipment
        self.assertIn(additional_plan, self.equipment_1.maintenance_plan_ids)
        self.assertEqual(
            len(self.equipment_1.maintenance_plan_ids), initial_plan_count + 1
        )

    def test_maintenance_equipment_notes(self):
        """Test notes field on maintenance equipment"""
        # Add notes to an existing equipment
        self.equipment_1.notes = "Test equipment notes"

        # Verify the notes are correctly saved
        self.assertEqual(self.equipment_1.notes, "Test equipment notes")

    def test_maintenance_team_required_computation(self):
        """Test maintenance_team_required computation"""
        # The equipment should now have maintenance_team_required as True
        self.assertTrue(self.equipment_1.maintenance_team_required)

    def test_create_request_with_skip_notify(self):
        """Test creating maintenance requests with skip notification"""
        # Create a maintenance plan with skip notification
        plan_with_skip = self.maintenance_plan_obj.create(
            {
                "equipment_id": self.equipment_1.id,
                "interval": 1,
                "interval_step": "month",
                "skip_notify_follower_on_requests": True,
            }
        )

        # Trigger request generation
        self.cron.method_direct_trigger()

        # Verify requests exist and were generated with context
        generated_requests = self.maintenance_request_obj.search(
            [("maintenance_plan_id", "=", plan_with_skip.id)]
        )
        self.assertTrue(generated_requests)

    def test_maintenance_plan_unlink_with_existing_requests(self):
        """Test unlinking a maintenance plan with existing non-done requests"""
        # Generate requests first
        self.cron.method_direct_trigger()

        # Find a maintenance plan with requests
        plan_to_delete = self.maintenance_plan_1

        # Try to unlink and expect a UserError
        with self.assertRaises(UserError):
            plan_to_delete.unlink()

    def test_maintenance_plan_get_maintenance_equipments(self):
        """Test _get_maintenance_equipments method with domain generation"""
        # Create a plan with domain generation
        plan_with_domain = self.maintenance_plan_obj.create(
            {
                "generate_with_domain": True,
                "generate_domain": "[('name', 'like', 'Laptop%')]",
                "interval": 1,
                "interval_step": "month",
            }
        )

        # Get equipments for this plan
        equipments = plan_with_domain._get_maintenance_equipments()

        # Verify multiple equipments are returned based on domain
        self.assertTrue(len(equipments) > 0)
        self.assertTrue(all("Laptop" in eq.name for eq in equipments))

    def test_search_search_equipment(self):
        """Test _search_search_equipment method"""
        # Create additional equipment
        equipment_2 = self.maintenance_equipment_obj.create({"name": "Laptop 2"})

        # Create a plan with a domain
        plan_with_domain = self.maintenance_plan_obj.create(
            {
                "generate_with_domain": True,
                "generate_domain": "[('name', 'like', 'Laptop%')]",
                "interval": 1,
                "interval_step": "month",
            }
        )

        # Search for plans related to this equipment
        plans = self.maintenance_plan_obj.search(
            [("search_equipment_id", "=", equipment_2.id)]
        )

        # Verify the plan is found
        self.assertIn(plan_with_domain, plans)

    def test_equipment_company_constraint(self):
        """Test company constraint between equipment and maintenance plans"""
        # Create a different company
        different_company = self.env["res.company"].create(
            {"name": "Test Different Company"}
        )

        # Create a maintenance plan with a different company
        conflicting_plan = self.maintenance_plan_obj.create(
            {
                "company_id": different_company.id,
                "interval": 1,
                "interval_step": "month",
            }
        )

        # Create an equipment and try to link the conflicting plan
        with self.assertRaises(ValidationError):
            conflicting_plan.write({"equipment_id": self.equipment_1.id})

    def test_equipment_search_maintenance_plan_count(self):
        """Test search maintenance plan count computation"""
        # Recompute the search maintenance plan count
        self.equipment_1._compute_search_maintenance_plan_count()

        # Verify the count includes both direct and searchable plans
        self.assertGreaterEqual(
            self.equipment_1.search_maintenance_plan_count,
            len(self.equipment_1.maintenance_plan_ids),
        )
