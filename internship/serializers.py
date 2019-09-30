import re
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from public.models import *
from internship.models import *



class CollogeInformation(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'


class FacultyInformation(serializers.ModelSerializer):
    college = CollogeInformation()
    class Meta:
        model = Faculties
        fields = '__all__'

class DepartmentInformation(serializers.ModelSerializer):
    faculty = FacultyInformation()
    class Meta:
        model = Department
        fields = '__all__'

class RoleInformation(serializers.ModelSerializer):
    department = DepartmentInformation(many=True)
    class Meta:
        model = Role
        fields = '__all__'

class UsreInformation(serializers.ModelSerializer):
    roles = RoleInformation(many=True)
    class Meta:
        model = Users
        fields = ['first_name','last_name','username','date_joined','roles','last_login']

class MajorInformation(serializers.ModelSerializer):
    faculty = FacultyInformation()
    class Meta:
        model = Major
        fields = '__all__'


class StudentInformationSerializer(serializers.ModelSerializer):
    user = UsreInformation()
    major = MajorInformation()
    class Meta:
        model = Student
        fields = '__all__'








class StateInformation(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class CityInformation(serializers.ModelSerializer):
    state = StateInformation()
    class Meta:
        model = City
        fields = '__all__'

class InternShipPlaceInformation(serializers.ModelSerializer):
    city = CityInformation()
    class Meta:
        model = InternShipPlace
        fields = '__all__'

class RequestInformationGETSerializer(serializers.ModelSerializer):
    internshipPlace = InternShipPlaceInformation()
    student = StudentInformationSerializer()
    class Meta:
        model = Request
        fields = '__all__'







class RequestFormInternShipSerializer(serializers.Serializer):
    nameplace = serializers.CharField()
    city = serializers.IntegerField(min_value=1)
    address = serializers.CharField()
    phone = serializers.CharField(max_length=15)
    internShipWebSite = serializers.CharField(required=False)
    term = serializers.CharField()
    title = serializers.CharField(required=False,allow_blank=True)
    state = serializers.IntegerField(required=False)
    reqdate = serializers.DateTimeField(required=False)


    def validate(self, data):
        x1 = re.findall("[a-z]", data['phone'])
        if x1 != []:

            raise serializers.ValidationError(
                'The Phone Number Should Only Be In Number !!!'
            )
        if self.context['student'].credits < 80 :
            raise serializers.ValidationError(
                'Credits Error'
            )
        return data


    def create(self, data):

        ct=City.objects.get(id=data['city'])

        isp=InternShipPlace(
            city = ct,
            nameplace = data['nameplace'],
            address = data ['address']  ,
            phone = data['phone']
        )
        if 'internShipWebSite' in data:
            form.internShipWebSite = data['internShipWebSite']
        isp.save()


        request=Request.objects.create(
            student = self.context['student'],
            internshipPlace = isp,
            title = 'InternShip',
            term = data['term'],
            reqdate = timezone.now(),
            state = 1,
        )
        ################################reqhash = hash(self.context['student'].user.username+reqdate)#########################
        request.save()

        if 'comment' in data:
            request.comment = data['comment']

        r=Role.objects.get(role='FacultyTrainingStaff')
        u=Users.objects.get(roles=r)

        try:
            opinion=Opinion(
                user = u,
                request = request,
            )
            opinion.save()

        except:
            request.delete()
            isp.delete()
            raise serializers.ValidationError(
                'Error!!!'
            )

        return request



class EditCreditsSerializer(serializers.Serializer):
    credits  = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        if 'credits' in  validated_data:
            instance.credits  = validated_data['credits']

        instance.save()
        return  instance




class OpinionSerializers(serializers.ModelSerializer):
    request = RequestInformationGETSerializer()
    class Meta:
        model = Opinion
        exclude=['user']



class InformationGetFilterSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        required=False, allow_blank=False, max_length=100)
    last_name = serializers.CharField(
        required=False, allow_blank=False, max_length=100)
    username = serializers.CharField(
        required=False, allow_blank=False, max_length=100)
    title = serializers.CharField(
        required=False, allow_blank=False, max_length=100)



class OpinionEditSerializer(serializers.Serializer):
    seenDate = serializers.DateTimeField(required=False)
    opinionDate = serializers.DateTimeField(required=False)
    opinionText = serializers.CharField(required=False,allow_blank=True)
    opinion = serializers.BooleanField(required=True)


    def validate(self, data):
        if data['opinion'] is None:
                    raise serializers.ValidationError(
                        "Opinion Is Empty!!!"
                    )

        for r in self.instance.user.roles.all():
            r=str(r)
            try:

                if (r == 'FacultyTrainingStaff' and self.instance.request.state != 1) :
                    op=Opinion.objects.get(
                        Q(user__roles__role='DepartmentHead') &
                        Q(request__student=self.instance.request.student))

                    if op:
                        if op.opinionDate:
                            raise serializers.ValidationError(
                                "You Can Not Comment"
                            )

                if (r == 'DepartmentHead' and self.instance.request.state != 2):
                    op=Opinion.objects.get(
                        Q(user__roles__role='UniversityTrainingStaff') &
                        Q(request__student=self.instance.request.student))

                    if op:
                        if op.opinionDate:
                            raise serializers.ValidationError(
                                "You Can Not Comment"
                            )

                if (r == 'UniversityTrainingStaff' and self.instance.request.state != 3):
                    raise serializers.ValidationError(
                        "You Can Not Comment"
                    )

            except:
                pass

        return data


    def update(self,instance,validated_data):
        if  'opinion' in  validated_data:

            if validated_data['opinion'] == 1 :

                if instance.request.state == 1 :
                    u=Users.objects.get(roles__role='FacultyTrainingStaff')

                    if instance.user == u:
                        instance.request.state += 1
                        instance.request.save()

                if instance.request.state == 2:
                    u=Users.objects.get(
                        Q(roles__role='DepartmentHead') &
                        Q(roles__department__departmentName=instance.request.student.major))

                    if instance.user == u:
                        instance.request.state += 1
                        instance.request.save()
                    if not  Opinion.objects.filter(Q(user=u) & Q(request=instance.request)):
                        op=Opinion(
                            user = u,
                            request = instance.request,
                        )
                        op.save()


                if instance.request.state == 3:
                    u=Users.objects.get(
                        Q(roles__role='UniversityTrainingStaff') &
                        Q(roles__department__departmentName=instance.request.student.major))

                    if instance.user == u:
                        instance.request.state += 1
                        instance.request.save()
                    if not  Opinion.objects.filter(Q(user=u) & Q(request=instance.request)):
                        op=Opinion(
                            user = u,
                            request = instance.request,
                        )
                        op.save()


                # if instance.request.state == 5:
                #     u=Users.objects.get(
                #         Q(roles__role='DepartmentHead') &
                #         Q(roles__department__departmentName=instance.request.student.major))
                #     instance.request.state += 1
                #     instance.request.save()
                #
                #     if not  Opinion.objects.filter(Q(user=u) & Q(request=instance.request)):
                #         op=Opinion(
                #             user = u,
                #             request = instance.request,
                #         )
                #         op.save()


                instance.opinion = 1
                instance.save()

            else:

                instance.request.state = 0
                instance.request.save()

        if  'opinionText' in  validated_data:
            instance.opinionText = validated_data['opinionText']


        instance.opinionDate = timezone.now()
        instance.save()
        return instance




class RoleInformationFlowSerializer(serializers.ModelSerializer):
    # department = DepartmentInformation(many=True)
    class Meta:
        model = Role
        fields = ['role']

class UsreInformationFlowSerializer(serializers.ModelSerializer):
    roles = RoleInformationFlowSerializer(many=True)
    class Meta:
        model = Users
        fields = ['roles']

class RequestInformationGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['title','state','reqdate']

class RequestFlowSerializer(serializers.ModelSerializer):
    user = UsreInformationFlowSerializer()
    request = RequestInformationGETSerializer()
    class Meta:
        model=Opinion
        fields='__all__'





class RequestSerializer(serializers.ModelSerializer):
    internshipPlace = InternShipPlaceInformation()
    student = StudentInformationSerializer()
    class Meta:
        model = Request
        fields = '__all__'

class OpinionSerializer(serializers.ModelSerializer):
    # user = UsreInformationFlowSerializer()
    request = RequestSerializer()
    class Meta:
        model = Opinion
        # fields = '__all__'
        exclude = ['user']



class SignUpInternShipSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=31)
    last_name = serializers.CharField(max_length=31)
    username = serializers.EmailField(max_length=31)
    password = serializers.CharField(max_length=31)
    phone = serializers.CharField(required=True, max_length=15)
    email = serializers.EmailField(required=False, allow_blank=True)

    def create(self, data):
        u = Users(
            first_name = data['first_name'],
            last_name = data['last_name'],
            username = data['username'],
        )
        u.save()

        try:
            request=self.context['request']
            u.roles.add(Role.objects.get(
                Q(role='InternshipHead') &
                Q(department__departmentName=request.student.major)))

            u.set_password(data['password'])
            u.save()
            ih = InternshipHead(
                user = u,
                request = self.context['request']
            )
            if 'email' in data:
                ih.email = data['email']
            ih.save()

        except:
            u.delete()

        return ih

        # try:
        #     request=self.context['request']
        #     u.roles.add(Role.objects.get(
        #         Q(role='InternshipHead') &
        #         Q(department__departmentName=request.student.major)))
        #
        #     u.set_password(data['password'])
        #     u.save()
        #     ih = InternshipHead(
        #         user = u,
        #         request = self.context['request']
        #     )
        #     if 'email' in data:
        #         ih.email = data['email']
        #     ih.save()
        #
        #     request.state = 5
        #     request.save()
        #     usr=Users.objects.get(
        #         Q(roles__role='DepartmentHead') &
        #         Q(roles__department__departmentName=request.student.major))
        #     op=Opinion(
        #         user = usr,
        #         request = request
        #     ).save()
        #
        # except:
        #     u.delete()
        #
        # return ih


class InternshipHeadInformation(serializers.ModelSerializer):
    user = UsreInformation()
    request = RequestSerializer()
    class Meta:
        model = InternshipHead
        fields = '__all__'


class ChoosingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choosing
        fields = '__all__'


class DepartmentOfTeacherInformation(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ['faculty']


class RoleOfTeacherInformation(serializers.ModelSerializer):
    department = DepartmentOfTeacherInformation(many=True)
    class Meta:
        model = Role
        fields = '__all__'

class TeacherInformation(serializers.ModelSerializer):
    roles = RoleOfTeacherInformation(many=True)
    class Meta:
        model = Users
        fields = ['id','first_name','last_name','username','roles']



class ChoosingGuideTeacherSerializer(serializers.ModelSerializer):
    choice = serializers.BooleanField(required=False)


    def create(self, data):
        ch = Choosing(
            user =  self.context['teacher'],
            student =  self.context['request'].student
        )
