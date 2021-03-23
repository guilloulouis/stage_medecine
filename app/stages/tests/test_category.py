from stages.models import Category
from django.test import TestCase


class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="MED")

    def test_class_name(self):
        """Category are correctly named"""
        category = Category.objects.get(name="MED")
        self.assertEqual(category.name, 'MED')
