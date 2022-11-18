from rest_framework import serializers
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

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name + ' ' + instance.lastname,
            'provider': instance.phase1.connection_with_provider.provider,
            'concept': instance.phase1.connection_with_provider.concept,
            'amount': instance.phase1.connection_with_provider.amount,
        }