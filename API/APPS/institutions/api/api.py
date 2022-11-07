from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from APPS.institutions.models import Institution, Service, Program, Semester, Student, Bill
from .serializers import InstitutionSerializer, CreationStudenUserSerializer, ServiceSerializer, GeneralInformationSerializer


@api_view(['GET',])
def general_info_institution(request):

    if request.method == 'GET':
        institution = Institution.objects.all()
        general_serializer = InstitutionSerializer(institution, many=True)
        return Response(general_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST',])
def create_student(request):
    
    if request.method == 'POST':
        student_serializer = CreationStudenUserSerializer(data=request.data)
        if student_serializer.is_valid():
            student_serializer.save()
            return Response(student_serializer.data, status=status.HTTP_201_CREATED)
        return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def general_info_student(request, pk):

    student = Student.objects.filter(id=pk).first()

    if student:
        if request.method == 'GET':
            data = {
                'student': student,
                'bill': Bill.objects.filter(student=student),
            }
            user_serializer = GeneralInformationSerializer(data)
            return Response(user_serializer.data, status=status.HTTP_200_OK)