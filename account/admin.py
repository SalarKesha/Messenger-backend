from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from account.models import UserModel
from django.utils.translation import gettext_lazy as _


@register(UserModel)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'is_active', 'status')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'image')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined')
