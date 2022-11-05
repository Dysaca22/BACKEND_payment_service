from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from APPS.banks.models import Card, Person, Transaction
from .serializers import CardSerializer, PersonSerializer, TransactionSerializer

# Person

@api_view(['GET',])
def person_detail_view(request, pk):
    
    person = Person.objects.filter(id=pk).first()

    if person:
        if request.method == 'GET':
            person_serializer = PersonSerializer(person)
            return Response(person_serializer.data, status=status.HTTP_200_OK)
    
    return Response({ 'message': 'No se ha encontrado la persona con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


# Card

@api_view(['GET',])
def card_detail_view(request, pk):
    
    card = Card.objects.filter(id=pk).first()

    if card:
        if request.method == 'GET':
            card_serializer = CardSerializer(card)
            return Response(card_serializer.data, status=status.HTTP_200_OK)
    
    return Response({ 'message': 'No se ha encontrado la tarjeta con estos datos' }, status=status.HTTP_400_BAD_REQUEST)

# Person cards

@api_view(['GET',])
def person_card_api_view(request, pk_person):

    card = Card.objects.filter(person__id=pk_person)

    if card:
        if request.method == 'GET':
            card_serializer = CardSerializer(card)
            return Response(card_serializer.data, status=status.HTTP_200_OK)
    
    return Response({ 'message': 'No se ha encontrado las tarjetas de la persona con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


# Transaction

@api_view(['POST',])
def transaction_api_view(request):
    
    if request.method == 'POST':
        transactions_serializer = TransactionSerializer(data=request.data)
        if transactions_serializer.is_valid():
            transactions_serializer.save()
            return Response(transactions_serializer.data, status=status.HTTP_201_CREATED)
        return Response(transactions_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def transaction_detail_view(request, pk):
    
    transaction = Transaction.objects.filter(id=pk).first()

    if transaction:
        if request.method == 'GET':
            transaction_serializer = TransactionSerializer(transaction)
            return Response(transaction_serializer.data, status=status.HTTP_200_OK)
    
    return Response({ 'message': 'No se ha encontrado la transacción con estos datos' }, status=status.HTTP_400_BAD_REQUEST)

# Person transactions

@api_view(['GET',])
def person_transaction_api_view(request, pk_person):

    transaction = Transaction.objects.filter(person__id=pk_person)

    if transaction:
        if request.method == 'GET':
            transaction_serializer = TransactionSerializer(transaction)
            return Response(transaction_serializer.data, status=status.HTTP_200_OK)
    
    return Response({ 'message': 'No se ha encontrado las transacciones de la persona con estos datos' }, status=status.HTTP_400_BAD_REQUEST)