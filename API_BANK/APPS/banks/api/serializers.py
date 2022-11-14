from rest_framework import serializers
from APPS.banks.models import Card, Transaction


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'number': instance.number,
        }


class TransactionPreparationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['passarellaID', 'institution', 'amount', 'concept']

    def to_representation(self, instance):
        return {
            #'document_number': self.context['person'].idNumber,
            'passarellaID': instance.passarellaID,
            'institution': instance.institution,
            'concept': instance.concept,
            'value': instance.amount,
            #'cards': CardSerializer(self.context['cards'], many=True),
        }