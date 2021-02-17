from django.db import models
from django.contrib.auth.models import AbstractUser, User
import string
import random
from django.db.models import Sum
# Create your models here.
from stages.models import StageDone


class Class(models.Model):
    """Class representing the promotion of each student forming group of students
    :param name: name of the promotion
    """
    name = models.CharField(max_length=50, default="New Promotion")


class ConnectCode(models.Model):
    """Class representing the access code that students will use to authenticate to the server
    :param unique_id: id that is generated randomly following the pattern [Letter-Letter-Number-Number-Letter-Letter]
    """
    unique_id = models.SlugField(primary_key=True, unique=True, editable=False, blank=True)

    def save(self, *args, **kwargs):
        while not self.unique_id:
            new_id = ''.join(random.sample(string.ascii_letters, 2) + random.sample(string.digits, 2) + random.sample(string.ascii_letters, 2))
            if not ConnectCode.objects.filter(pk=new_id).exists():
                self.unique_id = new_id

        super().save(*args, **kwargs)


class Student(models.Model):
    """Class representing each student
    :param user: key to the user to link with the student
    :param code: key to the code that will be generated for the student to log in when choosing a stage
    :param promotion: key to the promotion that is linked to the student
    :param stages_done: list of all the stages that have been done by the student
    :param stage_points: calculated points of the student
    :param validated_categories: list of the categories that have been validated
    :param ranking: rank of the student in his promotion to choose the next stage
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.ForeignKey(ConnectCode, on_delete=models.CASCADE, null=True)
    promotion = models.ForeignKey(Class, on_delete=models.PROTECT, null=True)
    stages_done = models.ManyToManyField(StageDone)
    stage_points = models.FloatField(default=0.0)

    @property
    def validated_categories(self):
        return [stage_done.stage.category for stage_done in self.stages_done.all() if stage_done.stage.category]

    @property
    def ranking(self):
        student_promo = Student.objects.filter(promotion=self.promotion).order_by('stage_points')
        for index, item in enumerate(student_promo):
            if item.id == self.id:
                return index+1
        return -1
