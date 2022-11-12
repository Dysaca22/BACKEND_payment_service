from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from APPS.users.models import User
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': [validators.UniqueValidator(
                get_user_model().objects.all(), "email already exists"
                )]}}
        def create(self, validated_data):
            user = get_user_model().objects.create_user(**validated_data)
            return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'username': instance.username,
            'email': instance.email,
            'password': instance.password,
        }