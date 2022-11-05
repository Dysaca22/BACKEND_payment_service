from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from APPS.institutions.models import Institution, Student, StudentService
from .serializers import InstitutionSerializer, StudentSerializer, StudentUserSerializer, StudentServiceSerializer


# Institution

@api_view(['GET',])
def institution_api_view(request):

    if request.method == 'GET':
        institutions = Institution.objects.all()
        institutions_serializer = InstitutionSerializer(institutions, many=True)
        return Response(institutions_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET',])
def institution_detail_view(request, pk):
    
    institution = Institution.objects.filter(id=pk).first()

    if institution:
        if request.method == 'GET':
            institution_serializer = InstitutionSerializer(institution)
            return Response(institution_serializer.data, status=status.HTTP_200_OK)
    
    return Response({ 'message': 'No se ha encontrado la institución con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


# Students

@api_view(['POST',])
def student_api_view(request):
    
    if request.method == 'POST':
        student_serializer = StudentUserSerializer(data=request.data)
        if student_serializer.is_valid():
            student_serializer.save()
            return Response(student_serializer.data, status=status.HTTP_201_CREATED)
        return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT',])
def student_detail_view(request, pk):
    
    student = Student.objects.filter(id=pk).first()

    if student:
        if request.method == 'GET':
            student_serializer = StudentSerializer(student)
            return Response(student_serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            student_serializer = StudentSerializer(student, data=request.data)
            if student_serializer.is_valid():
                student_serializer.save()
                return Response(student_serializer.data, status=status.HTTP_200_OK)
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({ 'message': 'No se ha encontrado un estudiante con estos datos' }, status=status.HTTP_400_BAD_REQUEST)

# Student services

@api_view(['GET', 'POST',])
def student_service_api_view(request, pk_student=None):
    if pk_student:
        student = Student.objects.filter(id=pk_student)
        if student:
            services = StudentService.objects.filter(student=student)
            if services:
                if request.method == 'GET':
                    services_serializer = StudentServiceSerializer(services, many=True)
                    return Response(services_serializer.data, status=status.HTTP_201_CREATED)
            return Response({ 'message': 'No se ha encontrado el servicio con estos datos' }, status=status.HTTP_400_BAD_REQUEST)
        return Response({ 'message': 'No se ha encontrado la/el estudiante con estos datos' }, status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.method == 'POST':
            services_serializer = StudentService(data=request.data)
            if services_serializer.is_valid():
                services_serializer.save()
                return Response(services_serializer.data, status=status.HTTP_201_CREATED)
            return Response(services_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE',])
def student_service_detail_view(request, pk):
    
    service = StudentService.objects.filter(id=pk).first()

    if service:
        if request.method == 'GET':
            service_serializer = StudentServiceSerializer(service)
            return Response(service_serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            service.delete()
            return Response({ 'message': 'Servicio cancelado correctamente!' }, status=status.HTTP_200_OK)
    
    return Response({ 'message': 'No se ha encontrado el servicio con estos datos' }, status=status.HTTP_400_BAD_REQUEST)