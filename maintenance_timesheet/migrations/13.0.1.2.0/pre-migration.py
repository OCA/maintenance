# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """ALTER TABLE maintenance_request
        ADD COLUMN timesheet_total_hours float
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE maintenance_request
        SET timesheet_total_hours=coalesce(tt.total_unit_amount, 0.0)
        FROM (
            SELECT mr.id, SUM(aal.unit_amount) total_unit_amount
            FROM maintenance_request mr
            LEFT JOIN account_analytic_line aal ON aal.maintenance_request_id = mr.id
            GROUP BY mr.id
        ) AS tt
        WHERE maintenance_request.id = tt.id
        """,
    )
