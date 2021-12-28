"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from webapp import views

urlpatterns = [
    path('', views.index),
    path('accounts/', views.accounts_list),
    path('accounts/<str:id_>/', views.account_detail,name = 'account_detail'),
    path('api/accounts/', views.accounts),
    path('createacc/', views.create_account),
    path('postacc/', views.post_account, name = 'post_account'),
    path('posttr/', views.post_trs, name = 'post_trs'),
]
