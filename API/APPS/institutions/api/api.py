from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from APPS.institutions.models import Institution, Student, Bill
from .serializers import InstitutionSerializer, StudentSerializer, BillSerializer, GeneralInformationSerializer, PaySerializer


@api_view(['GET',])
def general_info_institution(request):

    if request.method == 'GET':
        institution = Institution.objects.all()
        institution_serializer = InstitutionSerializer(institution, many=True)
        return Response(institution_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET',])
def user_student(request, pk_user):

    student = Student.objects.filter(user__id=pk_user).first()

    if student:
        if request.method == 'GET':
            student_serializer = StudentSerializer(student)
            return Response(student_serializer.data, status=status.HTTP_200_OK)
    return Response({ 'message': 'No se ha encontrado estudiante con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def general_info_student(request, pk):

    student = Student.objects.filter(id=pk).first()

    if student:
        if request.method == 'GET':
            data = {
                'student': student,
                'bill': Bill.objects.filter(student=student),
            }
            student_serializer = GeneralInformationSerializer(data)
            return Response(student_serializer.data, status=status.HTTP_200_OK)
    return Response({ 'message': 'No se ha encontrado estudiante con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def student_by_code(request, code):
    student = Student.objects.filter(code=code).first()

    if student:
        if request.method == 'GET':
            student_serializer = StudentSerializer(student)
            return Response(student_serializer.data, status=status.HTTP_200_OK)
    return Response({ 'message': 'No se ha encontrado estudiante con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def missing_bills(request, code):
    bills = Bill.objects.filter(student__code=code, _paid=False)

    if request.method == 'GET':
        bills_serializer = BillSerializer(bills, many=True)
        return Response(bills_serializer.data, status=status.HTTP_200_OK)
    

@api_view(['POST',])
def generate_pay(request):
    if request.method == 'POST':
        pay_serializer = PaySerializer(data=request.data)
        if pay_serializer.is_valid():
            pay_serializer.save()
            return Response(pay_serializer.data, status=status.HTTP_201_CREATED)
        return Response(pay_serializer.errors, status=status.HTTP_400_BAD_REQUEST)