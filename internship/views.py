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
from public.models import Users,Student
from internship.serializers import *
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
                        'Message' : 'Form completed',
                    },
                    status=status.HTTP_200_OK
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
                        'message': 'Credits Edited successfuly',
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
                req.reqhash = req.student.user.first_name + " " + req.student.user.last_name+" "+str(req.reqdate)
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
    def get(self, request):
        opi=Request.objects.filter(state=4)


    def post(self, request):
        serializer = SignUpInternShipSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                'Message' : 'Account Create,Welcome',
            },
            status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class CheckRequestView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self,request,userparameter):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            for r in request.user.roles.all():

                if str(r) == 'FacultyTrainingStaff':
                    opinion = Opinion.objects.filter(request__state=1)
                elif str(r) == 'DepartmentHead':
                    # opinion = Opinion.objects.filter(Q(user__roles__role='FacultyTrainingStaff') & Q(request__state__iexact=2))
                    opinion = Opinion.objects.filter(Q(user__roles__role='DepartmentHead') & Q(request__state=2)& (Q(user__roles__department__departmentName=r.department.all()[0])))
                    # opinion = Opinion.objects.filter(Q(request=request))
                elif str(r) == 'UniversityTrainingStaff':
                    opinion = Opinion.objects.filter(Q(user__roles__role='UniversityTrainingStaff') & Q(request__state=3))

        # except:
        #     return Response(
        #         {
        #             'message' : 'InAccessibility !!!'
        #         },
        #         status=status.HTTP_403_FORBIDDEN
        #     )

            opinion_serializer = OpinionGetFilterSerializer(data=request.GET) #data=request.data
            if opinion_serializer.is_valid():

                if 'first_name' in opinion_serializer.data:
                    opinion = opinion.filter(
                        request__student__user__first_name=opinion_serializer.data['first_name']
                    )
                if 'last_name' in opinion_serializer.data:
                    opinion = opinion.filter(
                        request__student__user__last_name=opinion_serializer.data['last_name']
                    )
                if 'username' in opinion_serializer.data:
                    opinion = opinion.filter(
                        request__student__user__username=opinion_serializer.data['username']
                    )
                if 'title' in opinion_serializer.data:
                    opinion = opinion.filter(
                        request__title=opinion_serializer.data['title']
                    )

                serializer = OpinionSerializer(instance=opinion,many=True)
                for op in opinion:
                    if op.seenDate is None:
                        op.seenDate=timezone.now()
                        op.save()


                return Response(
                    {
                        'data' : serializer.data
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


    def put(self, request, userparameter):

        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            try:
                opinion = Opinion.objects.get(Q(request = request.data['id']) & Q(user=request.user))
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



    # def put(self, request, userparameter):
    #     users = Users.objects.all()
    #
    #     try:
    #         opinion = Opinion.objects.get( Q(request = int(userparameter)) & Q(user=request.user))
    #         serializer = OpinionEditSerializer(instance=opinion,data=request.data)
    #
    #     except ValueError:
    #         print("there is no userparameters")
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             {
    #             'message': 'Your Opinion Was Recorded Successfuly',
    #             },
    #             status=status.HTTP_200_OK
    #         )
    #     else:
    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
