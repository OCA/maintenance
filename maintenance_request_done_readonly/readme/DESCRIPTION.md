This module makes completed maintenance requests read-only.

Once a request reaches a done stage, it can no longer be edited or reopened:
any attempt to change its fields (including moving it back out of the done
stage) is blocked. Only members of the *Maintenance: Edit Completed Requests*
group keep full access to completed requests. *Equipment Manager* users get
that group by default, so it can also be granted to users who should be able
to correct completed requests without being maintenance managers.

The restriction is enforced on write, so every field is locked by default,
without having to enumerate them. Completing a request and its follow-up
(commenting, following, scheduling activities) keep working.

If some fields should stay editable after completion, edit the
``maintenance_request_done_readonly.editable_fields`` system parameter
(*Settings > Technical > Parameters > System Parameters*, created on install)
and set a comma-separated list of their technical names.
