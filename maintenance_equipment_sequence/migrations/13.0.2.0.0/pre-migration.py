# Copyright 2021 ForgeFlow S.L. (https://forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """
    Fields 'code' and 'serial_no' of model 'maintenance.equipment' fulfill the
    same function, which is to have an internal identifier of an equipment.
    Therefore, as a solution we will use only one column.

    Field 'serial_no' is the one in odoo core and the one supposedly used for
    identifying our equipment.

    Based on this assumption, this migration will save on 'serial_no' column
    all the original values plus all the 'code' values that are null in
    'serial_no' original column. And after this, it will delete 'code' column.



    POSSIBLE ISSUE:
    Considering that this migration may not work correctly to everyone,
    because it's giving priority to 'serial_no' before 'code', we will create
    two new columns 'old_code' and 'old_serial_no' with the values of the
    original columns.

    ISSUE: If you identify your equipments with the 'code' field and you prefer to
    save it's values rather than 'serial_no' values. We provide you the following
    query:

    SQL STATEMENT:
        UPDATE maintenance_equipment
        SET serial_no = old_code
        WHERE old_code IS NOT NULL;
    """

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
             SELECT ROW_NUMBER()
             OVER(PARTITION BY code ORDER BY code,id ) AS rno, code, id
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
