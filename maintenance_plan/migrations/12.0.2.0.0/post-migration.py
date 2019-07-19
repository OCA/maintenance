# Copyright 2019 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def fill_interval_column(cr):
    cr.execute(
        """
            UPDATE maintenance_plan
            SET
             interval = period, interval_step = 'day';
        """
    )


def migrate(cr, version):
    fill_interval_column(cr)
