# Copyright 2021 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import logging

from odoo import SUPERUSER_ID, api

try:
    from openupgradelib import openupgrade
except Exception:
    from odoo.tools import sql as openupgrade

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    The objective of this hook is to create the column alias_id in maintenance.team
    and create the inactive aliases for each maintenance team.
    """
    if not openupgrade.column_exists(cr, "maintenance_team", "alias_id"):
        _logger.info("Creating field alias_id on maintenance_team")
        cr.execute(
            """
            ALTER TABLE maintenance_team
            ADD COLUMN alias_id int;
            """
        )


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, dict())
    teams = env["maintenance.team"].search([])
    model = env["ir.model"].search([("model", "=", "maintenance.team")])
    for team in teams:
        env["mail.alias"].create(
            {"alias_model_id": model.id, "alias_parent_thread_id": team.id}
        )
