from users.models import Class
from django.test import TestCase


class ClassTestCase(TestCase):
    def setUp(self):
        Class.objects.create(name="DFASM1")

    def test_class_name(self):
        """Class are correctly named"""
        class1 = Class.objects.get(name="DFASM1")
        self.assertEqual(class1.name, 'DFASM1')
