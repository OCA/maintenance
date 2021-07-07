# Copyright 2019 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def fill_interval_column(cr):
    cr.execute(
        """
            UPDATE maintenance_plan mp
            SET
                (interval, interval_step) = (meq.period, 'day')
            FROM
                maintenance_plan mp2
            INNER JOIN
                maintenance_equipment meq ON mp2.equipment_id = meq.id
            WHERE meq.period is not null and mp2.id = mp.id
        """
    )


def migrate(cr, version):
    fill_interval_column(cr)
