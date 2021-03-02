import random
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from stages.models import Stage, Period
from users.models import Class, Student
# Create your models here.


class Procedure(models.Model):
    promotion = models.ForeignKey(Class, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)

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

    def compute(self):
        promotion = self.promotion
        students = Student.objects.filter(promotion=promotion).order_by('ranking')
        simulation = Simulation.objects.create(procedure=self)
        student_with_no_stages = []
        stage_temp = []
        stages = Stage.objects.all()
        for stage in stages:
            stage_temp.append(TemporaryStageDone(simulation=simulation, stage=stage))
        temp_stages = list(TemporaryStageDone.objects.bulk_create(stage_temp))
        random.shuffle(temp_stages)
        for student in students:
            wishes = StageWish.objects.filter(student=student).order_by('-importance')
            stage_given = False
            for wish in wishes:
                try:
                    temporary_stage = TemporaryStageDone.objects.get(simulation=simulation, stage=wish.stage)
                except ObjectDoesNotExist:
                    return None
                temporary_stage.value += wish.importance
                if stage_given is False:
                    if len(temporary_stage.students) < wish.stage.place_max:
                        temporary_stage.students.add(student)
                        stage_given = True
            if stage_given is False:
                student_with_no_stages.append(student)
        for student in student_with_no_stages:
            for temp_stage in temp_stages:
                if len(temp_stage.students) < temp_stage.stage.place_max:
                    temp_stage.students.add(student)
                    break
        TemporaryStageDone.objects.bulk_update(temp_stages, ['value'])
        return simulation.id


class StageWish(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    importance = models.IntegerField(default=1)
    mandatory_stage = models.BooleanField(default=False)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)


class Simulation(models.Model):
    time = models.DateTimeField(auto_now=True)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)

    def apply(self):
        all_temporary_stages = TemporaryStageDone.objects.filter(simulation=self)
        students = []
        for temporary_stage in all_temporary_stages:
            for student in temporary_stage.students:
                student.stage_points += temporary_stage.value
                students.append(student)
        Student.objects.bulk_update(students, ['stage_points'])
        self.procedure.active = False
        self.procedure.save()


class TemporaryStageDone(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    students = models.ManyToManyField(Student)
