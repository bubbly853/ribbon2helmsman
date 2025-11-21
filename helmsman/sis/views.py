"""
SIS Views - Banner-style pages
Place this in /srv/ribbon2helmsman/helmsman/sis/views.py
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connections
from django.core.paginator import Paginator
from .models import Student, Course, Enrollment


@login_required
def dashboard(request):
    """Main dashboard/home page"""
    context = {
        'user': request.user,
    }
    return render(request, 'sis/dashboard.html', context)


@login_required
def student_list(request):
    """List all students with search and pagination"""
    search_query = request.GET.get('search', '')
    
    # Query SIS database
    students = Student.objects.using('sis').all()
    
    if search_query:
        students = students.filter(
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(student_id__icontains=search_query)
        )
    
    students = students.order_by('last_name', 'first_name')
    
    # Pagination
    paginator = Paginator(students, 25)  # 25 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'sis/student_list.html', context)


@login_required
def student_detail(request, student_id):
    """View/edit individual student"""
    student = get_object_or_404(Student.objects.using('sis'), pk=student_id)
    enrollments = Enrollment.objects.using('sis').filter(student_id=student_id)
    
    if request.method == 'POST':
        # Handle form submission to update student
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.email = request.POST.get('email')
        student.enrollment_status = request.POST.get('enrollment_status')
        
        try:
            student.save(using='sis')
            messages.success(request, 'Student updated successfully.')
            return redirect('student_detail', student_id=student_id)
        except Exception as e:
            messages.error(request, f'Error updating student: {str(e)}')
    
    context = {
        'student': student,
        'enrollments': enrollments,
    }
    return render(request, 'sis/student_detail.html', context)


@login_required
def course_list(request):
    """List all courses"""
    search_query = request.GET.get('search', '')
    
    courses = Course.objects.using('sis').all()
    
    if search_query:
        courses = courses.filter(
            models.Q(course_code__icontains=search_query) |
            models.Q(course_name__icontains=search_query) |
            models.Q(department__icontains=search_query)
        )
    
    courses = courses.order_by('course_code')
    
    paginator = Paginator(courses, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'sis/course_list.html', context)


@login_required
def course_detail(request, course_id):
    """View/edit individual course"""
    course = get_object_or_404(Course.objects.using('sis'), pk=course_id)
    enrollments = Enrollment.objects.using('sis').filter(course_id=course_id)
    
    if request.method == 'POST':
        # Handle form submission
        course.course_name = request.POST.get('course_name')
        course.credits = request.POST.get('credits')
        course.department = request.POST.get('department')
        
        try:
            course.save(using='sis')
            messages.success(request, 'Course updated successfully.')
            return redirect('course_detail', course_id=course_id)
        except Exception as e:
            messages.error(request, f'Error updating course: {str(e)}')
    
    context = {
        'course': course,
        'enrollments': enrollments,
    }
    return render(request, 'sis/course_detail.html', context)
