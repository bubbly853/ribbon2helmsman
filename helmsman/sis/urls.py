"""
SIS URL Configuration
Place this in /srv/ribbon2helmsman/helmsman/sis/urls.py
"""

from django.urls import path
from . import views

app_name = 'sis'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/<str:student_rbid>/', views.student_detail, name='student_detail'),
    path('persons/', views.person_list, name='person_list'),
    path('persons/<str:student_rbid>/', views.person_detail, name='person_detail'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<str:course_id>/', views.course_detail, name='course_detail'),
]
