from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Restaurant

User = get_user_model()

admin.site.register(Restaurant)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'first_name', 'last_name', 'is_owner', 'restaurant')
    ordering = ['first_name', ]
    list_editable = ('is_owner',)
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            None,
            {
                'fields': ('is_owner', 'restaurant')
            }
        ),
    )
