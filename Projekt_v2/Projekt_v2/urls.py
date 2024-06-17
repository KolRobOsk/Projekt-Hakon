"""
URL configuration for Kolke_Hakon_Projekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('home', views.homeview, name='homepage'),
    path('', views.homeview),
    path('admin', admin.site.urls),
    path('dodaj', views.dodaj),
    path('ksiazki', views.ksiazki, name='ksiazki'),
    path('dodajrec', views.dodajrec),
    path('dodajkat', views.dodajkat),
    path('ksiazka/<int:pk>', views.bookview.as_view(), name='szczegóły książki'),
    path('filter/<str:tytul>', views.filterview, name='filter'),
    path('rejestracja/', views.RejestracjaUzytkownikaView.as_view()),
    path('login/', auth_views.LoginView.as_view(), {'template_name': 'registration/login.html'}, name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), {'template_name': 'registration/logged_out.html'}, name = 'logout'),
]
