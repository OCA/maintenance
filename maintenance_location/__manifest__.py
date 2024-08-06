# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Location",
    "summary": """
        Define a location system for maintenance""",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca,Odoo Community Association (OCA)",
    "website": "www.creublanca.es",
    "depends": ["maintenance_plan", "web_widget_child_selector"],
    "data": [
        "views/maintenance_plan.xml",
        "views/maintenance_equipment.xml",
        "security/ir.model.access.csv",
        "views/maintenance_request.xml",
        "views/maintenance_location.xml",
    ],
}
