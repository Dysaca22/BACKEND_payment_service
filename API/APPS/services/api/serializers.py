from rest_framework import serializers
from APPS.services.models import Fase1, Fase2
from APPS.institutions.models import Pay


class Fase1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Fase1
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            'banks': dict(Fase2.BANK_ENUM),
        }


class Fase2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Fase2
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'institution': instance.institution,
            'concept': instance.concept,
            'value': instance.value,
            'type_card': instance.fase1.payType,
        }