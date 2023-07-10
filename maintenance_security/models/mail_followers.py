# Copyright 2023 Tecnativa - Víctor Martínez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class Followers(models.Model):
    _inherit = "mail.followers"

    def _add_followers(
        self,
        res_model,
        res_ids,
        partner_ids,
        subtypes,
        check_existing=False,
        existing_policy="skip",
    ):
        """We need to prevent a partner without Maintenance permission from being
        a follower of mt_mat_assign."""
        if res_model == "maintenance.equipment":
            partner_model = self.env["res.partner"]
            group = "maintenance.group_equipment_manager"
            subtype = self.env.ref("maintenance.mt_mat_assign")
            for partner_id in partner_ids:
                if subtype.id in subtypes[partner_id]:
                    partner = partner_model.browse(partner_id)
                    user = fields.first(partner.user_ids)
                    if not user or (user and not user.has_group(group)):
                        subtypes[partner_id].remove(subtype.id)
        return super()._add_followers(
            res_model=res_model,
            res_ids=res_ids,
            partner_ids=partner_ids,
            subtypes=subtypes,
            check_existing=check_existing,
            existing_policy=existing_policy,
        )
