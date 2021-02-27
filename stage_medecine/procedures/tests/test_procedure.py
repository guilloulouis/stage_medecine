from django.contrib.auth.models import User
from procedures.models import Procedure
from django.test import TestCase
from stages.models import Period
from users.models import Class, Student


class ProcedureTestCase(TestCase):
    def setUp(self):
        promotion = Class.objects.create(name='promo1')
        user_test = User.objects.create_user(username="test1", email='test@test.com', password='test', is_active=False)
        user_test2 = User.objects.create_user(username="test2", email='test@test.com', password='test', is_active=False)
        Student.objects.create(user=user_test, promotion=promotion)
        Student.objects.create(user=user_test2, promotion=promotion)
        period = Period.objects.create(name='first period')
        Procedure.objects.create(promotion=promotion, period=period)

    def test_all_user_active(self):
        """all users are active in the procedure"""
        procedure = Procedure.objects.first()
        students = Student.objects.filter(promotion=procedure.promotion)
        for student in students:
            self.assertEqual(student.user.is_active, True)

    def test_all_user_inactive_on_delete(self):
        """all users are inactive when the procedure is deleted"""
        procedure = Procedure.objects.first()
        students = Student.objects.filter(promotion=procedure.promotion)
        procedure.delete()
        for student in students:
            self.assertEqual(student.user.is_active, False)
