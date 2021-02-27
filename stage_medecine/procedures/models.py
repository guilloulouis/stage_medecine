from django.contrib.auth.models import User
from django.db import models
from stages.models import Stage, Period
from users.models import Class, Student
# Create your models here.


class Procedure(models.Model):
    promotion = models.ForeignKey(Class, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        students = Student.objects.filter(promotion=self.promotion).select_related('user')
        users = []
        for student in students:
            user = student.user
            user.is_active = True
            users.append(user)
        User.objects.bulk_update(users, ['is_active'])
        super(Procedure, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        students = Student.objects.filter(promotion=self.promotion).select_related('user')
        users = []
        for student in students:
            user = student.user
            user.is_active = False
            users.append(user)
        User.objects.bulk_update(users, ['is_active'])
        super(Procedure, self).delete(using, keep_parents)


class StageWish(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    importance = models.IntegerField(default=1)
    mandatory_stage = models.BooleanField(default=False)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)


class Simulation(models.Model):
    time = models.DateTimeField(auto_now=True)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)


class TemporaryStageDone(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    students = models.ManyToManyField(Student)
