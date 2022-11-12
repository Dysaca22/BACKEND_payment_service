from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from APPS.services.models import Fase1
from .serializers import Fase1Serializer, Fase2Serializer


"""
( Botón pagar ) (4)
### /pasarela/fase1
	- Datos que envía el backend (Respuesta del POST de /institution/student/pay)
		. id pago
		. Nombre institución
		. Concepto de servicios a pagar
		. Valor a pagar
	- Datos de ingreso usuario (POST al backend /services/fase1)
		. Correo electrónico
		. Medio de pago (crédito o débito)
		. id pago
		. Botón continuar (6) o cancelar (7)
"""
@api_view(['POST',])
def fase1(request):
    if request.method == 'POST':
        fase1_serializer = Fase1Serializer(data=request.data)
        if fase1_serializer.is_valid():
            fase1_serializer.save()
            return Response(fase1_serializer.data, status=status.HTTP_201_CREATED)
        return Response(fase1_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

"""
( Botón continuar ) (6)
### /pasarela/fase2
	- Datos que envía el backend (Respuesta del POST de /services/fase1)
		. id fase1
		. Correo electrónico
		. Bancos
			.. Nombre
	- Datos que envía el backend (GET /institution/student/pay/<int:pk_pago>)
		. Nombre institución
		. Concepto de servicios a pagar
		. Valor a pagar
	- Datos de ingreso usuario (POST al backend /services/fase2)
		. Nombre
		. Apellido
		. Número de documento
		. Número de teléfono
		. id fase1
		. Botón continuar (8), cancelar (9) o volver
"""
@api_view(['POST',])
def fase2(request):
    if request.method == 'POST':
        fase2_serializer = Fase2Serializer(data=request.data)
        if fase2_serializer.is_valid():
            fase2_serializer.save()
            return Response(fase2_serializer.data, status=status.HTTP_201_CREATED)
        return Response(fase2_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
( Botón cancelar ) (9)
### /institucion/estudiante/pagar
	- Redirección a /institucion/estudiante/pagar
	- Enviar al backend (POST /services/fase1/delete/<int:id_fase1>)
"""
@api_view(['DELETE'])
def delete_fase1(request, pk):
    fase1 = Fase1.objects.filter(pk=pk).first()
    if request.method == 'DELETE':
        if fase1:
            fase1.delete()
            return Response({ 'message': 'No se ha eliminado la fase 1 con éxito' }, status=status.HTTP_204_NO_CONTENT)
        return Response({ 'message': 'No se ha encontrado fase 1 con estos datos' }, status=status.HTTP_400_BAD_REQUEST)