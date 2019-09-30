from django.urls import path, re_path
from internship.views import *

urlpatterns = [
    path('request/',RequestInternShipView.as_view()),
    path('requestflow/',RequestFlowView.as_view()),
    path('requestflow/choice/',InternshipFlow.as_view()),
    re_path('signup/internshiphead/(?P<userparameter>\w+/$)',CreateAccountInternshipHeadView.as_view()),
    re_path('checkrequest/(?P<requestparameter>\d*/$)',CheckRequestView.as_view()),
    re_path('checkrequest/(?P<requestparameter>\d+)/choice/(?P<teacherparameter>\d+)/$',ChoiceGuideTeacherView.as_view()),
]
