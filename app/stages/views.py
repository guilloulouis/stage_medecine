from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from stages.models import Stage, StageDone
from stages.serializer import StageSerializer, StageDoneSerializer
from users.models import Student


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stages(request):
    stages = Stage.objects.all()
    serializer = StageSerializer(stages, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stages_done(request):
    try:
        student = Student.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return Response({'error': 'student does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    stagedones = StageDone.objects.filter(student=student)
    serializer = StageDoneSerializer(stagedones, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_stages_done(request):
    stagedones = StageDone.objects.all()
    serializer = StageDoneSerializer(stagedones, many=True)
    return JsonResponse(serializer.data, safe=False)
