from django.urls import path

from account.views import UserRetrieveAPI, UserCreateAPI, UserUpdateAPI, UserExploreAPI

urlpatterns = [
    path('me/', UserRetrieveAPI.as_view(), name='me'),
    path('create/', UserCreateAPI.as_view(), name='user_create'),
    path('<int:user_id>/update/', UserUpdateAPI.as_view(), name='user_update'),
    path('explore/', UserExploreAPI.as_view(), name='user_explore_list'),
]
