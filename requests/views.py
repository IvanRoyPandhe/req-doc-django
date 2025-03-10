from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Request, Attachment
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage

@login_required
def dashboard(request):
    # Ambil parameter dari URL
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    sort_order = request.GET.get('sort', 'dateDesc')

    # Filter data berdasarkan parameter
    requests = Request.objects.filter(user=request.user)

    if search_query:
        requests = requests.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query))
    
    if status_filter != 'all':
        requests = requests.filter(status=status_filter)

    # Urutkan data
    if sort_order == 'dateAsc':
        requests = requests.order_by('date_submitted')
    else:
        requests = requests.order_by('-date_submitted')

    # Hitung statistik
    stats = {
        'total': Request.objects.filter(user=request.user).count(),
        'pending': Request.objects.filter(user=request.user, status='Pending').count(),
        'approved': Request.objects.filter(user=request.user, status='Approved').count(),
        'rejected': Request.objects.filter(user=request.user, status='Rejected').count(),
    }

    return render(request, 'dashboard.html', {
        'requests': requests,
        'stats': stats,
        'search_query': search_query,
        'status_filter': status_filter,
        'sort_order': sort_order,
    })

@login_required
def request_step1(request):
    if request.method == 'POST':
        # Save document type to session
        request.session['document_type'] = request.POST.get('document_type')
        return redirect('request_step2')
    return render(request, 'step1.html')

@login_required
def request_step2(request):
    if request.method == 'POST':
        # Save title, description, and priority to session
        request.session['title'] = request.POST.get('title')
        request.session['description'] = request.POST.get('description')
        request.session['priority'] = request.POST.get('priority')
        return redirect('request_step3')
    return render(request, 'step2.html')

@login_required
def request_step3(request):
    if request.method == 'POST':
        # Save deadline, additional_notes, and file to session
        request.session['deadline'] = request.POST.get('deadline')
        request.session['additional_notes'] = request.POST.get('additional_notes')
        if 'file' in request.FILES:
            file = request.FILES['file']
            file_name = default_storage.save(f'attachments/{file.name}', file)
            request.session['file'] = file_name
        return redirect('request_review')
    return render(request, 'step3.html')

@login_required
def request_review(request):
    if request.method == 'POST':
        try:
            # Ambil data dari session
            title = request.session.get('title')
            document_type = request.session.get('document_type')
            description = request.session.get('description')
            priority = request.session.get('priority')
            deadline = request.session.get('deadline')
            additional_notes = request.session.get('additional_notes')
            file = request.session.get('file')

            # Validasi deadline
            if deadline == '':
                deadline = None  # Set ke None jika kosong

            # Buat objek Request
            new_request = Request(
                user=request.user,
                title=title,
                type=document_type,
                description=description,
                priority=priority,
                deadline=deadline,
                additional_notes=additional_notes,
            )
            new_request.full_clean()  # Validasi model
            new_request.save()

            # Simpan file jika ada
            if file:
                attachment = Attachment(
                    request=new_request,
                    file=file,
                )
                attachment.save()

            # Hapus data session
            for key in ['title', 'document_type', 'description', 'priority', 'deadline', 'additional_notes', 'file']:
                if key in request.session:
                    del request.session[key]

            return redirect('request_success')

        except ValidationError as e:
            # Tangani error validasi
            return render(request, 'step4.html', {'error': e.messages})

    return render(request, 'step4.html')

@login_required
def request_success(request):
    return render(request, 'success.html')

@login_required
def request_detail(request, request_id):
    request_detail = get_object_or_404(Request, id=request_id, user=request.user)
    return render(request, 'request_detail.html', {'request': request_detail})

def request_notifications(request):
    if request.user.is_staff:
        new_requests_count = Request.objects.filter(status='Pending').count()
        print(f"New Requests Count: {new_requests_count}")  # Debugging
        return {'new_requests_count': new_requests_count}
    return {}