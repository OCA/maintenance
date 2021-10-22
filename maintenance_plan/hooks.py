# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, _, api
from odoo.exceptions import UserError


def post_init_hook(cr, registry):

    logging.getLogger("odoo.addons.maintenance_plan").info(
        "Migrating existing preventive maintenance"
    )

    env = api.Environment(cr, SUPERUSER_ID, {})

    equipments = env["maintenance.equipment"].search([("period", "!=", False)])

    if equipments:

        maintenance_kind = env["maintenance.kind"].create(
            {"name": "Install", "active": True}
        )

        for equipment in equipments:
            request = equipment.maintenance_ids.filtered(
                lambda r: r.maintenance_type == "preventive"
                and not r.stage_id.done
                and r.request_date == equipment.next_action_date
            )
            if len(request) > 1:
                raise UserError(
                    _(
                        "You have multiple preventive maintenance requests on "
                        "equipment %(name)s next action date (%(date)s). Please leave only "
                        "one preventive request on the date of equipment's next "
                        "action to install the module.",
                        name=equipment.name,
                        date=equipment.next_action_date,
                    )
                )
            elif len(request) == 1:
                request.write({"maintenance_kind_id": maintenance_kind.id})
            env["maintenance.plan"].create(
                {
                    "equipment_id": equipment.id,
                    "maintenance_kind_id": maintenance_kind.id,
                    "duration": equipment.maintenance_duration,
                    "interval": equipment.period,
                }
            )
