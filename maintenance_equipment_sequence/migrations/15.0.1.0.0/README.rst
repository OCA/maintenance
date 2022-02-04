==============================
Maintenance Equipment Sequence
==============================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fmaintenance-lightgray.png?logo=github
    :target: https://github.com/OCA/maintenance/tree/14.0/maintenance_equipment_sequence
    :alt: OCA/maintenance
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/maintenance-14-0/maintenance-14-0-maintenance_equipment_sequence
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runbot-Try%20me-875A7B.png
    :target: https://runbot.odoo-community.org/runbot/240/14.0
    :alt: Try me on Runbot

|badge1| |badge2| |badge3| |badge4| |badge5|

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
