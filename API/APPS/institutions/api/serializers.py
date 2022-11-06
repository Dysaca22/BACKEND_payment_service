from rest_framework import serializers
from APPS.institutions.models import Service, Institution, Student, StudentService
from APPS.users.models import User


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Student
        fields = '__all__'


class StudentUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    lastName = serializers.CharField(max_length=255)
    institution = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'lastName': instance.lastName,
            'intitution': instance.institution.name,
            'username': instance.user.username,
            'email': instance.user.email,
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('El tamaño de la contraseña debe ser mayor o igual a 8.')

    def validate_institution(self, value):
        institution = Institution.objects.filter(pk=value).first()
        if not institution:
            raise serializers.ValidationError('EL id de la institución no existe en los registros.')
        return institution

    def create(self, validated_data):
        data_user = {
            'username': validated_data['name'][0:2].lower() + validated_data['lastName'].split(' ')[0].capitalize(),
            'email': validated_data['email'],
            'password': validated_data['password'],
        }
        user = User.objects.create_user(**data_user)
        data_user = {
            'name': validated_data['name'],
            'lastName': validated_data['lastName'],
            'institution': validated_data['institution'],
            'user': user,
        }
        return Student.objects.create(**data_user)


class StudentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentService
        fields = '__all__'