from django.urls import path

from call.views import UserCallListAPI, CallRetrieveAPI

urlpatterns = [
    path('list/', UserCallListAPI.as_view(), name='calls_list'),
    path('<int:call_id>/', CallRetrieveAPI.as_view(), name='call'),
]
