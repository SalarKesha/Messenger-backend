from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, ListAPIView

from account.models import UserModel
from account.serializers import UserCreateSerializer, UserSerializer, UserUpdateImageSerializer, UserExploreSerializer
from private.models import PrivateChat


class ApiToken(TokenObtainPairView):
    # throttle_classes = []
    pass


# class UserRetrieveAPI(RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = UserModel.objects.all()
#
#     def get_queryset(self):
#         return self.request.user


class UserCreateAPI(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserCreateSerializer


class UserRetrieveAPI(APIView):
    permission_classes = [IsAuthenticated, ]
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateAPI(UpdateAPIView):
    lookup_url_kwarg = 'user_id'
    serializer_class = UserUpdateImageSerializer
    queryset = UserModel.objects.all()
    permission_classes = [IsAuthenticated, ]
    #  todo: ownership permission


class UserExploreAPI(ListAPIView):
    serializer_class = UserExploreSerializer
    queryset = UserModel.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.queryset.exclude(id=self.request.user.id)
        # PrivateChat.objects.exclude(owner=self.request.user | user=self.request.user)
