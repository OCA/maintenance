# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Equipment Contract",
    "summary": """
        Manage equipment contracts""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["contract", "base_maintenance"],
    "data": ["views/contract_contract.xml", "views/maintenance_equipment.xml"],
    "demo": ["demo/maintenance_equipment_contract_demo.xml"],
}
