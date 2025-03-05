from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('step1/', views.request_step1, name='request_step1'),
    path('step2/', views.request_step2, name='request_step2'),
    path('step3/', views.request_step3, name='request_step3'),
    path('review/', views.request_review, name='request_review'),
    path('success/', views.request_success, name='request_success'),
]