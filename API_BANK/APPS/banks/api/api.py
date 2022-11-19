from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from APPS.banks.models import Bank, Service, Person, DebitCard, ConnectionWithPassarella
from .serializers import ProfileSerializer, ServiceSerializer, ConnSerializer, ConnGetSerializer, TransactionSerializer
from .functions import update_statud_connection


@api_view(['GET',])
def query_is_active(request):
    type = request.data['type']
    bank = request.data['bank']
    service = Service.objects.filter(name=type, bank__name=bank).first()
    if service:
        service_serializer = ServiceSerializer(service)
        return Response(service_serializer.data, status=status.HTTP_200_OK)
    return Response({ 'message': 'No se ha encontrado el servicio con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def conn_with_passarella(request):
    if request.method == 'POST':
        data = request.data.copy()
        bank = Bank.objects.filter(name=data['bank']).first()
        if bank:
            data.update({'bank':bank.id})
            conn_serializer = ConnSerializer(data=data)
            if conn_serializer.is_valid():
                conn_serializer.save()
                return Response(conn_serializer.data, status=status.HTTP_201_CREATED)
            return Response(conn_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({ 'message': 'No se ha encontrado el banco con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def start_pay_or_consult(request):
    person = Person.objects.filter(user=request.user).first()
    if person:
        if request.method == 'GET':
            if 'conn_with_bank_id' in request.data:
                connwithpassarella = ConnectionWithPassarella.objects.filter(id=request.data['conn_with_bank_id']).first()
                if connwithpassarella:
                    service = Service.objects.filter(name='P', bank=connwithpassarella.bank).first()
                    if service:
                        if service._status:
                            cards = DebitCard.objects.filter(person=person, bank=connwithpassarella.bank)
                            conn_get_serializer = ConnGetSerializer(connwithpassarella, context={ 'cards':cards })
                            return Response(conn_get_serializer.data, status=status.HTTP_200_OK)
                        return Response({ 'message': 'El servicio de pagos esta deshabilitado por el momento' }, status=status.HTTP_200_OK)
                    return Response({ 'message': 'No se ha encontrado el servicio con estos datos' }, status=status.HTTP_200_OK)
                return Response({ 'message': 'No se ha encontrado el proceso de pago con estos datos' }, status=status.HTTP_200_OK)
            else:
                bank = Bank.objects.filter(name=request.data['bank']).first()
                if bank:
                    service = Service.objects.filter(name='C', bank=bank).first()
                    if service:
                        if service._status:
                            profile_serializer = ProfileSerializer(person, context={ 'bank':bank.id })
                            return Response(profile_serializer.data, status=status.HTTP_200_OK)
                        return Response({ 'message': 'El servicio de consulta esta deshabilitado por el momento' }, status=status.HTTP_200_OK)
                    return Response({ 'message': 'No se ha encontrado el servicio con estos datos' }, status=status.HTTP_400_BAD_REQUEST)
                return Response({ 'message': 'No se ha encontrado banco con estos datos' }, status=status.HTTP_400_BAD_REQUEST)
    return Response({ 'message': 'No se ha encontrado la persona con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
@permission_classes((IsAuthenticated, ))
def make_transaction(request):
    if request.method == 'POST':
        conn_with_bank = ConnectionWithPassarella.objects.filter(pk=request.data['conn_with_bank_id']).first()
        if conn_with_bank:
            card = DebitCard.objects.filter(number=request.data['card']).first()
            if card:
                if card._isActive:
                    if card.balance >= conn_with_bank.amount:
                        data = {
                            'process_of_pay': conn_with_bank.id,
                            'card': card.number,
                        }
                        transaction_serializer = TransactionSerializer(data=data)
                        if transaction_serializer.is_valid():
                            card.balance -= conn_with_bank.amount
                            card.save()
                            transaction_serializer.save()
                            update_statud_connection(conn_with_bank, 'S', transaction_serializer.data['number_bill'])
                            return Response(transaction_serializer.data, status=status.HTTP_201_CREATED)
                        return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response({ 'message': 'La tarjeta seleccionada no tiene el dinero suficiente par ala transacción' }, status=status.HTTP_400_BAD_REQUEST)
                return Response({ 'message': 'La tarjeta seleccionada esta deshabilitada' }, status=status.HTTP_400_BAD_REQUEST)    
            return Response({ 'message': 'No se ha encontrado la tarjeta con estos datos' }, status=status.HTTP_400_BAD_REQUEST)
        return Response({ 'message': 'No se ha encontrado proceso de pago con estos datos' }, status=status.HTTP_400_BAD_REQUEST)