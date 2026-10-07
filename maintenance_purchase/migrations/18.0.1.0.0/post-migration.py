# Copyright 2026 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Bring the category data from maintenance_equipment_category to the product
    if openupgrade.column_exists(
        env.cr, "maintenance_equipment_category", "product_category_id"
    ):
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE product_template pt
            SET equipment_category_id = mec.equipment_category_id
            FROM maintenance_equipment_category mec
            WHERE pt.categ_id = mec.product_category_id
                AND pt.equipment_category_id IS NULL""",
        )
