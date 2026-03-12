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
    path('persons/<str:person_rbid>/', views.person_detail, name='person_detail'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<str:course_crid>/', views.course_detail, name='course_detail'),
    path('sections/', views.section_list, name='section_list'),
    path('create_section/', views.section_create, name='section_create'),
    path('sections/<str:section_stid>/', views.section_detail, name='section_detail'),
    path('create_enrollment/student/', views.student_list, name='enrollment_create_student_select'),
    path('create_enrollment/student/<str:student_id>', views.enrollment_create_term_select, name='enrollment_create_term_select'),
    path('create_enrollment/enroll/<str:student_term_tsid>', views.enrollment_create, name='enrollment_create'),
]
