"""
SIS Views - Banner-style pages with campus per major support
Place this in /srv/ribbon2helmsman/helmsman/sis/views.py
"""
from django.db import models
from dataclasses import dataclass
from typing import Optional, List

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction

# Import your real models
from .models import (
    FglFyear,
    GglCitzn,
    GglCount,
    GrlRcens,
    GrlRdetl,
    GumAdinf,
    GumIdent,
    SalAvtyp,
    SarAdvrl,
    SarOvrar,
    SclCipcd,
    SclCrtyp,
    SclCurrv,
    SclDegrs,
    SclDlevl,
    SclIscdf,
    SclMajor,
    ScmStucv,
    ScrCreqs,
    ScrOvcls,
    ScrOvmrk,
    ScrPreqs,
    ScrRqgrp,
    SdlCamps,
    SdlColeg,
    SdlDepts,
    SglLevel,
    SglSmstr,
    SglStype,
    SglTerms,
    SgmStubi,
    SrbSects,
    SrhEnrol,
    SrhSterm,
    SrlCours,
    SrlEnrst,
    SrlRgtyp,
    SrlRqtyp,
    SrlSubjs,
    SthCrtrn,
    StlMarks,
    HsvStdnt,
    HgvPrson,
    HsvActcr,
    HsvAllcr,
    HsvCrcrc,
)

# --- Helper dataclasses ---
@dataclass
class StudentRecord:
    rbid: str
    preferred_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[str]
    level_id: Optional[str]
    level_name: Optional[str]
    student_type_id: Optional[str]
    student_type_name: Optional[str]
    active_ind: Optional[str]
    hsv_stdnt: Optional[HsvStdnt] = None

@dataclass
class PersonRecord:
    rbid: str
    preferred_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[str]
    id_num: Optional[str]
    id_country: Optional[str]
    hgv_prson: Optional[HgvPrson] = None


# --- Utility functions ---
def make_student_record(stdnt: Optional[HsvStdnt]) -> StudentRecord:
    """
    Build StudentRecord from HsvStdnt object.
    """

    def safe_date(d):
        if d is None:
            return None
        if d.year < 1900:
            return None
        return d

    # --------------------
    # GumIdent fields
    # --------------------
    rbid = None
    preferred_name = None
    first_name = None
    middle_name = None
    last_name = None
    birthday = None
    level_id = None
    level_name = None
    student_type_id = None
    student_type_name = None
    active_ind = None

    if stdnt:
        rbid = stdnt.hsv_stdnt_rbid
        preferred_name = stdnt.hsv_stdnt_pref_first_name
        first_name = stdnt.hsv_stdnt_first_name
        middle_name = stdnt.hsv_stdnt_middle_name
        last_name = stdnt.hsv_stdnt_last_name
        birthday = safe_date(stdnt.hsv_stdnt_birthday)
        level_id = stdnt.hsv_stdnt_lvid
        level_name = stdnt.hsv_stdnt_level
        student_type_id = stdnt.hsv_stdnt_stid
        student_type_name = stdnt.hsv_stdnt_student_type
        active_ind = stdnt.hsv_stdnt_active_ind

    return StudentRecord(
        rbid=rbid,
        preferred_name=preferred_name,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        birthday=birthday,
        level_id=level_id,
        level_name=level_name,
        student_type_id=student_type_id,
        student_type_name=student_type_name,
        active_ind=active_ind,
        hsv_stdnt=stdnt
    )

def get_student_record_by_rbid(rbid: str) -> Optional[StudentRecord]:
    """
    Fetch and return StudentRecord for given RBID.
    """
    # get GumIdent
    stdnt_qs = HsvStdnt.objects.using('sis').filter(hsv_stdnt_rbid=rbid).first()
    if not stdnt_qs:
        return None

    return make_student_record(stdnt_qs)


def make_person_record(prson: Optional[HgvPrson]) -> PersonRecord:
    """
    Build PersonRecord from hsv_prson.
    """

    def safe_date(d):
        if d is None:
            return None
        if d.year < 1900:
            return None
        return d

    # --------------------
    # GumIdent fields
    # --------------------
    rbid = None
    preferred_name = None
    first_name = None
    middle_name = None
    last_name = None
    birthday = None
    id_num = None
    id_country = None

    if prson:
        rbid = prson.hgv_prson_rbid
        preferred_name = prson.hgv_prson_pref_first_name
        first_name = prson.hgv_prson_first_name
        middle_name = prson.hgv_prson_middle_name
        last_name = prson.hgv_prson_last_name
        birthday = safe_date(prson.hgv_prson_birthday)
        id_num = prson.hgv_prson_idnum
        id_country = prson.hgv_prson_id_country

    return PersonRecord(
        rbid=rbid,
        preferred_name=preferred_name,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        birthday=birthday,
        id_num=id_num,
        id_country=id_country,
        hgv_prson=prson,
    )

