from rest_framework import serializers
from APPS.banks.models import Service, DebitCard, Person, Transaction, ConnectionWithPassarella


class DebitCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitCard
        fields = '__all__'
    
    def to_representation(self, instance):
        if 'amount' in self.context:
            data = {
                'number': instance.number,
                'balance': instance.balance,
                'active': instance._isActive,
                'valid_to_pay': 'valid' if instance.balance >= self.context['amount'] else 'invalid',
            }
        else:
            data = {
                'number': instance.number,
                'balance': instance.balance,
                'active': instance._isActive,
            }
        return data


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'active': instance._status,
        }


class ConnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionWithPassarella
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'person': {
                'name': instance.name,
                'lastname': instance.lastName,
                'email': instance.email,
                'idNumber': instance.idNumber,
                'username': instance.user.username,
            },
            'cards': DebitCardSerializer(DebitCard.objects.filter(person=instance, bank=self.context['bank']), many=True).data
        }


class ConnGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionWithPassarella
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'conn_with_bank_id': instance.id,
            'provider': instance.provider,
            'concept': instance.concept,
            'amount': instance.amount,
            'cards': DebitCardSerializer(self.context['cards'], context={ 'amount':instance.amount }, many=True).data,
        }


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['process_of_pay', 'card']

    def to_representation(self, instance):
        return {
            'message': 'Transacción exitosa',
            'number_bill': instance.number_bill,
            'provider': instance.process_of_pay.provider,
            'concept': instance.process_of_pay.concept,
            'amount': instance.process_of_pay.amount,
            'date_of_transaction': instance._createdDate,
            'card': instance.card.number,
        }