# Copyright 2021 ForgeFlow S.L. (https://forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not version:
        return

    if not openupgrade.column_exists(env.cr, "maintenance_equipment", "code"):
        return

    openupgrade.copy_columns(
        env.cr, {"maintenance_equipment": [("code", "old_code", None)]}
    )
    openupgrade.copy_columns(
        env.cr, {"maintenance_equipment": [("serial_no", "old_serial_no", None)]}
    )

    openupgrade.logged_query(
        env.cr,
        """
        UPDATE maintenance_equipment
        SET code = serial_no
        WHERE serial_no IS NOT NULL""",
    )

    openupgrade.logged_query(
        env.cr,
        """
        WITH cte AS
        (
             SELECT ROW_NUMBER() OVER(PARTITION BY code ORDER BY code,id ) AS rno, code, id
            FROM maintenance_equipment
        )
        UPDATE maintenance_equipment me
        SET code = me.code || '_' || cte.rno
        FROM cte
        WHERE cte.rno>1 AND cte.id = me.id""",
    )

    openupgrade.logged_query(
        env.cr,
        """
        UPDATE maintenance_equipment
        SET serial_no = code
        WHERE code IS NOT NULL
        """,
    )

    openupgrade.drop_columns(env.cr, [("maintenance_equipment", "code")])
