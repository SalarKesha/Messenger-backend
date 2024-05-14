from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        if hasattr(request.resolver_match.func.cls, 'permission_classes'):
            view_class = request.resolver_match.func.cls
            permissions = getattr(view_class, 'permission_classes', [])
            if IsAuthenticated in permissions:
                return super().authenticate(request)
        return None
