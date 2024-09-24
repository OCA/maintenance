# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.ref("maintenance.group_equipment_manager").write(
        {"implied_ids": [(3, env.ref("project.group_project_manager").id)]}
    )
