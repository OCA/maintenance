Instead of defining a period and duration for only one preventive maintenance
per equipment, you can define multiple preventive maintenance kind for each
equipment.

Maintenance Kinds have to be defined through the configuration menu. Their name
have to be unique and can be set as active or inactive, should these not be
used anymore.

On any equipment over the maintenance tab, the maintenance plan be accessible,
allowing to add different maintenance kind with their
own frequency and duration. The next maintenance date will then be computed
automatically according to the start's date and the frequency defined, but the
maintenance request won't be created automatically as is the case in Odoo's
Maintenance module. In the plan there's also a field allowing the user to set the
maintenance horizon, insert the instructions to follow on the maintenance that
will be forwarded to the maintenance request generated from the plan.

This module uses the original Cron job of Odoo's Maintenance module to generate
maintenance requests. To do so, it takes into account the planning horizon and
generates all maintenance requests whose schedule date would fall inside that
planning horizon. Therefore, the maintenance manager can have a proper planning
of how many maintenance requests are programming for the future. Leaving planning
horizon to 0 will only create those maintenance request that are scheduled for
today.
