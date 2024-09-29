"""
URL configuration for server project.

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
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/01/', views.test01),
    path('user/register/', views.register),
    path('user/login/', views.login),
    path('user/logout/', views.logout),
    path('user/token/add/', views.token_add),
    path('user/token/del/', views.token_del),
    path('user/token/list/', views.token_list),
    path('user/components/add/', views.components_add),
    path('user/components/del/', views.components_del),
    path('user/components/list/', views.components_list),
]
