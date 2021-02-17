from datetime import datetime

from stages.models import Period
from django.test import TestCase


class PeriodTestCase(TestCase):
    def setUp(self):
        Period.objects.create(name="2016")

    def test_class_name(self):
        """Period are correctly named with good date"""
        period1 = Period.objects.get(name="2016")
        current_date = datetime.now().date()
        self.assertEqual(period1.date_start, current_date)
