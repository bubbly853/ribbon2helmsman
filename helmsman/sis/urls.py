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
    path('create_person/', views.person_create, name='person_create'),
    path('sections/<str:section_stid>/', views.section_detail, name='section_detail'),
    path('create_enrollment/student/', views.student_list, name='enrollment_create_student_select'),
    path('create_enrollment/student/<str:student_id>', views.enrollment_create_term_select, name='enrollment_create_term_select'),
    path('create_enrollment/enroll/<str:student_term_tsid>', views.enrollment_create, name='enrollment_create'),
    path('create_student/', views.person_list, name='student_create_person_select'),
    path('create_student/<str:person_rbid>', views.student_create_term_select, name='student_create_term_select'),
    path('enter_marks/', views.section_list, name='marks_enter_section_select'),
    path('enter_marks/<str:section_stid>', views.marks_enter, name='marks_enter'),
    path('curriculums/', views.curriculum_list, name='curriculum_list'),
    path('curriculums/<str:curriculum_cvid>', views.curriculum_detail, name='curriculum_detail'),
    path('audit/student/', views.student_list, name='curriculum_audit_student_select'),
    path('audit/student/<str:student_id>', views.curriculum_audit_curriculum_select, name='curriculum_audit_curriculum_select'),
    path('audit/view/<str:stucv_scid>', views.curriculum_audit, name='curriculum_audit'),
]
