from django.contrib import admin
from .models import Request, Attachment

class AttachmentInline(admin.TabularInline):  # atau admin.StackedInline untuk tampilan yang lebih detail
    model = Attachment
    extra = 1  # Jumlah form kosong yang ditampilkan

class RequestAdmin(admin.ModelAdmin):
    # Tampilan daftar request
    list_display = ('title', 'user', 'type', 'status', 'priority', 'date_submitted', 'deadline')
    list_filter = ('status', 'priority', 'type', 'date_submitted')  # Filter di sidebar
    search_fields = ('title', 'user__username', 'description')  # Pencarian berdasarkan field
    ordering = ('-date_submitted',)  # Urutan data (terbaru pertama)
    date_hierarchy = 'date_submitted'  # Navigasi berdasarkan tanggal

    # Tampilan detail request
    fieldsets = (
        (None, {'fields': ('user', 'title', 'type', 'description')}),
        ('Status & Priority', {'fields': ('status', 'priority', 'deadline')}),
        ('Additional Info', {'fields': ('additional_notes', 'fileadmin', 'deskripsiadmin')}),
    )

    # Inline untuk Attachment
    inlines = [AttachmentInline]

    # Action kustom untuk mengubah status
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        queryset.update(status='Approved')
    approve_requests.short_description = "Approve selected requests"

    def reject_requests(self, request, queryset):
        queryset.update(status='Rejected')
    reject_requests.short_description = "Reject selected requests"

# Daftarkan model dan admin kustom
admin.site.register(Request, RequestAdmin)

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('request', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('request__title', 'file')
    date_hierarchy = 'uploaded_at'

admin.site.register(Attachment, AttachmentAdmin)