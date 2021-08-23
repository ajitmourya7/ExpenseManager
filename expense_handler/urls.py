"""ExpenseManager URL Configuration

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
from expense_handler import views

urlpatterns = [
    path('registration', views.user_registration, name='user.registration'),
    path('login', views.user_login, name='user.login'),
    path('create_category', views.create_category, name='user.create_category'),
    path('category_list', views.category_list, name='user.category_list'),
    path('add_expense', views.add_expense, name='user.add_expense'),
    path('view_expense', views.view_expense, name='user.view_expense'),
]
