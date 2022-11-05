from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from APPS.services.models import Shop
from .serializers import ShopSerializer


# Shop

@api_view(['GET', 'PUT', 'DELETE',])
def shop_detail_view(request, pk):
    
    shop = Shop.objects.filter(id=pk).first()

    if shop:
        if request.method == 'GET':
            shop_serializer = ShopSerializer(shop)
            return Response(shop_serializer.data, status=status.HTTP_200_OK)
    
    return Response({ 'message': 'No se ha encontrado una compra con estos datos' }, status=status.HTTP_400_BAD_REQUEST)

# Student shops

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