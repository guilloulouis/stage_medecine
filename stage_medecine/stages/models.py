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
    """
    name = models.CharField(max_length=30)


class Stage(models.Model):
    """Class representing each stage and its attributes
    :param name: name of the stage (of service often times)
    :param place_min: number of minimum places for each stage
    :param place_max: number of maximum places for each stage
    :param guard: boolean indicating if you can take guards during the stage
    :param town: town location of the stage
    :param hospital: hospital of the stage
    :param category: Key indicating if the stage fills a mandatory category and if so, which one
    """

    name = models.CharField(max_length=100, default="Stage")
    place_min = models.IntegerField(default=0)
    place_max = models.IntegerField(default=0)
    guard = models.BooleanField(default=False)
    town = models.CharField(max_length=100, default="Caen")
    hospital = models.CharField(max_length=100, default="CHU")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name + ' (' + self.town + ' - ' + self.hospital + ')'


class StageDone(models.Model):
    """Class representing the stage that has been done
    :param stage: key of the linked stage
    :param period: period of the stage so the stagedone are grouped into batch
    :param value: value of the stage in points
    """

    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, null=True)
    value = models.FloatField(default=0.0)
