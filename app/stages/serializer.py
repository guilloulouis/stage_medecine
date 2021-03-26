from rest_framework import serializers
from stages.models import Period, Category, Stage, StageDone


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['name', 'date_start']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'mandatory']


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['name', 'place_max', 'guard', 'category']
        depth = 1


class StageDoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageDone
        fields = ['stage', 'period', 'value']
        depth = 2
