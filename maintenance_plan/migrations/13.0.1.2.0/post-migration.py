# Copyright 2020 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    cr.execute(
        """
        UPDATE maintenance_plan mp
        SET company_id = me.company_id
        FROM maintenance_equipment me
        WHERE mp.equipment_id = me.id;
    """
    )
