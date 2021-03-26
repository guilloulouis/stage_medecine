from datetime import datetime

from procedures.models import Simulation, Procedure
from django.test import TestCase

from stages.models import Period
from users.models import Class


class SimulationTestCase(TestCase):
    def setUp(self):
        promotion = Class.objects.create(name='promo1')
        period = Period.objects.create(name='first period')
        procedure = Procedure.objects.create(promotion=promotion, period=period)
        Simulation.objects.create(procedure=procedure)

    def test_time(self):
        """Test if time is different that current time"""
        time = datetime.now()
        simulation = Simulation.objects.first()
        self.assertNotEqual(simulation.time, time)
