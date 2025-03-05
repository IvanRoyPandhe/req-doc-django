from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'bio', 'profile_picture')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)