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
    path('register/', views.register),
    path('logout/', views.logout),
    path('home/', views.home),
    path('home/page', views.home_page),
    path('home/search/page', views.search_book),
    path('home/search/type', views.search_by_type),
    path('book/download',views.download_book),
    path('management/user/',views.user_mgr),
    path('management/user/page',views.user_page),
    path('management/user/changegroup',views.change_group),
    path('management/user/delete',views.delete_user),
    path('management/user/addusers/',views.add_users),
    path('management/user/addusers/download/',views.download_upload_user_template),
    path('management/refresh/',views.refresh_permission),
    path('management/book/',views.book_mgr),
    path('management/book/page',views.book_page),
    path('management/book/update/',views.update_book),
    path('management/book/delete',views.delete_book),
    path('management/book/addbook/',views.add_book),
    path('management/system/', views.system_mgr),
    path('management/system/page',views.system_page),
    path('management/system/permission/add/',views.add_permission),
    path('management/system/permission/update/',views.update_permission),
    path('management/system/permission/delete',views.delete_permission),
    path('management/system/permission/upload/',views.upload_permissions),
    path('management/system/permission/upload/download',views.download_upload_permission_template),
]
