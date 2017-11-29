.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================
Maintenance Plan
================

This module extends the functionality of Odoo Maintenance module by allowing
an equipment to have different preventive maintenance kinds.

Installation
============

Install the module.

Should you already use the maintenance module and have equipments with field
'Preventive Maintenance Frequency' defined, a new maintenance plan will be
automatically created on these equipments with maintenance kind 'Install'.

Moreover if a Request of type 'preventive' exists, whose stage isn't marked as
'Request done', and has a Request Date matching the equipment's
'Next Preventive Maintenance', the request will be updated with the
'Install' maintenance kind.

Make sure you don't have multiple 'preventive' requests at a stage which isn't
marked as 'Request done' and on the same 'Request date' as the equipment or
the module installation will fail with a User Error.


Usage
=====

Instead of defining a period and duration for only one preventive maintenance
per equipment, you can define multiple preventive maintenance kind for each
equipment.

Maintenance Kinds have to be defined through the configuration menu. Their name
have to be unique and can be set as active or inactive, should these not be
used anymore.

On any equipment over the maintenance tab, the maintenance plan will appear
as an embedded list view, allowing to add different maintenance kind with their
own period and duration. The next maintenance date will then be computed
automatically according to today's date and the period defined, but the
maintenance request won't be created automatically as is the case in Odoo's
Maintenance module.

Instead, this module uses the original Cron job of Odoo's Maintenance module
to generate maintenance requests, should there not be any requests which is not
done, at the request date matching the maintenance plan next_maintenance_date
for this equipment and this maintenance kind !


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/240/10.0


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/maintenance/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Akim Juillerat <akim.juillerat@camptocamp.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
