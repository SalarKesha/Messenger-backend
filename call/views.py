from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from call.serializers import CallSerializer
from call.models import Call


class UserCallListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(
            Q(caller=user) | Q(callee=user)
        )


class CallRetrieveAPI(RetrieveAPIView):
    lookup_url_kwarg = 'call_id'
    permission_classes = [IsAuthenticated]
    queryset = Call.objects.all()
    serializer_class = CallSerializer
