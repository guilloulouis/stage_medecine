import re
from users.models import ConnectCode
from django.test import TestCase


class ConnectCodeTestCase(TestCase):
    def setUp(self):
        ConnectCode.objects.create()
        ConnectCode.objects.create()

    def test_connectcode_id_initialized(self):
        """Connect code unique id isn't empty even if it's not manually initialized"""
        connectcode1 = ConnectCode.objects.first()
        self.assertNotEqual(connectcode1.unique_id, '')

    def test_connectcode_id_regex(self):
        """Connect code unique id follow the regex [a-zA-Z]{2}[0-9]{2}[a-zA-Z]{2}"""
        connectcode1 = ConnectCode.objects.first()
        matched = re.match("[a-zA-Z]{2}[0-9]{2}[a-zA-Z]{2}", connectcode1.unique_id)
        self.assertEqual(bool(matched), True)

    def test_connectcode_id_different(self):
        """Connected code unique id are unique"""
        connectcode1 = ConnectCode.objects.first()
        connectcode2 = ConnectCode.objects.last()
        self.assertNotEqual(connectcode1.unique_id, connectcode2.unique_id)
