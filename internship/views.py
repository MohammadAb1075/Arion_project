import hashlib
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from Arion.utils import CsrfExemptSessionAuthentication
from internship.serializers import *
from public.models import Users,Student
from public.serializers import *




class RequestInternShipView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            ###Show Student Information
            student = Student.objects.get(user = request.user)
            serializer = StudentInformationSerializer(instance=student)

            if student.credits < 80 :
                return Response(
                        {
                            'message' : 'Credits Error',

                            'data' : serializer.data
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )

            return Response(
                {
                    'data' : serializer.data
                },
                status=status.HTTP_200_OK
            )

    def post(self,request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            # student = Student.objects.get(user = request.user)
            student = Student.objects.filter(user = request.user)[0]
            serializer = RequestFormInternShipSerializer(
                data=request.data,
                context={
                    'student'  : student
                    }
            )

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'Message' : 'Form Completed',
                    },
                    status=status.HTTP_201_CREATED
                    )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_403_FORBIDDEN
                )

    def put(self,request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            editcredit = Student.objects.get(user = request.user)
            serializer = EditCreditsSerializer(instance=editcredit,data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        'message': 'Credits Edited Successfuly',
                        'data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class RequestFlowView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self,request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            student = Student.objects.get(user = request.user)
            opinion = Opinion.objects.filter(request__student=student)
        except:
            return Response(
                {
                    'message' : 'InAccessibility !!!'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RequestFlowSerializer(instance=opinion,many=True)

        try:
            req = Request.objects.get(student = student)
            if req.state == 4 :
                req.reqhash = req.student.user.first_name + " " + req.student.user.last_name + " " + str(req.reqdate)
                req.reqhash = hashlib.md5(req.reqhash.encode()).hexdigest()
                req.save()
                return Response(
                    {
                        'message' : 'The Approval Process Has Been Completed Successfully',

                        'data' : serializer.data
                    },
                    status=status.HTTP_200_OK
                )
        except:
            pass

        return Response(
            {
                'data' : serializer.data
            },
            status=status.HTTP_200_OK
        )


class CreateAccountInternshipHeadView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request, userparameter):
        try:
            request=Request.objects.get(reqhash = userparameter)
            serializer=RequestSerializer(instance = request)
            return Response(
                {
                    'data' : serializer.data,
                    'Message' : 'If this Information Is Correct, Create Your Account'
                    },
                status=status.HTTP_200_OK
                )
        except:
            return Response(
                {
                    'Message' : 'The Hash Expression May Be Incorrect'
                    },
                status=status.HTTP_404_NOT_FOUND
                )

    def post(self, request, userparameter):
        req=Request.objects.get(reqhash = userparameter)
        serializer = SignUpInternShipSerializer(
            data = request.data,
            context = {
                'request' : req
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                'Message' : 'Account Create, Welcome',
            },
            status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class InternshipFlow(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self,request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


        try:
            request = Request.objects.get(student__user = request.user)
            try:
                guideTeacher = Choosing.objects.get(student__user = request.user)
            except:
                try:
                    confirmation = request.internshiphead
                    serializer = InternshipHeadInformation(instance=confirmation)
                except:
                    return Response(
                        {
                            'data1' : 'Error1',
                        }
                    )

                return Response(
                    {
                        'data1' : serializer.data,
                        'data2' : 'Guide Teacher Not Selected Yet',
                    }
                )
            serializer = InternshipHeadInformation(instance=confirmation)
            serial = ChoosingSerializer(instance = guideTeacher)
            return Response(
                {
                    'data1' : serializer.data,
                    'data2' : serial.data
                }
            )



        except:
            return Response(
                {
                    'message' : 'InAccessibility !!!'
                },
                status=status.HTTP_403_FORBIDDEN
            )




class CheckRequestView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self,request,requestparameter):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            for r in request.user.roles.all():
                internshiphead = ""
                opinion = Opinion.objects

                if str(r) == 'FacultyTrainingStaff':
                    opinion = Opinion.objects.filter(request__state=1)


                elif str(r) == 'DepartmentHead':
                    opinion = Opinion.objects.filter(
                        Q(user__roles__role=str(r)) &
                        Q(request__state=2) &
                        Q(user__roles__department__departmentName=r.department.all()[0]))

                    internshiphead = InternshipHead.objects.filter(
                        Q(request__state=5) &
                        Q(user__roles__department__departmentName=r.department.all()[0]))


                elif str(r) == 'UniversityTrainingStaff':
                    opinion = Opinion.objects.filter(
                        Q(user__roles__role=str(r)) &
                        Q(request__state=3))


            filter_serializer = InformationGetFilterSerializer(data=request.GET)
            if filter_serializer.is_valid():
                if 'first_name' in filter_serializer.data:
                    opinion = opinion.filter(
                        request__student__user__first_name=filter_serializer.data['first_name'])
                    internshiphead = InternshipHead.objects.filter(
                        Q(user__first_name=filter_serializer.data['first_name']) |
                        Q(request__student__user__first_name=filter_serializer.data['first_name']))

                if 'last_name' in filter_serializer.data:
                    opinion = opinion.filter(
                        request__student__user__last_name=filter_serializer.data['last_name'])

                    internshiphead = InternshipHead.objects.filter(
                        Q(user__last_name=filter_serializer.data['last_name']) |
                        Q(request__student__user__last_name=filter_serializer.data['last_name']))

                if 'username' in filter_serializer.data:
                    opinion = opinion.filter(
                        request__student__user__username=filter_serializer.data['username'])

                    internshiphead = InternshipHead.objects.filter(
                        Q(user__username=filter_serializer.data['username']) |
                        Q(request__student__user__username=filter_serializer.data['username']))

                if 'title' in filter_serializer.data:
                    opinion = opinion.filter(
                        request__title=filter_serializer.data['title'])

                    internshiphead = InternshipHead.objects.filter(
                        request__title=filter_serializer.data['title'])



                serializer = OpinionSerializer(instance=opinion,many=True)
                serial = InternshipHeadInformation(instance=internshiphead,many=True)
                for op in opinion:
                    if op.seenDate is None:
                        op.seenDate=timezone.now()
                        op.save()


                return Response(
                    {
                        'data1' : serializer.data,
                        'data2' : serial.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    opinion_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        except:
            return Response(
                {
                    'message' : 'InAccessibility !!!'
                },
                status=status.HTTP_403_FORBIDDEN
            )


    def put(self,request,requestparameter):

        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            try:
                opinion = Opinion.objects.get(
                    Q(request = requestparameter) &
                    Q(user = request.user))
                serializer = OpinionEditSerializer(instance=opinion,data=request.data)
            except:
                return Response(
                    {
                    'message': 'You Can''t comment'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                    'message': 'Your Opinion Was Recorded Successfuly',
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

class ChoiceGuideTeacherView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request,requestparameter,teacherparameter):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        req = Request.objects.get(id=requestparameter)
        role = Role.objects.get(
            Q(role='DepartmentHead') &
            Q(department__departmentName=req.student.major))

        if role not in request.user.roles.all():
            return Response(
                {
                    'message' : 'InAccessibility !!!'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        teachers = Users.objects.filter(
            Q(roles__role='Teacher') &
            Q(roles__department__departmentName=req.student.major))

        serializer = TeacherInformation(instance = teachers,many=True)

        return Response(
            {
                'data' : serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request,requestparameter,teacherparameter):

        teacher = Users.objects.get(id=teacherparameter)
        req = Request.objects.get(id=requestparameter)
        serializer = ChoosingGuideTeacherSerializer(
            data = request.data,
            context = {
                'request' : req,
                'teacher' : teacher
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                'Message' : 'Account Create, Welcome',
            },
            status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
