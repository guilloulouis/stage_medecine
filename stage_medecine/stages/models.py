from django.db import models

# Create your models here.


class Period(models.Model):
    """Class representing each period of stage
    :param name: name of the period (indicating the number of period for each promotion for example)
    :param date_start: starting date of the period and affiliated stages
    """
    name = models.CharField(max_length=100, default="Period")
    date_start = models.DateField(auto_now_add=True)


class Category(models.Model):
    """Class representing each stage categories
    :param name: name of the stage (of service often times)
    :param mandatory: true if a student must do a stage in this category to validate his clerkship
    """
    name = models.CharField(max_length=30)
    mandatory = models.BooleanField(default=True)

    def __str__(self):
        return self.name + ' - ' + "Obligatoire" if self.mandatory else self.name + ' - ' + "Optionnel"


class Stage(models.Model):
    """Class representing each stage and its attributes
    :param name: name of the stage (of service often times)
    :param place_min: number of minimum places for each stage
    :param place_max: number of maximum places for each stage
    :param guard: boolean indicating if you can take guards during the stage
    :param category: Key indicating if the stage fills a mandatory category and if so, which one
    """

    name = models.CharField(max_length=100, default="Stage")
    place_min = models.IntegerField(default=0)
    place_max = models.IntegerField(default=0)
    guard = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name + ' (' + str(self.category) + ')'


class StageDone(models.Model):
    """Class representing the stage that has been done
    :param stage: key of the linked stage
    :param period: period of the stage so the stagedone are grouped into batch
    :param value: value of the stage in points
    """

    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, null=True)
    value = models.IntegerField(default=0)
