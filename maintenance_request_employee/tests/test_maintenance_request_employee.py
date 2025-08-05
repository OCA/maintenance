# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import TransactionCase


class TestMaintenanceRequest(TransactionCase):
    def setUp(self):
        super().setUp()
        # Create some test employees
        self.employee_1 = self.env["hr.employee"].create({"name": "Employee 1"})
        self.employee_2 = self.env["hr.employee"].create({"name": "Employee 2"})

    def test_maintenance_request_with_employees(self):
        # Create a maintenance request and assign employees
        maintenance_request = self.env["maintenance.request"].create(
            {
                "name": "Test Request",
                "employee_ids": [(6, 0, [self.employee_1.id, self.employee_2.id])],
            }
        )

        # Ensure the request was created
        self.assertTrue(maintenance_request)

        # Check if employees are correctly linked
        self.assertEqual(len(maintenance_request.employee_ids), 2)
        self.assertIn(self.employee_1, maintenance_request.employee_ids)
        self.assertIn(self.employee_2, maintenance_request.employee_ids)

    def test_maintenance_request_without_employees(self):
        # Create a maintenance request without assigning any employees
        maintenance_request = self.env["maintenance.request"].create(
            {
                "name": "Test Request No Employees",
            }
        )

        # Ensure no employees are assigned
        self.assertEqual(len(maintenance_request.employee_ids), 0)
