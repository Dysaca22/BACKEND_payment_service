from rest_framework import serializers
from requests import get, post
from APPS.services.models import ConnectionWithProvider, Phase1, Phase2


class ConnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionWithProvider
        fields = '__all__'


class Phase1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Phase1
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'provider': instance.connection_with_provider.provider,
            'concept': instance.connection_with_provider.concept,
            'amount': instance.connection_with_provider.amount,
            'email': instance.email,
        }


class Phase2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Phase2
        fields = '__all__'

    def validate_bank(self, value):
        get_data = {
            'type': 'P',
            'bank': value,
        }
        response_query = get('http://localhost:8020/api/bank/service/query', data=get_data)
        if response_query:
            if response_query.json()['active']:
                return value
            raise serializers.ValidationError(f'El banco {value} tiene el servicio de pago deshabilitado.')
        raise serializers.ValidationError('Ha ocurrido un problema con el banco')

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name + ' ' + instance.lastname,
            'provider': instance.phase1.connection_with_provider.provider,
            'concept': instance.phase1.connection_with_provider.concept,
            'amount': instance.phase1.connection_with_provider.amount,
            'bank': instance.bank,
        }