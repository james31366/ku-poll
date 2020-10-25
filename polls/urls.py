"""This script is use to handle the url of the KU Polls web application.

Author: Vichisorn Wejsupakul
Date: 10/9/2020
"""
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', login_required(views.DetailView.as_view(), login_url='polls:login'), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', login_required(views.vote, login_url='polls:login'), name='vote'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register')
]
