from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from APPS.services.models import Shop
from .serializers import Fase1Serializer, Fase2PSESerializer, ShopSerializer


@api_view(['POST',])
def fase_1_pay(request):

    if request.method == 'POST':
        fase1_serializer = Fase1Serializer(data=request.data)
        if fase1_serializer.is_valid():
            fase1_serializer.save()
            return Response(fase1_serializer.data, status=status.HTTP_201_CREATED)
        return Response(fase1_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST',])
def fase_2_pse_pay(request):

    if request.method == 'POST':
        fase2_serializer = Fase2PSESerializer(data=request.data)
        if fase2_serializer.is_valid():
            fase2_serializer.save()
            return Response(fase2_serializer.data, status=status.HTTP_201_CREATED)
        return Response(fase2_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def shop_detail_view(request, pk):
    
    shop = Shop.objects.filter(id=pk).first()

    if shop:
        if request.method == 'GET':
            shop_serializer = ShopSerializer(shop)
            return Response(shop_serializer.data, status=status.HTTP_200_OK)
    
    return Response({ 'message': 'No se ha encontrado una compra con estos datos' }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST',])
def student_shop_api_view(request, pk_student=None):

    if pk_student:
        shops = Shop.objects.filter(transaction__student__id=pk_student)
        if shops:
            if request.method == 'GET':
                shops_serializer = ShopSerializer(shops, many=True)
                return Response(shops_serializer.data, status=status.HTTP_201_CREATED)
        return Response({ 'message': 'No se ha encontrado compras del estudiante con estos datos' }, status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.method == 'POST':
            shops_serializer = ShopSerializer(data=request.data)
            if shops_serializer.is_valid():
                shops_serializer.save()
                return Response(shops_serializer.data, status=status.HTTP_201_CREATED)
            return Response(shops_serializer.errors, status=status.HTTP_400_BAD_REQUEST)