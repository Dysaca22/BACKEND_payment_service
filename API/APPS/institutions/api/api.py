from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from requests import post
from APPS.institutions.models import Institution, Campus, Student, Bill, Pay
from .serializers import InfoInstitucionSerializer, StudentSerializer, StudentBillsSerializer, PaySerializer, PayFinishSerializer


"""
url: /api/institution/
Método: GET
Entrada: Ninguna
Salida:
	. institution
		.. name
	. campus
		.. name
		.. city
"""
@api_view(['GET',])
def institution_information(request):
    if request.method == 'GET':
        institution = Institution.objects.all().first()
        campus = Campus.objects.filter(institution=institution)
        data = {
            'institucion': institution,
            'campus': campus,
        }
        informacion_serializer = InfoInstitucionSerializer(data)
        return Response(informacion_serializer.data, status=status.HTTP_200_OK)


"""
url: /api/institution/student/profile
Método: GET
Entrada: Ninguna
Salida: 
	. Nombre: name
	. Apellido: lastname
	. Código: code
	. Sede: campus
	. Usuario: username
"""
@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def student_profile(request):
    if request.method == 'GET':
        student = Student.objects.filter(user=request.user).first()
        if student:
            student_serializer = StudentSerializer(student)
            return Response(student_serializer.data, status=status.HTTP_200_OK)
        return Response({ 'message': 'No se ha encontrado estudiante con estos datos' }, status=status.HTTP_400_BAD_REQUEST)
    

"""
url: /api/institution/student/bills
Método: GET
Entrada: Ninguna
Salida:
	. Estudiante: student
		.. Nombre: name
		.. Apellido: lastname
		.. Código: code
		.. Sede: campus
		.. Usuario: username
	. Cuentas: bills
		.. id
		.. semester
		.. program
		.. service
		.. value
		.. status
		.. issue_date
"""
@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def student_bills(request):
    if request.method == 'GET':
        student = Student.objects.filter(user=request.user).first()
        if student:
            bills = Bill.objects.filter(student=student)
            data = {
                'student': student,
                'bills': bills,
            }
            student_bills_serializer = StudentBillsSerializer(data)
            return Response(student_bills_serializer.data, status=status.HTTP_200_OK)
        return Response({ 'message': 'No se ha encontrado estudiante con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


"""
url: /api/institution/student/bills_to_pay
Método: GET
Entrada: Ninguna
Salida:
	. Estudiante: student
		.. Nombre: name
		.. Apellido: lastname
		.. Código: code
		.. Sede: campus
		.. Usuario: username
	. Cuentas: bills
		.. id
		.. semester
		.. program
		.. service
		.. value
		.. status
		.. issue_date

##############################################################################

url: /api/institution/student/bills_to_pay
Método: POST
Entrada: 
	. bills 			(vector con los ids de las cuentas a pagar)
Salida:
	. pay_id
	. institution
	. concept
	. value
Error: "bills": ["Clave primaria \"0\" inválida - objeto no existe."]
"""
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def student_bills_to_pay(request):
    student = Student.objects.filter(user=request.user).first()
    if student:
        if request.method == 'GET':
            bills = Bill.objects.filter(student=student, _paid=False)
            data = {
                'student': student,
                'bills': bills,
            }
            student_bills_serializer = StudentBillsSerializer(data)
            return Response(student_bills_serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            data = {
                'student': student.pk,
                'bills': request.data['bills'],
            }
            pay_serializer = PaySerializer(data=data)
            if pay_serializer.is_valid():
                pay_serializer.save()
                post_data = {
                    'pay_id': pay_serializer.data['pay_id'],
                    'provider': student.campus.__str__(),
                    'concept': pay_serializer.data['concept'],
                    'amount': pay_serializer.data['value'],
                }
                response = post('http://localhost:8010/api/passarella/conn_with_provider', data=post_data)
                if response:
                    return Response({ 'id_passarella': response.json()['id'] }, status=status.HTTP_201_CREATED)
                return Response({ 'message': 'Ha ocurrido un problema con la pasarela' }, status=status.HTTP_400_BAD_REQUEST)
            return Response(pay_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({ 'message': 'No se ha encontrado estudiante con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


"""
url: /api/institution/student/pay/<int:pk>
Método: GET
Entrada: Ninguna
Salida:
	. pay_id
	. institution
	. concept
	. value
Error: "message": "No se ha encontrado el pago con estos datos"
"""
@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def pay_information(request, pk):
    pay = Pay.objects.filter(pk=pk).first()

    if request.method == 'GET':
        if pay:
            pay_serializer = PaySerializer(pay)
            return Response(pay_serializer.data, status=status.HTTP_201_CREATED)
        return Response({ 'message': 'No se ha encontrado el pago con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


"""
url: /api/institution/student/pay/delete/<int:pk>
Método: DELETE
Entrada: Ninguna
Salida: "message": "Se ha cancelado pago con éxito"
Error: "message": "No se ha encontrado pago con estos datos"
"""
@api_view(['DELETE'])
@permission_classes((IsAuthenticated, ))
def delete_student_pay(request, pk):
    pay = Pay.objects.filter(pk=pk).first()
    if request.method == 'DELETE':
        if pay:
            pay.delete()
            return Response({ 'message': 'Se ha cancelado pago con éxito' }, status=status.HTTP_204_NO_CONTENT)
        return Response({ 'message': 'No se ha encontrado pago con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT',])
def finallize(request):
    if request.method == 'PUT':
        pay = Pay.objects.filter(pk=request.data['id']).first()
        if pay:
            pay._status = request.data['status']
            pay.receipt = request.data['number_bill']
            pay.save()
            pay.bills.update(_paid=True)
            return Response(PayFinishSerializer(pay).data, status=status.HTTP_201_CREATED)
        return Response({ 'message': 'No se ha encontrado pago con estos datos' }, status=status.HTTP_400_BAD_REQUEST)