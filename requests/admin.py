from django.contrib import admin
from .models import Request, Attachment

class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'type', 'status', 'date_submitted', 'priority')
    list_filter = ('status', 'priority', 'type')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'type', 'status', 'description', 'priority', 'assigned_to', 'deadline', 'additional_notes')
        }),
        ('Admin Section', {
            'fields': ('fileadmin', 'deskripsiadmin'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('date_submitted',)  # Tambahkan ini

admin.site.register(Request, RequestAdmin)
admin.site.register(Attachment)