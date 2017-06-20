.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Maintenance Equipments Scrap
============================

This module improves the action of scrapping an equipment, sending a
message and automatically setting the scrap date when the action is performed.

Configuration
=============

To configure this module, you need to:

#. [OPTIONAL] Go to 'Settings' -> 'Technical' -> 'Email' -> 'Templates' and create a new template you wish to use for equipment scrapping notifications. Notice that a default template is already provided by this module. If you wish to use it, you can skip this step.
#. [OPTIONAL] Go to 'Maintenance' -> 'Configuration' -> 'Equipment Categories' and create a new equipment category or select an already existing one.
#. [OPTIONAL] You will be able to select a mail template as 'Equipment Scrap Email Template'
#. Go to 'Maintenance' -> 'Equipments' and create a new equipment or select an already existing one
#. You will be able to select a mail template as 'Equipment Scrap Template Email'. Note that if you select an equipment category on which you previously selected a mail template, the same male template will be automatically proposed.

Usage
=====

If you want to scrap an equipment, you need to:

#. Go to 'Maintenance' -> 'Equipments' and select an already existing equipment
#. Click the button 'Scrap'
#. On the wizard select a date for the field 'Scrap Date' and click 'Scrap'

You will find that the selected date was automatically set to the 'Scrap Date' field of the equipment.
Moreover, if on the equipment an 'Equipment Scrap Template Email' was set, such template was used to generate a message to notify that the equipment was scrapped.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/92/10.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/account-financial-tools/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Antonio Esposito <a.esposito@onestein.nl>
* Andrea Stirpe <a.stirpe@onestein.nl>

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
