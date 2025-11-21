from django.test import TestCase
from django.core.exceptopns import ValidationError
from .model import Consumable

class ConsumableModelsTest(TestCase):
    def test_negative_quantity_not_allowed(self):
        consumable= Consumable(
            name="Тест",
            quantity=-10,
            unit="шт"
        )
        with self.assertRaises(ValidationError):
            consumable.full_clean()