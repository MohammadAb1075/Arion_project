from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt
from public.views import *
urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('signup/student/', SignUpStudentView.as_view()),
    path('signin/', csrf_exempt(SignIn.as_view())),
    path('editprofile/', EditProfile.as_view()),
    path('email/', RequestForgetEmail.as_view()),
    path('logout/', LogOutView.as_view()),
    # path('forgetpassword/', views.RequestForgetEmail.as_view()),
    ]
