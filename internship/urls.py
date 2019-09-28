from django.urls import path, re_path
from internship.views import *

urlpatterns = [
    # path('list/', views.user_list),
    # re_path('list/(?P<id>\d{0,10})', views.conversation_view),
    path('request/',RequestInternShipView.as_view()),
    # path('checkrequest/',CheckRequestView.as_view()),
    path('requestflow/',RequestFlowView.as_view()),
    re_path('signup/internshiphead/(?P<userparameter>\w+)',CreateAccountInternshipHeadView.as_view()),
    re_path('checkrequest/(?P<userparameter>\d{0,10000000})', CheckRequestView.as_view())
]
