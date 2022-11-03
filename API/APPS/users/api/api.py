from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from APPS.users.models import User
from .serializers import UserSerializer


@api_view(['GET', 'POST',])
def user_api_view(request):

    if request.method == 'GET':
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'POST':
        users_serializer = UserSerializer(data=request.data)
        if users_serializer.is_valid():
            users_serializer.save()
            return Response(users_serializer.data, status=status.HTTP_201_CREATED)
        return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_view(request, pk):
    
    user = User.objects.filter(id=pk).first()

    if user:
        if request.method == 'GET':
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            user_serializer = UserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.methd == 'DELETE':
            user.delete()
            return Response({ 'message': 'Usuario eliminado correctamente!' }, status=status.HTTP_200_OK)
    
    return Response({ 'message': 'No se ha encontrado un usuario con estos datos' }, status=status.HTTP_400_BAD_REQUEST)