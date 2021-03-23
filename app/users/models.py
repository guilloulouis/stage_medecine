from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from stages.models import StageDone


class Class(models.Model):
    """Class representing the promotion of each student forming group of students
    :param name: name of the promotion
    """
    name = models.CharField(max_length=50, default="New Promotion")


class Student(models.Model):
    """Class representing each student
    :param user: key to the user to link with the student
    :param promotion: key to the promotion that is linked to the student
    :param stages_done: list of all the stages that have been done by the student
    :param stage_points: calculated points of the student
    :param validated_categories: list of the categories that have been validated
    :param ranking: rank of the student in his promotion to choose the next stage
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Class, on_delete=models.PROTECT, null=True, blank=True)
    stages_done = models.ManyToManyField(StageDone, blank=True)
    stage_points = models.FloatField(default=0.0)

    @property
    def validated_categories(self):
        return [stage_done.stage.category for stage_done in self.stages_done.all() if stage_done.stage.category]

    @property
    def ranking(self):
        student_promo = Student.objects.filter(promotion=self.promotion).order_by('stage_points')
        for index, item in enumerate(student_promo):
            if item.id == self.id:
                return index + 1
        return -1
