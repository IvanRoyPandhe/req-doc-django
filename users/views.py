from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from .models import CustomUser

@csrf_protect   
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("User registered and logged in successfully")  # Debugging
            return redirect('dashboard')
        else:
            print("Form errors:", form.errors)  # Debugging
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:  # Jika admin, arahkan ke halaman admin
                    return redirect('/admin')
                return redirect('dashboard')  # Jika user biasa, ke dashboard
            else:
                messages.error(request, 'Username atau password salah.')
        else:
            # Jika form tidak valid, tampilkan pesan error
            for field, errors in form.errors.items():
                if field == "__all__":
                    for error in errors:
                        messages.error(request, error)  # Tampilkan pesan tanpa "__all__:"
                else:
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'users/profile.html', {'user': user})

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Setelah logout, kembali ke halaman login

def lock(request):
  return render(request, 'accounts/lock.html')

# Errors
def error_404(request):
  return render(request, 'pages/examples/404.html')

def error_500(request):
  return render(request, 'pages/examples/500.html')

# Extra
def upgrade_to_pro(request):
  return render(request, 'pages/upgrade-to-pro.html')
