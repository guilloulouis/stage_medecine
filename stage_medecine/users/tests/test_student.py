from django.contrib.auth.models import User

from stages.models import Stage, StageDone, Category
from users.models import Student
from django.test import TestCase, Client


class StudentTestCase(TestCase):
    def setUp(self):
        user_test = User.objects.create_user(username="test1", email='test@test.com', password='test')
        User.objects.create_user(username="test2", email='test@test.com', password='test')
        student = Student.objects.get(user=user_test)

    def test_student_user_exist(self):
        """Check if the user of the student exists"""
        user = User.objects.get(username="test1")
        student = Student.objects.get(user=user)
        self.assertEqual(student.user.username, user.username)

    def test_student_stage_points_initialized(self):
        """Check if the user has 0 stage points"""
        user = User.objects.get(username="test2")
        student = Student.objects.get(user=user)
        self.assertEqual(student.stage_points, 0)

    def test_student_stage_points_add(self):
        """Check if the user has stage points after adding a stage done"""
        stage = Stage.objects.create(name="Cardio")
        stage_done_test = StageDone.objects.create(stage=stage, value=10)
        user = User.objects.get(username="test2")
        student = Student.objects.get(user=user)
        student.stages_done.add(stage_done_test)
        self.assertEqual(student.stage_points, 10)

    def test_student_stage_ranking(self):
        """Check if the user ranking evolves with its points"""
        stage = Stage.objects.create(name="Cardio")
        stage_done_test = StageDone.objects.create(stage=stage, value=10)
        stage_done_test2 = StageDone.objects.create(stage=stage, value=20)
        user = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        student = Student.objects.get(user=user)
        student2 = Student.objects.get(user=user2)
        student.stages_done.add(stage_done_test)
        self.assertEqual(student.ranking, 2)
        student2.stages_done.add(stage_done_test2)
        self.assertEqual(student2.ranking, 2)
        self.assertEqual(student.ranking, 1)

    def test_student_stage_validated_category(self):
        """Check if the user validated category evolves when adding stages only when stage contains a category"""
        category = Category.objects.create(name='MED')
        stage = Stage.objects.create(name="Cardio", category=category)
        stage_done_test = StageDone.objects.create(stage=stage, value=10)
        stage2 = Stage.objects.create(name="Cardio2")
        stage_done_test2 = StageDone.objects.create(stage=stage2, value=10)
        user = User.objects.get(username="test1")
        student = Student.objects.get(user=user)
        student.stages_done.add(stage_done_test)
        self.assertEqual(student.validated_categories, [category])
        student.stages_done.add(stage_done_test2)
        self.assertEqual(student.validated_categories, [category])
