from openupgradelib import openupgrade

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    if openupgrade.column_exists(env.cr, "maintenance_plan", "note"):
        openupgrade.rename_fields(
            env,
            [
                (
                    "maintenance.plan",
                    "maintenance_plan",
                    "note",
                    "instruction_text",
                ),
            ],
        )
