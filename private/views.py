from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from private.models import PrivateChat, PrivateMessage
from private.serializers import PrivateChatSerializer, UserPrivateChatSerializer, PrivateMessageSerializer, \
    PrivateChatCreateSerializer


class UserPrivateChatAPI(ListAPIView):
    serializer_class = UserPrivateChatSerializer
    queryset = PrivateChat.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(Q(owner=self.request.user) | Q(user=self.request.user))


class PrivateChatAPI(RetrieveAPIView):
    serializer_class = PrivateChatSerializer
    queryset = PrivateChat.objects.all()
    lookup_url_kwarg = 'private_chat_id'
    permission_classes = [IsAuthenticated]

    # todo: membership permission


class PrivateChatCreateAPI(CreateAPIView):
    serializer_class = PrivateChatCreateSerializer
    queryset = PrivateChat.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = serializer.validated_data.get('user')
        if (not PrivateChat.objects.filter(
                Q(owner=user, user=self.request.user) | Q(owner=self.request.user, user=user))
                and user != self.request.user):
            serializer.save(owner=self.request.user)


class PrivateMessageListAPI(ListAPIView):
    serializer_class = PrivateMessageSerializer
    queryset = PrivateMessage.objects.all()
    permission_classes = [IsAuthenticated]

    # todo: membership permission

    def get_queryset(self):
        return self.queryset.filter(private_chat=self.kwargs.get('private_chat_id')).order_by('-created_time')
