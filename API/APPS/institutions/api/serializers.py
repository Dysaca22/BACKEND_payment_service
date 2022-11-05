from rest_framework import serializers
from APPS.institutions.models import Service, Institution, Student, StudentService
from APPS.users.api.serializers import UserSerializer


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
    StudentSerializer()
    UserSerializer()


class StudentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentService
        fields = '__all__'