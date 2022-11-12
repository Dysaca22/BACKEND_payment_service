from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from APPS.banks.models import Person, Card
from .serializers import TransactionPreparationSerializer


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
def bank_login(request):
    if request.method == 'GET':
        user = request.data['user']
        password = request.data['password']

        person = Person.objects.filter(
            user__username=user,
            user__password=password,
        ).first()
        if person:
            data = {
                'passarellaID': request.data['id_fase2'],
                'institution': request.data['institution'],
                'concept': request.data['concept'],
                'value': request.data['value'],
            }
            cards = Card.objects.filter(person=person, type=request.data['type_card'])
            pay_preparation_serializer = TransactionPreparationSerializer(data=data, context={'person': person, 'cards': cards,})
            return Response(pay_preparation_serializer.data, status=status.HTTP_200_OK)
        return Response({ 'message': 'No se ha encontrado la persona con estos datos' }, status=status.HTTP_400_BAD_REQUEST)