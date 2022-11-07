from rest_framework import serializers
from APPS.institutions.models import Institution, Campus, Service, Program, Semester, Student, Bill, Pay


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['name', 'city']
    
    def to_representation(self, instance):
        return {
            'name': instance.name,
            'city': dict(Campus.CAMPUS_ENUM)[instance.city]
        }


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name']

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'campus': CampusSerializer(Campus.objects.filter(institution=instance.id), many=True).data,
        }


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = ['id', 'campus']

    
class ProgramSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = Program
        exclude = ['id']


class SemesterSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    class Meta:
        model = Semester
        exclude = ['id']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'lastName': instance.lastName,
            'campus': instance.campus.__str__(),
            'code': instance.code,
        }


class BillSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    class Meta:
        model = Bill
        exclude = ['student']


class GeneralInformationSerializer(serializers.Serializer):
    student = StudentSerializer()
    bill = BillSerializer(many=True)


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = '__all__'
    
    def validated_student(self, value):
        student = Student.objects.filter(pk=value)
        if not student:
            raise serializers.ValidationError('El estudiante no existe.')
        return student