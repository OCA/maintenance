# Copyright 2026 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # 16.0 took the first equipment category of the product category,
    # for maintenance products only
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE product_template pt
        SET purchase_equipment_category_id = mec.id
        FROM (
            SELECT product_category_id, MIN(id) AS id
            FROM maintenance_equipment_category
            WHERE product_category_id IS NOT NULL
            GROUP BY product_category_id
        ) mec
        WHERE pt.categ_id = mec.product_category_id
            AND pt.maintenance_ok
            AND pt.purchase_equipment_category_id IS NULL""",
    )
