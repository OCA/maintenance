# Copyright 2019 Creu Blanca
# Copyright 2026 NuoBiT Solutions - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Maintenance Request Stage transition",
    "summary": """
        Manage transition visibility and management between stages""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/maintenance",
    "depends": ["maintenance"],
    "data": ["views/maintenance_request.xml", "views/maintenance_stage.xml"],
    "demo": ["data/demo_maintenance_request_stage_transition.xml"],
    "maintainers": ["etobella"],
}
