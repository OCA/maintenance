# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tools.sql import column_exists, create_column


def pre_init_hook(env):
    """Set existing equipment to confirmed, as it is already in use."""
    if not column_exists(env.cr, "maintenance_equipment", "state"):
        create_column(env.cr, "maintenance_equipment", "state", "varchar")
        env.cr.execute("UPDATE maintenance_equipment SET state = 'confirmed'")
