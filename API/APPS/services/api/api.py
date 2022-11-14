from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from APPS.services.models import Fase1, Fase2
from .serializers import Fase1Serializer, Fase2Serializer
from APPS.institutions.models import Pay


"""
url: /api/passarella/fase1
Método: POST
Entrada:
	. email
	. payType			(DC: debit card, CC: credit card)
	. payID				(id del pago antes obtenida)
Salida: 
	. id
	. email
	. banks
		. EB
		. WB
Error: 
	. email: error
	. payType: error
	. payID: error
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
url: /api/passarella/fase2
Método: POST
Entrada:
	. banks				(EB: East Bank, WB: Western Bank)
	. name
	. lastname
	. idNumber
	. phone
	. fase1
Salida: 
	. id
	. institution
	. concept
	. value
	. type_card
Error: 
	. banks: error
	. name: error
	. lastname: error
	. idNumber: error
	. phone: error
	. fase1: error
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
url: /api/passarella/fase1/delete/<int:pk>
Método: DELETE
Entrada: Ninguna
Salida: { 'message': 'Se ha eliminado la fase 1 con éxito' }
Error: { 'message': 'No se ha encontrado fase 1 con estos datos' }
"""
@api_view(['DELETE'])
def delete_fase1(request, pk):
    fase1 = Fase1.objects.filter(pk=pk).first()
    if request.method == 'DELETE':
        if fase1:
            pay = Pay.objects.filter(pk=fase1.payID).first()
            pay.delete()
            fase1.delete()
            return Response({ 'message': 'Se ha eliminado la fase 1 con éxito' }, status=status.HTTP_204_NO_CONTENT)
        return Response({ 'message': 'No se ha encontrado fase 1 con estos datos' }, status=status.HTTP_400_BAD_REQUEST)
    

"""
url: /api/passarella/fase2/delete/<int:pk>
Método: DELETE
Entrada: Ninguna
Salida: { 'message': 'Se ha eliminado la fase 2 con éxito' }
Error: { 'message': 'No se ha encontrado fase 2 con estos datos' }
"""
@api_view(['DELETE',])
def delete_fase2(request, pk):
    fase2 = Fase2.objects.filter(pk=pk).first()
    if request.method == 'DELETE':
        if fase2:
            pay = Pay.objects.filter(pk=fase2.fase1.payID).first()
            pay.delete()
            fase2.fase1.delete()
            return Response({ 'message': 'Se ha eliminado la fase 2 con éxito' }, status=status.HTTP_204_NO_CONTENT)
        return Response({ 'message': 'No se ha encontrado fase 2 con estos datos' }, status=status.HTTP_400_BAD_REQUEST)