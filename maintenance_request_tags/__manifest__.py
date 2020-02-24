# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Request Tags",
    "summary": """
        Adds tags to Maintenance Requests""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca,Odoo Community Association (OCA)",
    "website": "www.creublanca.es",
    "depends": ["maintenance_plan", "maintenance_team_hierarchy"],
    "data": [
        "views/maintenance_equipment.xml",
        "views/maintenance_plan.xml",
        "security/ir.model.access.csv",
        "views/maintenance_request_tag.xml",
        "views/maintenance_request.xml",
        "views/maintenance_team.xml",
    ],
}
