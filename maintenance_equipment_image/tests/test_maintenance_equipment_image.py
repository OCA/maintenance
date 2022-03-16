# Copyright 2021 Exo Software
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64
import io

from PIL import Image

from odoo.tests import common


class TestMaintenanceEquipmentImage(common.TransactionCase):
    def setUp(self):
        super(TestMaintenanceEquipmentImage, self).setUp()

        self.images = {}

        # Create an image
        f = io.BytesIO()
        Image.new("RGB", (800, 500), '#FF0000').save(f, "PNG")
        f.seek(0)
        self.image = base64.b64encode(f.read())

        self.Equipment = self.env["maintenance.equipment"]
        self.equipment = self.Equipment.create(
            {
                "name": "Equipment",
                "image": self.image,
            }
        )

    def test_equipment_images_created(self):
        """ Check that all three images are created"""
        self.assertTrue(self.equipment.image)
        self.assertTrue(self.equipment.image_small)
        self.assertTrue(self.equipment.image_medium)

    def test_equipment_images_write(self):
        """ Check that when we edit equipment images all data are set"""
        self.equipment.image = False
        self.assertFalse(self.equipment.image)
        self.assertFalse(self.equipment.image_small)
        self.assertFalse(self.equipment.image_medium)
        self.equipment.write({
            "image_small": self.image,
        })
        self.assertEqual(self.equipment.image, self.image)
