from rest_framework import serializers
from procedures.models import Procedure


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ['promotion', 'period']
        depth = 1


class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ['procedure', 'time']
        depth = 1
