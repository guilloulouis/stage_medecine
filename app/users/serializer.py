from rest_framework import serializers
from users.models import Class, Student


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user', 'promotion', 'stages_done', 'stage_points', 'validated_categories', 'ranking']
        depth = 2
