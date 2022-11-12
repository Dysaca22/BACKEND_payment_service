from rest_framework import serializers
from APPS.services.models import Fase1, Fase2


class Fase1Serializer(serializers.Serializer):
    class Meta:
        model = Fase1
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            'banks': dict(Fase2.BANK_ENUM).values(),
        }


class Fase2Serializer(serializers.Serializer):
    class Meta:
        model = Fase2
        fields = '__all__'