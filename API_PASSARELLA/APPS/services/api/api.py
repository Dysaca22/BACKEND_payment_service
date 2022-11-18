from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from requests import post
from .serializers import ConnSerializer, Phase1Serializer, Phase2Serializer
from APPS.services.models import ConnectionWithProvider, Phase1


@api_view(['POST',])
def conn_with_provider(request):
    if request.method == 'POST':
        conn_serializer = ConnSerializer(data=request.data)
        if conn_serializer.is_valid():
            conn_serializer.save()
            return Response(conn_serializer.data, status=status.HTTP_201_CREATED)
        return Response(conn_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def start_passarella(request, pk):
    conn = ConnectionWithProvider.objects.filter(pk=pk).first()
    if conn:
        if request.method == 'GET':
            conn_serializer = ConnSerializer(conn)
            return Response(conn_serializer.data, status=status.HTTP_201_CREATED)
    return Response( {'message': 'No se ha encontrado proceso de pago con estos datos'} , status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def phase1(request):
    if request.method == 'POST':
        phase1_serializer = Phase1Serializer(data=request.data)
        if phase1_serializer.is_valid():
            phase1_serializer.save()
            return Response(phase1_serializer.data, status=status.HTTP_201_CREATED)
        return Response(phase1_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def phase2(request):
    phase1 = Phase1.objects.filter(pk=request.data['phase1']).first()
    if request.method == 'POST':
        phase2_serializer = Phase2Serializer(data=request.data)
        if phase2_serializer.is_valid():
            phase2_serializer.save()
            if phase1.payment_method == 'DC':
                post_data = {
                    "phase2": phase2_serializer.data['id'],
                    "provider": phase1.connection_with_provider.provider,
                    "concept": phase1.connection_with_provider.concept,
                    "amount": phase1.connection_with_provider.amount,
                }
                response = post('http://localhost:8020/api/bank/conn_with_passarella', data=post_data)
                if response:
                    return Response(phase2_serializer.data, status=status.HTTP_201_CREATED)
                return Response({ 'message': 'Ha ocurrido un problema con la banco' }, status=status.HTTP_400_BAD_REQUEST)
        return Response(phase2_serializer.errors, status=status.HTTP_400_BAD_REQUEST)