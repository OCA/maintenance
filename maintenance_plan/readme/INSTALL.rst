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
