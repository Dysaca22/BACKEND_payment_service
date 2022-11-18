from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from APPS.banks.models import Bank, Service, Person, Card
from .serializers import TransactionPreparationSerializer, ServiceSerializer


"""
( Botón continuar ) (8)
### /[nombre_banco]/[metodo_pago]/pagoElectronico?PAYMENT_ID=[id_fase2]
	- Datos que envía el backend (Respuesta del POST de /services/fase2)
		. id fase2
		. Nombre institución
		. Concepto de servicios a pagar
		. Valor a pagar
		. Medio de pago (crédito o débito)
	- Datos de ingreso usuario (GET al backend /banks/pay/login)
		. Usuario
		. Contraseña
		. Botón login (10) o cancelar (11)
	* Enviar por json lo siguiente:
		. id fase2
		. Nombre institución
		. Concepto de servicios a pagar
		. Valor a pagar
		. Medio de pago (crédito o débito)
"""
@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def bank_login(request):
    person = Person.objects.filter(user=request.user).first()

    if person:
        """send_mail(
            'Segunda clave banco',
            f'{123456}',
            'dysaca0022@gmil.com',
            ['dilanc@uninorte.edu.co'],
            fail_silently=False,
        )"""
        if request.method == 'GET':
            cards = Card.objects.filter(person=person)
            pay_preparation_serializer = TransactionPreparationSerializer(data=request.data, context={'person': person, 'cards': cards,})
            if pay_preparation_serializer.is_valid():
                pay_preparation_serializer.save()
                return Response(pay_preparation_serializer.data, status=status.HTTP_200_OK)
            return Response(pay_preparation_serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    return Response({ 'message': 'No se ha encontrado la persona con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def query_is_active(request):
    type = request.data['type']
    bank = request.data['bank']
    bank = Bank.objects.filter(name=bank).first()
    if bank:
        service = Service.objects.filter(name=type, bank=bank).first()
        if service:
            service_serializer = ServiceSerializer(service)
            return Response(service_serializer.data, status=status.HTTP_200_OK)
        return Response({ 'message': 'No se ha encontrado el servicio con estos datos' }, status=status.HTTP_400_BAD_REQUEST)
    return Response({ 'message': 'No se ha encontrado el banco con estos datos' }, status=status.HTTP_400_BAD_REQUEST)