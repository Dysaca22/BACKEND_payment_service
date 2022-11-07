from rest_framework import serializers
from APPS.institutions.models import Institution, Campus, Service, Program, Semester, Student, Bill
from APPS.users.models import User


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


class CreationStudenUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    lastName = serializers.CharField(max_length=255)
    campus = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'lastName': instance.lastName,
            'campus': instance.campus.name,
            'username': instance.user.username,
            'email': instance.user.email,
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('El tamaño de la contraseña debe ser mayor o igual a 8.')

    def validate_campus(self, value):
        campus = Campus.objects.filter(pk=value).first()
        if not campus:
            raise serializers.ValidationError('EL id de el campus no existe en los registros.')
        return campus

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
            'campus': validated_data['campus'],
            'user': user,
        }
        return Student.objects.create(**data_user)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'type']

    
class ProgramSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = Program
        fields = ['name', 'service']


class SemesterSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    class Meta:
        model = Semester
        fields = ['year', 'period', 'value', 'program']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'lastName': instance.lastName,
            'campus': instance.campus.__str__(),
            'code': f'{instance.code[0:3]}{"*"*(len(instance.code)-3)}',
        }


class BillSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    class Meta:
        model = Bill
        fields = ['_paid', 'semester', '_expiration', '_generatedDate']


class GeneralInformationSerializer(serializers.Serializer):
    student = StudentSerializer()
    bill = BillSerializer(many=True)