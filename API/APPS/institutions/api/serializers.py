from rest_framework import serializers
from APPS.institutions.models import Institution, Campus, Student, Bill, Pay


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['name']


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['name', 'city']
    
    def to_representation(self, instance):
        return {
            'name': instance.name,
            'city': dict(Campus.CAMPUS_ENUM)[instance.city]
        }
        

class InfoInstitucionSerializer(serializers.Serializer):
    institucion = InstitutionSerializer()
    campus = CampusSerializer(many=True)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'lastName': instance.lastName,
            'code': instance.code,
            'campus': instance.campus.__str__(),
            'username': instance.user.username,
        }


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        exclude = ['student']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'semester': instance.semester.__str__(),
            'program': instance.semester.program.name,
            'service': f'{instance.semester.program.service.name} - {instance.semester.program.service.getType}',
            'value': instance.semester.value,
            'status': instance.getPaid,
            'issue_date': instance._generatedDate,
        }


class StudentBillsSerializer(serializers.Serializer):
    student = StudentSerializer()
    bills = BillSerializer(many=True)


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = ['student', 'bills']

    def to_representation(self, instance):
        concept = 'Pago de '
        value = 0
        for bill in instance.bills.all():
            concept += f'{bill.semester.program.service.name.lower()} {bill.semester.program.name.lower()}'
            value += bill.semester.value
            if bill != [*instance.bills.all()][-1]:
                concept += ', '
            else: 
                concept += ''
        return {
            'pay_id': instance.id,
            'institution': instance.student.campus.institution.name,
            'concept': concept,
            'value': value,
        }