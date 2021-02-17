from stages.models import StageDone, Stage
from django.test import TestCase


class StageDoneTestCase(TestCase):
    def setUp(self):
        stage = Stage.objects.create(name="Cardio")
        StageDone.objects.create(stage=stage, value=10)

    def test_class_name(self):
        """Class are correctly named"""
        stage = Stage.objects.get(name="Cardio")
        stagedone1 = StageDone.objects.get(stage=stage)
        self.assertEqual(stagedone1.stage.name, stage.name)
