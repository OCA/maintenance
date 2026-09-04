# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Create a maintenance plan for equipments that had an expected MTBF.

    Odoo 19 removed ``maintenance.equipment.next_action_date`` and
    ``maintenance.equipment.mtbf``; the original migration relied on both and
    raised ``AttributeError`` on install. We now derive the plan interval from
    ``expected_mtbf`` (expressed in days) and no longer try to tag a specific
    preventive request by its (now inexistent) next action date.
    """
    _logger.info("Migrating existing preventive maintenance")
    equipments = env["maintenance.equipment"].search([("expected_mtbf", "!=", False)])
    if not equipments:
        return
    maintenance_kind = env["maintenance.kind"].create(
        {"name": "Install", "active": True}
    )
    env["maintenance.plan"].create(
        [
            {
                "equipment_id": equipment.id,
                "maintenance_kind_id": maintenance_kind.id,
                "interval": equipment.expected_mtbf,
                "interval_step": "day",
            }
            for equipment in equipments
        ]
    )
