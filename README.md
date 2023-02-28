
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/maintenance&target_branch=13.0)
[![Pre-commit Status](https://github.com/OCA/maintenance/actions/workflows/pre-commit.yml/badge.svg?branch=13.0)](https://github.com/OCA/maintenance/actions/workflows/pre-commit.yml?query=branch%3A13.0)
[![Build Status](https://github.com/OCA/maintenance/actions/workflows/test.yml/badge.svg?branch=13.0)](https://github.com/OCA/maintenance/actions/workflows/test.yml?query=branch%3A13.0)
[![codecov](https://codecov.io/gh/OCA/maintenance/branch/13.0/graph/badge.svg)](https://codecov.io/gh/OCA/maintenance)
[![Translation Status](https://translation.odoo-community.org/widgets/maintenance-13-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/maintenance-13-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# Maintenance

Odoo modules for businesses that involves maintenance tasks.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[base_maintenance](base_maintenance/) | 13.0.1.2.0 |  | Base Maintenance
[base_maintenance_config](base_maintenance_config/) | 13.0.1.0.0 |  | Provides general settings for the Maintenance App
[base_maintenance_group](base_maintenance_group/) | 13.0.1.0.1 |  | Provides base access groups for the Maintenance App
[maintenance_account](maintenance_account/) | 13.0.1.0.0 | [![victoralmau](https://github.com/victoralmau.png?size=30px)](https://github.com/victoralmau) | Maintenance Account
[maintenance_equipment_always_fold](maintenance_equipment_always_fold/) | 13.0.1.0.0 | [![dalonsod](https://github.com/dalonsod.png?size=30px)](https://github.com/dalonsod) | Equipment categories will always be folded if I indicate it with an always_fold Boolean; if not, let him behave as before
[maintenance_equipment_category_kanban](maintenance_equipment_category_kanban/) | 13.0.1.1.0 | [![dalonsod](https://github.com/dalonsod.png?size=30px)](https://github.com/dalonsod) | Sets kanban category groping by default for equipments
[maintenance_equipment_contract](maintenance_equipment_contract/) | 13.0.1.0.2 |  | Manage equipment contracts
[maintenance_equipment_custom_info](maintenance_equipment_custom_info/) | 13.0.1.0.0 |  | Add custom info in equipments
[maintenance_equipment_hierarchy](maintenance_equipment_hierarchy/) | 13.0.1.0.2 |  | Manage equipment hierarchy
[maintenance_equipment_scrap](maintenance_equipment_scrap/) | 13.0.1.0.0 |  | Enhance the functionality for Scrapping Equipments
[maintenance_equipment_sequence](maintenance_equipment_sequence/) | 13.0.1.0.0 |  | Adds sequence to maintenance equipment defined in the equipment's category
[maintenance_equipment_status](maintenance_equipment_status/) | 13.0.1.0.1 |  | Maintenance Equipment Status
[maintenance_equipment_tags](maintenance_equipment_tags/) | 13.0.1.0.0 |  | Adds category tags to equipment
[maintenance_plan](maintenance_plan/) | 13.0.1.7.1 |  | Extends preventive maintenance planning
[maintenance_plan_activity](maintenance_plan_activity/) | 13.0.1.0.1 |  | This module allows defining in the maintenance plan activities that will be created once the maintenance requests are created as a consequence of the plan itself.
[maintenance_plan_employee](maintenance_plan_employee/) | 13.0.1.0.0 | [![victoralmau](https://github.com/victoralmau.png?size=30px)](https://github.com/victoralmau) | Maintenance Plan Employee
[maintenance_product](maintenance_product/) | 13.0.1.0.0 | [![victoralmau](https://github.com/victoralmau.png?size=30px)](https://github.com/victoralmau) | Maintenance Product
[maintenance_project](maintenance_project/) | 13.0.1.1.0 |  | Adds projects to maintenance equipments and requests
[maintenance_project_plan](maintenance_project_plan/) | 13.0.1.0.0 |  | Adds project and task to a Maintenance Plan
[maintenance_remote](maintenance_remote/) | 13.0.1.0.0 |  | Define remote on maintenance request
[maintenance_request_employee](maintenance_request_employee/) | 13.0.1.0.0 | [![victoralmau](https://github.com/victoralmau.png?size=30px)](https://github.com/victoralmau) | Maintenance Request Employee
[maintenance_request_sequence](maintenance_request_sequence/) | 13.0.1.0.0 |  | Adds sequence to maintenance requests
[maintenance_request_stage_transition](maintenance_request_stage_transition/) | 13.0.1.1.0 | [![etobella](https://github.com/etobella.png?size=30px)](https://github.com/etobella) | Manage transition visibility and management between stages
[maintenance_team_hierarchy](maintenance_team_hierarchy/) | 13.0.1.0.0 |  | Create hierarchies on teams
[maintenance_timesheet](maintenance_timesheet/) | 13.0.1.3.0 |  | Adds timesheets to maintenance requests
[maintenance_timesheet_time_control](maintenance_timesheet_time_control/) | 13.0.1.1.0 | [![victoralmau](https://github.com/victoralmau.png?size=30px)](https://github.com/victoralmau) | Maintenance Timesheets Timesheet Time Control

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.
