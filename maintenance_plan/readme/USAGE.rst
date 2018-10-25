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
