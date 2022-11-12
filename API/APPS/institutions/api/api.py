from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from APPS.institutions.models import Institution, Campus, Student, Bill, Pay
from .serializers import InfoInstitucionSerializer, StudentSerializer, StudentBillsSerializer, PaySerializer


"""
### /institucion/home
	- Datos que envía el backend (GET al backend /institution)
		. Nombre de la institución
		. Lista de las sedes de la institución
			.. Nombre
			.. Ciudad
	- Datos de ingreso del usuario
		. Botón pagar cuentas (1)
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
### /institucion/login
	- Datos de ingreso del usuario (GET al backend /institution/student/login)
		. Usuario
		. Contraseña
    * Enviar json con user y password
	
	
### /institucion/perfil
	- Datos que envía el backend (Respuesta del GET de /institution/student/login)
		. Nombre
		. Apellido
		. Código
		. Nombre campus
		. Usuario
	- Datos de ingreso del usuario
		. Botón ver cuentas (2) o pagar cuentas (1)
"""
@api_view(['GET',])
def institution_login(request):
    if request.method == 'GET':
        user = request.data['user']
        password = request.data['password']

        student = Student.objects.filter(
            user__username=user,
            user__password=password,
        ).first()
        if student:
            student_serializer = StudentSerializer(student)
            return Response(student_serializer.data, status=status.HTTP_200_OK)
        return Response({ 'message': 'No se ha encontrado estudiante con estos datos' }, status=status.HTTP_400_BAD_REQUEST)
    

"""
( Botón ver cuentas ) (2)
### /institucion/perfil/cuentas
	- Datos que envía el backend (GET al backend /institution/student/bills)
		. Nombre
		. Apellido
		. Código
		. Lista de cuentas
			.. Semestre
			.. Programa
			.. Servicio
			.. Valor
			.. Estado
			.. Fecha de emisión
    * Enviar json con el código del estudiante
"""
@api_view(['GET',])
def student_bills(request):
    if request.method == 'GET':
        code = request.data['code']
        student = Student.objects.filter(code=code).first()
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
( Botón pagar cuentas ) (1)
### /institucion/estudiante
	- Datos de ingreso usuario (GET al backend /institution/student)
		. Código estudiante
		. Botón pagar (3)
	* Enviar json con el código del estudiante


( Botón pagar ) (3)
### /institucion/estudiante/pagar
	- Datos que envía el backend (GET al backend /institution/student/bills_to_pay/<int:code_student>)
		. Nombre
		. Apellido
		. Código
		. Lista de cuentas
			.. id
			.. Semestre
			.. Programa
			.. Servicio
			.. Valor
			.. Fecha de emisión
	- Datos de ingreso usuario (POST al backend /institution/student/pay)
		. Código estudiante
		. ids cuentas
		. Botón pagar (4) o cancelar (5)
"""
@api_view(['GET', 'POST'])
def student_bills_to_pay(request):
    if request.method == 'GET':
        code = request.data['code']
        student = Student.objects.filter(code=code).first()
        if student:
            bills = Bill.objects.filter(student=student, _paid=False)
            data = {
                'student': student,
                'bills': bills,
            }
            student_bills_serializer = StudentBillsSerializer(data)
            return Response(student_bills_serializer.data, status=status.HTTP_200_OK)
        return Response({ 'message': 'No se ha encontrado estudiante con estos datos' }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        data = {
            'student': Student.objects.filter(code=request.data['code']).first().pk,
            'bills': request.data['bills'],
        }
        pay_serializer = PaySerializer(data=data)
        if pay_serializer.is_valid():
            pay_serializer.save()
            return Response(pay_serializer.data, status=status.HTTP_201_CREATED)
        return Response(pay_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
( Botón cancelar ) (7)
### /institucion/estudiante/pagar
	- Redirección a /institucion/estudiante/pagar
	- Enviar al backend (DELETE /institution/student/bills_to_pay/<int:id_pago>)
"""
@api_view(['DELETE'])
def delete_student_bills_to_pay(request, pk):
    pay = Pay.objects.filter(pk=pk).first()
    if request.method == 'DELETE':
        if pay:
            pay.delete()
            return Response({ 'message': 'No se ha eliminado pago con éxito' }, status=status.HTTP_204_NO_CONTENT)
        return Response({ 'message': 'No se ha encontrado pago con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


"""
- Datos que envía el backend (GET /institution/student/pay/<int:pk_pago>)
		. Nombre institución
		. Concepto de servicios a pagar
		. Valor a pagar
"""
@api_view(['GET',])
def pay_information(request, pk):
    pay = Pay.objects.filter(pk=pk).first()

    if request.method == 'GET':
        if pay:
            pay_serializer = PaySerializer(pay)
            return Response(pay_serializer.data, status=status.HTTP_201_CREATED)
        return Response({ 'message': 'No se ha encontrado el pago con estos datos' }, status=status.HTTP_400_BAD_REQUEST)