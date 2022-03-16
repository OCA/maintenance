# Copyright 2021 Exo Software, Lda.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    image = fields.Binary(
        attachment=True,
        help="This field holds the image used as image for the equipment, "
             "limited to 1024x1024px.",
    )
    image_medium = fields.Binary(
        string="Medium-sized image",
        attachment=True,
        help="Medium-sized image of the equipment. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved, "
             "only when the image exceeds one of those sizes. Use this "
             "field in form views or some kanban views.")
    image_small = fields.Binary(
        string="Small-sized image",
        attachment=True,
        help="Small-sized image of the equipment. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.",
    )

    @api.model_create_multi
    def create(self, values_list):
        for values in values_list:
            tools.image_resize_images(values)
        return super().create(values_list)

    @api.multi
    def write(self, values):
        tools.image_resize_images(values)
        return super().write(values)
