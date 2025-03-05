from django.contrib import admin
from .models import Request, Attachment

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'type', 'status', 'priority', 'date_submitted')
    list_filter = ('status', 'priority', 'type')
    search_fields = ('title', 'description')
    date_hierarchy = 'date_submitted'

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('request', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('request__title',)