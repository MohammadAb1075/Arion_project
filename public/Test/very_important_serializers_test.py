import re
from django.db.models import Q
# from django.db.utils import IntegrityError
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import serializers
from public.models import Users,Student,Role
from public.models import College,Faculties,Department,Major



class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=31)
    last_name = serializers.CharField(max_length=31)
    username = serializers.EmailField(max_length=31)
    password = serializers.CharField(max_length=31)
    role =  serializers.CharField(required=True, allow_blank=False, max_length=255)
    departmentName = serializers.CharField(max_length=63)

    def validate(self, data):

        if Users.objects.filter(username=data['username']):
            raise serializers.ValidationError(
                {
                    'Error' : 'This Username Has Already Been Used '
                }
            )
        items=[x for x in data['role'].split(',')]
        if len(items)>1 and 'Student' in items:
            raise serializers.ValidationError(
                {
                    'Error' : 'Student Can not Have Any Other Role !!!'
                }
            )

        # x = re.search("@ut.ac.ir", data['username'])
        # if x is None:
        #     raise serializers.ValidationError(
        #         'Username Must Be Tehran University Email!!!'
        #     )
        return data


    def create(self, data):
        u = Users(
            first_name = data['first_name'],
            last_name = data['last_name'],
            username = data['username'],
        )
        u.set_password(data['password'])
        u.save()

        # try:
        #     departments=[x for x in data['departmentName'].split(',')]
        #     for dep in departments:
        #         d=Department.objects.filter(departmentName=dep)[0]
        #
        # except:
        #     fac= Faculties.objects.get(name = 'Engineering')
        #     departments=[x for x in data['departmentName'].split(',')]
        #     for dep in departments:
        #         d=Department.objects.filter(departmentName=data['departmentName'])[0]
        #         d=Department(
        #         faculty = fac,
        #         departmentName = data['departmentName']
        #         )
        #     d.save()
        # try:
        #     d=Department.objects.filter(departmentName=data['departmentName'])[0]
        # except:
        #     fac= Faculties.objects.get(name = 'Engineering')
        #     d=Department(
        #         faculty = fac,
        #         departmentName = data['departmentName']
        #         )
        #     d.save()

        # try:
        items=[x for x in data['role'].split(',')]
        for i in items:
                departments=[x for x in data['departmentName'].split(',')]
                for dep in departments:
                    if not Department.objects.filter(departmentName=dep):
                        fac= Faculties.objects.get(name = 'Engineering')
                        d=Department(
                            faculty = fac,
                            departmentName=dep
                        )
                        d.save()
                    d=Department.objects.filter(departmentName=dep)[0]
                    try:
                        r=Role.objects.filter(Q(role=i))[0]
                        if r.role == 'DepartmentHead':
                            r.department.add(d)
                            u.roles.add(r)
                            u.save()
                            break
                        else:
                            r.department.add(d)
                    except:
                        r=Role(
                            role = i
                        )
                        r.save()
                        r.department.add(d)

                    r.save()
                    u.roles.add(r)
                    u.save()
        return u
                # except:
                #     fac= Faculties.objects.get(name = 'Engineering')
                #     d=Department(
                #         faculty = fac,
                #         departmentName = data['departmentName']
                #         )
                #     d.save()
            # else:
            #     r=Role(
            #         role=data['role']
            #     )
            #
            #     r.save()
            #     r.department.add(d)
            #     r.save()
            #     u.roles.add(r)
            #     u.save()


        # except:
        #     r=Role(
        #         role=data['role']
        #     )
        #
        #     r.save()
        #     r.department.add(d)
        #     r.save()
        #     u.roles.add(r)
        #     u.save()




        # try:
        #     d=Department.objects.filter(departmentName=data['departmentName'])[0]
        # except:
        #     fac= Faculties.objects.get(name = 'Engineering')
        #     d=Department(
        #         faculty = fac,
        #         departmentName = data['departmentName']
        #         )
        #     d.save()
        #
        # try:
        #     items=[x for x in data['role'].split(',')]
        #     for i in items:
        #         r=Role.objects.filter(Q(role=i) & Q(department=d))[0]
        #         u.roles.add(r)
        #     u.save()
        #
        # except:
        #     r=Role(
        #         role=data['role']
        #     )
        #
        #     r.save()
        #     r.department.add(d)
        #     r.save()
        #     u.roles.add(r)
        #     u.save()
        #
        # return u


        # try:
        #     d=Department.objects.filter(departmentName=data['departmentName'])[0]
        # except:
        #     fac= Faculties.objects.get(name = 'Engineering')
        #     d=Department(
        #         faculty = fac,
        #         departmentName = data['departmentName']
        #         )
        #     d.save()

        # try:
            # r=Role.objects.filter(Q(role=data['role']) & Q(department=d))[0]

        # except:
        #     r=Role(
        #         role=data['role']
        #     )
        #
        #     r.save()
        #     r.department.add(d)
        #     r.save()

        # u = Users(
        #     first_name = data['first_name'],
        #     last_name = data['last_name'],
        #     username = data['username'],
        # )
        # u.set_password(data['password'])
        # u.save()
        # u.roles.add(r)
        # u.save()
        # return u

class SignUpStudentSerializer(serializers.Serializer):
    major          = serializers.IntegerField(min_value=1)
    credits        = serializers.IntegerField(min_value=0,max_value=150)
    average        = serializers.FloatField(min_value=1,max_value=20)
    studentNumber  = serializers.CharField(max_length=9)
    phone          = serializers.CharField(max_length=11)
    nationalCode   = serializers.CharField(max_length=10)
    name           = serializers.CharField(required=False,max_length=31)

    def create(self, data):
        m = Major.objects.get(
        id = data['major'])

        s = Student(
            user          = self.context['user'],#self.context['user'],
            major         = m,
            credits       = data['credits'],
            average       = data['average'],
            studentNumber = data['studentNumber'],
            nationalCode  = data['nationalCode'],
            phone         = data['phone'],
        )
        s.save()
        return s


class RequestSigninSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, allow_blank=False, max_length=30)
    password = serializers.CharField(
        required=True, allow_blank=False, max_length=128)



class ForgetEmailSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)





class RoleInformation(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UsreInformation(serializers.ModelSerializer):
    roles = RoleInformation(many=True)
    class Meta:
        model = Users
        fields = ['first_name','last_name','username','roles']


class CollogeInformation(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

class FacultyInformation(serializers.ModelSerializer):
    college = CollogeInformation()
    class Meta:
        model = Faculties
        fields = '__all__'

class MajorInformation(serializers.ModelSerializer):
    faculty = FacultyInformation()
    class Meta:
        model = Major
        fields = '__all__'


class StudentInformationSerializer(serializers.ModelSerializer):
    user  = UsreInformation()
    major = MajorInformation()
    class Meta:
        model = Student
        fields = '__all__'




class EditProfileSerializer(serializers.Serializer):
    password = serializers.CharField(required=False)
    credits  = serializers.IntegerField(required=False)
    average  = serializers.FloatField(required=False)
    phone    = serializers.CharField(required=False)


    def update(self, instance, validated_data):

        if  'password' in  validated_data:
            instance.user.set_password(validated_data['password'])
            instance.user.save()

        if 'credits' in  validated_data:
            instance.credits  = validated_data['credits']

        if  'average' in  validated_data:
            instance.average  = validated_data['average']

        if 'phone' in validated_data:
            instance.phone  = validated_data['phone']


        instance.save()
        return  instance
