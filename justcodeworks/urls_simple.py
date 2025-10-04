"""
Simple URL configuration for testing templates directly
"""
from django.contrib import admin
from django.urls import path
from websites import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('home/', views.home_page, name='home_page'),
    path('about/', views.about_page, name='about_page'),
    path('portfolio/', views.portfolio_page, name='portfolio'),
    path('services/', views.services_page, name='services'),
    path('services/<str:service_slug>/', views.service_detail_page, name='service_detail'),
    path('contact/', views.contact_page, name='contact'),
    path('get-quote/', views.quote_page, name='quote'),
    path('request-quote/', views.quote_page, name='request_quote'),
]