def get_person_record_by_rbid(rbid: str) -> Optional[PersonRecord]:
    """
    Fetch and return PersonRecord for given RBID
    """
    
    prson_qs = HgvPrson.objects.using('sis').filter(hgv_prson_rbid=rbid).first()
    if not prson_qs:
        return None

    return make_person_record(prson_qs)

# --- Views ---

@login_required
def dashboard(request):
    """Main dashboard/home page"""
    context = {
        'user': request.user,
    }
    return render(request, 'sis/dashboard.html', context)


@login_required
def student_list(request):
    """List  students with search and pagination"""
    search_query = request.GET.get('search', '').strip()
    rbid_query = request.GET.get('rbid', '').strip()

    # Base queryset: only students that have a SGM_stdnt record
    stdnt_qs = HsvStdnt.objects.using('sis').all()

    # Search by name or RBID through GumIdent
    if search_query:
        stdnt_qs = stdnt_qs.filter(
            models.Q(hsv_stdnt_first_name__icontains=search_query) |
            models.Q(hsv_stdnt_last_name__icontains=search_query)
        )

    if rbid_query:
        stdnt_qs = stdnt_qs.filter(hsv_stdnt_rbid__icontains=rbid_query)

    # Order by last_name, first_name from GumIdent
    stdnt_qs = stdnt_qs.order_by(
        'hsv_stdnt_last_name',
        'hsv_stdnt_first_name'
    )

    # Limit to 2000 results for safety
    stdnt_list = stdnt_qs[:2000]

    # Build student records
    students: List = []
    for stdnt in stdnt_list:
        students.append(make_student_record(stdnt))

    # Pagination
    paginator = Paginator(students, 25)  # 25 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'sis/student_list.html', context)

@login_required
def student_detail(request, student_rbid):
    """View/edit individual student by RBID"""
    # Build combined student record
    record = get_student_record_by_rbid(student_rbid)
    if not record:
        # mimic get_object_or_404 behaviour
        return get_object_or_404(GumIdent, gum_ident_rbid=student_rbid)

    # Enrollments for student: SrhEnrol rows where srh_enrol_rbid = student's rbid
    enrollments = SrhEnrol.objects.using('sis').filter(
        srh_enrol_rbid__gum_ident_rbid=student_rbid
    ).select_related(
        'srh_enrol_esid', 
        'srh_enrol_stid__srb_sects_crid',
        'srh_enrol_stid__srb_sects_tmid'
    )

    if request.method == 'POST':
        # Accept only a small set of editable fields for safety
        # Update GumIdent: first_name, last_name, idnum
        # Update SgmStubi: active_ind
        ident = record.gum_ident
        stubi = record.sgm_stubi

        # use transaction to keep changes consistent
        try:
            with transaction.atomic(using='sis'):
                if ident:
                    ident.gum_ident_first_name = request.POST.get('first_name', ident.gum_ident_first_name)
                    ident.gum_ident_last_name = request.POST.get('last_name', ident.gum_ident_last_name)
                    # idnum if provided
                    idnum = request.POST.get('idnum')
                    if idnum is not None:
                        ident.gum_ident_idnum = idnum or None
                    ident.save(using='sis')

                if stubi:
                    active_val = request.POST.get('active_ind')
                    if active_val is not None:
                        stubi.sgm_stubi_active_ind = active_val
                        stubi.save(using='sis')

            messages.success(request, 'Student updated successfully.')
            return redirect('sis:student_detail', student_rbid=student_rbid)
        except Exception as e:
            messages.error(request, f'Error updating student: {e}')

    context = {
        'student': record,
        'enrollments': enrollments,
    }
    return render(request, 'sis/student_detail.html', context)


