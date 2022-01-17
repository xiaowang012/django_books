"""BookStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from app1 import views

urlpatterns = [
    #当路由为'' 时,表示127.0.0.1:5000
    path('', views.host),
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('home/', views.home),
    path('home/page/', views.home_page),
    path('home/search/page', views.search_book),
    # path('home/search/page', views.search_book_page),
    path('management/', views.management),
    path('register/', views.register),
    path('logout/', views.logout),
    path('add_book/', views.add_book),
    path('download/<book_file_name>/', views.download_book),
    path('add_users/', views.add_users),
    path('download_excel/', views.download_excel),    
]
