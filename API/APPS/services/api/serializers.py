from rest_framework import serializers
from APPS.services.models import Fase1, Fase2PSE, Shop


class Fase1Serializer(serializers.Serializer):
    class Meta:
        model = Fase1
        fields = '__all__'


class Fase2PSESerializer(serializers.Serializer):
    class Meta:
        model = Fase2PSE
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'