@login_required
def course_list(request):
    """List all courses with search and pagination"""
    search_query = request.GET.get('search', '').strip()

    qs = SrlCours.objects.using('sis').all().select_related('srl_cours_sbid')

    if search_query:
        qs = qs.filter(
            models.Q(srl_cours_crid__icontains=search_query) |
            models.Q(srl_cours_hr_name__icontains=search_query) |
            models.Q(srl_cours_crse_num__icontains=search_query) |
            models.Q(srl_cours_sbid__srl_subjs_hr_name__icontains=search_query)
        )

    qs = qs.order_by('srl_cours_crid')

    # Build simple course objects for template convenience
    courses = []
    for c in qs:
        subject_code = getattr(c.srl_cours_sbid, 'srl_subjs_sbid', None) if getattr(c, 'srl_cours_sbid', None) else None
        course_code = f"{subject_code} {c.srl_cours_crse_num}" if subject_code else f"{c.srl_cours_crse_num}"
        courses.append({
            'id': c.srl_cours_crid,
            'course_code': course_code,
            'course_name': c.srl_cours_hr_name,
            'inactive_ind': c.srl_cours_inactive_ind,
            'model': c,
        })

    paginator = Paginator(courses, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'sis/course_list.html', context)


def person_list(request):
    """List all students with search and pagination"""
    search_query = request.GET.get('search', '').strip()
    rbid_query = request.GET.get('rbid', '').strip()

    # Base queryset: only students that have a SGM_STUBI record
    prson_qs = HgvPrson.objects.using('sis').all()

    # Search by name or RBID through hsvprson
    if search_query:
        prson_qs = prson_qs.filter(
            models.Q(hgv_prson_first_name__icontains=search_query) |
            models.Q(hgv_prson_last_name__icontains=search_query)
        )

    if rbid_query:
        prson_qs = prson_qs.filter(hgv_prson_rbid__icontains=rbid_query)

    # Order by last_name, first_name from hsvprson
    prson_qs = prson_qs.order_by(
        'hgv_prson_last_name',
        'hgv_prson_first_name'
    )

    # Limit to 2000 results for safety
    prson_list = prson_qs[:2000]

    # Build student records
    persons: List = []
    for prson in prson_list:
        persons.append(make_person_record(prson))

    # Pagination
    paginator = Paginator(persons, 25)  # 25 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'sis/person_list.html', context)

@login_required
def person_detail(request, person_rbid):
    """View/edit individual student by RBID"""
    record = get_person_record_by_rbid(person_rbid)
    if not record:
        return get_object_or_404(GumIdent, gum_ident_rbid=person_rbid)

    if request.method == 'POST':
        ident = record.gum_ident

        # use transaction to keep changes consistent
        try:
            with transaction.atomic(using='sis'):
                if ident:
                    ident.gum_ident_first_name = request.POST.get('first_name', ident.gum_ident_first_name)
                    ident.gum_ident_last_name = request.POST.get('last_name', ident.gum_ident_last_name)
                    # idnum if provided
                    idnum = request.POST.get('idnum')
                    if idnum is not None:
                        ident.gum_ident_idnum = idnum or None
                    ident.save(using='sis')

            messages.success(request, 'Persson updated successfully.')
            return redirect('sis:person_detail', person_rbid=person_rbid)
        except Exception as e:
            messages.error(request, f'Error updating student: {e}')

    context = {
        'person': record,
    }
    return render(request, 'sis/person_detail.html', context)


@login_required
def course_detail(request, course_id):
    """View/edit individual course by CRID"""
    # Get course (SrlCours)
    course = get_object_or_404(SrlCours.objects.using('sis'), pk=course_id)

    # Sections for this course
    sections = SrbSects.objects.using('sis').filter(srb_sects_crid=course).select_related('srb_sects_tmid')

    # Enrollments for this course: SrhEnrol where srh_enrol_stid references a section whose crid is this course
    enrollments = SrhEnrol.objects.using('sis').filter(srh_enrol_stid__srb_sects_crid=course).select_related(
        'srh_enrol_stid', 'srh_enrol_esid', 'srh_enrol_stid__srb_sects_tmid'
    )

    if request.method == 'POST':
        # Only allow limited updates: course title and inactive indicator
        course_title = request.POST.get('course_name')
        inactive = request.POST.get('inactive_ind')

        if course_title is not None:
            course.srl_cours_hr_name = course_title

        if inactive is not None:
            course.srl_cours_inactive_ind = inactive

        try:
            course.save(using='sis')
            messages.success(request, 'Course updated successfully.')
            return redirect('sis:course_detail', course_id=course_id)
        except Exception as e:
            messages.error(request, f'Error updating course: {e}')

    context = {
        'course': course,
        'sections': sections,
        'enrollments': enrollments,
    }
    return render(request, 'sis/course_detail.html', context)
