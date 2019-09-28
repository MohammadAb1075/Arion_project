import string
import random
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from Arion.utils import CsrfExemptSessionAuthentication
from public.models import Users,Student
from public.serializers import *
from . import newpass



class SignUpView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        serializer = SignUpSerializer(data = request.data)

        # serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                'Message' : 'Account Create',
                # 'data'  : serializer.data
            },
            status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
 

class SignUpStudentView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        serializer = SignUpStudentSerializer(
            data = request.data,
            context = {
                'user' : request.user
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                'Message' : 'The Account Creation Process completed',
                # 'data'  : serializer.data
            },
            status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )




class SignIn(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        serial = RequestSigninSerializer(data=request.data)
        if serial.is_valid():
            user = authenticate(
                request,
                username=serial.data['username'],
                password=serial.data['password'])

            if user is None:
                    return Response(
                        {
                            'message': 'There is not any account with this username'
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )

            login(request, user)
            return Response(
                {
                    'message': 'Your account info is correct',
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
             serial.errors,
             status=status.HTTP_400_BAD_REQUEST
            )


class EditProfile(APIView):
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
            information = Student.objects.get(user = request.user)
            serializer = StudentInformationSerializer(instance=information)
            # serializer = StudentInformationSerializer(instance=information,many=True)
            return Response(
                {
                    'data' : serializer.data
                },
                status=status.HTTP_200_OK
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
            information = Student.objects.get(user = request.user)
            serializer = EditProfileSerializer(instance=information,data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        'message': 'your account have been Edited successfuly',
                        'data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class RequestForgetEmail(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request):

        serializer = ForgetEmailSerializer(data=request.data) #request.POST['email']
        if serializer.is_valid():
            try:
                user = Users.objects.get(username=serializer.data['username'])
            except ObjectDoesNotExist:
                return Response(
                    {
                        'message': 'There is not any account with this username'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            newpassword = newpass.get_code(10)
            send_mail('New Password', 'This is Your New Password : {}'.format(newpassword),'utfarabi@gmail.com', user.username.split())
            user.set_password(newpassword)
            user.save()

            return Response(
                {
                    'message':'A New Email Sended successfuly!!!'
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response(
             serializer.errors,
             status=status.HTTP_400_BAD_REQUEST
            )



class LogOutView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        else:
            request.session.flush()
            request.user = AnonymousUser()
            return Response(
                {
                    'message': 'Your account info is correct',
                },
                status=status.HTTP_200_OK
            )
