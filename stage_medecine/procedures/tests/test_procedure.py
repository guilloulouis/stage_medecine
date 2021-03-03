from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from procedures.models import Procedure
from django.test import TestCase, RequestFactory
from stages.models import Period
from users.models import Class, Student


class ProcedureTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
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

    def test_get_procedure_on_connect_not_admin(self):
        notadmin = User.objects.create_user(username="admin", email='test@test.com', password='admin')
        client = APIClient()
        refresh = RefreshToken.for_user(notadmin)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = client.get('/procedures/')
        self.assertEqual(response.status_code, 403)

    def test_get_procedure_not_connected(self):
        response = self.client.get('/procedures/')
        self.assertEqual(response.status_code, 401)

    def test_get_procedure_connected_admin(self):
        admin = User.objects.create_user(username="admin", email='test@test.com', password='admin', is_staff=True)
        client = APIClient()
        refresh = RefreshToken.for_user(admin)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        # self.client.login(username='admin', password='admin')
        response = client.get('/procedures/')
        self.assertEqual(response.status_code, 200)
