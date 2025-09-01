from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.column_exists(env.cr, "maintenance_request", "milestone_id"):
        openupgrade.add_fields(
            env,
            [
                (
                    "milestone_id",
                    "maintenance.request",
                    "maintenance_request",
                    "many2one",
                    False,
                    "maintenance_project",
                )
            ],
        )
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE maintenance_request mr
            SET milestone_id = pt.milestone_id
            FROM project_task pt
            WHERE pt.milestone_id IS NOT NULL AND mr.task_id = pt.id
            """,
        )
