from .models import Request  # Sesuaikan dengan model Anda

def request_notifications(request):
    if request.user.is_staff:  # Hanya untuk admin
        new_requests_count = Request.objects.filter(status='Pending').count()
        return {'new_requests_count': new_requests_count}
    return {}