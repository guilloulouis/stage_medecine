from stages.models import Stage
from django.test import TestCase


class StageTestCase(TestCase):
    def setUp(self):
        Stage.objects.create(name="Cardio")

    def test_class_name(self):
        """Stage are correctly named"""
        class1 = Stage.objects.get(name="Cardio")
        self.assertEqual(class1.name, 'Cardio')
        self.assertEqual(str(class1), "Cardio (None)")
