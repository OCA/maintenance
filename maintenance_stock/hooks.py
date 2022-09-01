# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging

from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    logging.getLogger("odoo.addons.maintenance_stock").info(
        "Adding pending locations, sequences and pìcking types to " "current warehouses"
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    PickingType = env["stock.picking.type"]
    print(env["stock.warehouse"].count_search([]))
    for warehouse in env["stock.warehouse"].search([]):
        warehouse._create_missing_locations(vals={})
        print(env["stock.warehouse"].count_search([]))
        print(warehouse)
        new_vals = warehouse._create_or_update_sequences_and_picking_types()
        print(new_vals)
        warehouse.write(new_vals)
        print(warehouse)
        # return picking type workaround for existing warehouses
        if "cons_type_id" in new_vals:
            PickingType.browse(new_vals["cons_type_id"]).write(
                {"return_picking_type_id": warehouse.in_type_id.id}
            )
