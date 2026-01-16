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
    GumIdent,
    SgmStubi,
    SrlCours,
    SrbSects,
    SrhEnrol,
    SrlEnrst,
    SrlSubjs,
    SglTerms,
    ScbMjrcm,
    SclMajor,
    SdlCamps,
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
    major1_id: Optional[str]
    major1_name: Optional[str]
    major1_campus_id: Optional[str]
    major1_campus_name: Optional[str]
    minor1_id: Optional[str]
    minor1_name: Optional[str]
    minor1_campus_id: Optional[str]
    minor1_campus_name: Optional[str]
    active_ind: Optional[str]
    gum_ident: Optional[GumIdent] = None
    sgm_stubi: Optional[SgmStubi] = None

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
    gum_ident: Optional[GumIdent] = None


# --- Utility functions ---
def make_student_record(ident: Optional[GumIdent], stubi: Optional[SgmStubi]) -> StudentRecord:
    """
    Build StudentRecord from GumIdent and SgmStubi objects.
    Handles ScbMjrcm -> SclMajor and ScbMjrcm -> SdlCamps for majors/minors with campus.
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

    if ident:
        rbid = ident.gum_ident_rbid
        preferred_name = ident.gum_ident_first_name
        first_name = ident.gum_ident_first_name
        middle_name = ident.gum_ident_middle_name
        last_name = ident.gum_ident_last_name
        birthday = safe_date(ident.gum_ident_birthday)

    # --------------------
    # SgmStubi fields
    # --------------------
    level_id = None
    level_name = None
    student_type_id = None
    student_type_name = None
    active_ind = None

    # primary major/minor only (for current StudentRecord)
    major1_id = None
    major1_name = None
    major1_campus_id = None
    major1_campus_name = None
    minor1_id = None
    minor1_name = None
    minor1_campus_id = None
    minor1_campus_name = None

    if stubi:
        rbid = rbid or stubi.sgm_stubi_rbid
        active_ind = stubi.sgm_stubi_active_ind

        # ---- Level ----
        lvl = getattr(stubi, 'sgm_stubi_lvid', None)
        if lvl:
            level_id = getattr(lvl, 'sgl_level_lvid', None)
            level_name = getattr(lvl, 'sgl_level_hr_name', None)

        # ---- Student type ----
        st = getattr(stubi, 'sgm_stubi_stid', None)
        if st:
            student_type_id = getattr(st, 'sgl_stype_stid', None)
            student_type_name = getattr(st, 'sgl_stype_hr_name', None)

        # ---- Majors / Minors via ScbMjrcm ----
        def extract_major_with_campus(mjrcm_obj):
            """
            Given ScbMjrcm, return (major_id, major_name, campus_id, campus_name) safely.
            ScbMjrcm has:
              - scb_mjrcm_mrid (FK to SclMajor)
              - scb_mjrcm_cpid (FK to SdlCamps)
            """
            if not mjrcm_obj:
                return None, None, None, None
            
            # Get the SclMajor from the FK
            major = getattr(mjrcm_obj, 'scb_mjrcm_mrid', None)
            major_id = None
            major_name = None
            if major:
                major_id = getattr(major, 'scl_major_mrid', None)
                major_name = getattr(major, 'scl_major_hr_name', None)
            
            # Get the SdlCamps from the FK
            campus = getattr(mjrcm_obj, 'scb_mjrcm_cpid', None)
            campus_id = None
            campus_name = None
            if campus:
                campus_id = getattr(campus, 'sdl_camps_cpid', None)
                campus_name = getattr(campus, 'sdl_camps_hr_name', None)
            
            return major_id, major_name, campus_id, campus_name

        major1_id, major1_name, major1_campus_id, major1_campus_name = extract_major_with_campus(
            getattr(stubi, 'sgm_stubi_major1_mcid', None)
        )

        minor1_id, minor1_name, minor1_campus_id, minor1_campus_name = extract_major_with_campus(
            getattr(stubi, 'sgm_stubi_minor1_mcid', None)
        )

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
        major1_id=major1_id,
        major1_name=major1_name,
        major1_campus_id=major1_campus_id,
        major1_campus_name=major1_campus_name,
        minor1_id=minor1_id,
        minor1_name=minor1_name,
        minor1_campus_id=minor1_campus_id,
        minor1_campus_name=minor1_campus_name,
        active_ind=active_ind,
        gum_ident=ident,
        sgm_stubi=stubi,
    )

def get_student_record_by_rbid(rbid: str) -> Optional[StudentRecord]:
    """
    Fetch and return StudentRecord for given RBID (joined GumIdent + SgmStubi).
    Uses select_related where useful.
    """
    # get GumIdent
    ident = GumIdent.objects.using('sis').filter(gum_ident_rbid=rbid).first()

    # get SgmStubi with related lookups (levels, types, majors via ScbMjrcm, campus)
    stubi_qs = SgmStubi.objects.using('sis').filter(sgm_stubi_rbid=rbid)
    # select_related to get the ScbMjrcm, then the SclMajor and SdlCamps
    try:
        stubi = stubi_qs.select_related(
            'sgm_stubi_lvid',
            'sgm_stubi_stid',
            'sgm_stubi_major1_mcid__scb_mjrcm_mrid',  # ScbMjrcm -> SclMajor
            'sgm_stubi_major1_mcid__scb_mjrcm_cpid',  # ScbMjrcm -> SdlCamps
            'sgm_stubi_minor1_mcid__scb_mjrcm_mrid',  # ScbMjrcm -> SclMajor
            'sgm_stubi_minor1_mcid__scb_mjrcm_cpid',  # ScbMjrcm -> SdlCamps
            'sgm_stubi_major2_mcid__scb_mjrcm_mrid',
            'sgm_stubi_major2_mcid__scb_mjrcm_cpid',
            'sgm_stubi_minor2_mcid__scb_mjrcm_mrid',
            'sgm_stubi_minor2_mcid__scb_mjrcm_cpid',
            'sgm_stubi_major3_mcid__scb_mjrcm_mrid',
            'sgm_stubi_major3_mcid__scb_mjrcm_cpid',
            'sgm_stubi_minor3_mcid__scb_mjrcm_mrid',
            'sgm_stubi_minor3_mcid__scb_mjrcm_cpid',
        ).first()
    except Exception:
        stubi = stubi_qs.first()

    if not ident and not stubi:
        return None

    return make_student_record(ident, stubi)


def make_person_record(ident: Optional[GumIdent]) -> PersonRecord:
    """
    Build PersonRecord from GumIdent and GglCount object.
    Handles GumIdent -> GglCount.
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

    if ident:
        rbid = ident.gum_ident_rbid
        preferred_name = ident.gum_ident_first_name
        first_name = ident.gum_ident_first_name
        middle_name = ident.gum_ident_middle_name
        last_name = ident.gum_ident_last_name
        birthday = safe_date(ident.gum_ident_birthday)
        id_num = ident.gum_ident_idnum

    if ident and ident.gum_ident_id_coid:
        id_country = ident.gum_ident_id_coid.ggl_count_hr_name

    return PersonRecord(
        rbid=rbid,
        preferred_name=preferred_name,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        birthday=birthday,
        id_num=id_num,
        id_country=id_country,
        gum_ident=ident,
    )

def get_pesron_record_by_rbid(rbid: str) -> Optional[PersonRecord]:
    """
    Fetch and return StudentRecord for given RBID (joined GumIdent + SgmStubi).
    Uses select_related where useful.
    """
    # get GumIdent
    ident_qs = GumIdent.objects.using('sis').filter(gum_ident_rbid=rbid)

    # get SgmStubi with related lookups (levels, types, majors via ScbMjrcm, campus)
    # select_related to get the ScbMjrcm, then the SclMajor and SdlCamps
    try:
        ident = ident_qs.select_related(
            'gum_ident_rbid',
            'gum_ident_first_name',
            'gum_ident_last_name',
            'gum_ident_middle_name',
            'gum_ident_birthday',
            'gum_ident_idnum',
            'gum_ident_id_coid'
        ).first()
    except Exception:
        ident = -ident_qs.first()

    if not ident_qs:
        return None

    return make_person_record(ident)

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
    """List all students with search and pagination"""
    search_query = request.GET.get('search', '').strip()
    rbid_query = request.GET.get('rbid', '').strip()

    # Base queryset: only students that have a SGM_STUBI record
    stubi_qs = SgmStubi.objects.using('sis').select_related(
        'sgm_stubi_rbid',  # GumIdent
        'sgm_stubi_lvid',
        'sgm_stubi_stid',
        'sgm_stubi_major1_mcid__scb_mjrcm_mrid',  # ScbMjrcm -> SclMajor
        'sgm_stubi_major1_mcid__scb_mjrcm_cpid',  # ScbMjrcm -> SdlCamps
        'sgm_stubi_minor1_mcid__scb_mjrcm_mrid',  # ScbMjrcm -> SclMajor
        'sgm_stubi_minor1_mcid__scb_mjrcm_cpid'   # ScbMjrcm -> SdlCamps
    )

    # Search by name or RBID through GumIdent
    if search_query:
        stubi_qs = stubi_qs.filter(
            models.Q(sgm_stubi_rbid__gum_ident_first_name__icontains=search_query) |
            models.Q(sgm_stubi_rbid__gum_ident_last_name__icontains=search_query)
        )

    if rbid_query:
        stubi_qs = stubi_qs.filter(sgm_stubi_rbid__gum_ident_rbid__icontains=rbid_query)

    # Order by last_name, first_name from GumIdent
    stubi_qs = stubi_qs.order_by(
        'sgm_stubi_rbid__gum_ident_last_name',
        'sgm_stubi_rbid__gum_ident_first_name'
    )

    # Limit to 2000 results for safety
    stubi_list = stubi_qs[:2000]

    # Build student records
    students: List = []
    for stubi in stubi_list:
        students.append(make_student_record(stubi.sgm_stubi_rbid, stubi))

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
            return redirect('student_detail', student_rbid=student_rbid)
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
    ident_qs = GumIdent.objects.using('sis').select_related(
        'gum_ident_rbid',
        'gum_ident_first_name',
        'gum_ident_last_name',
        'gum_ident_middle_name',
        'gum_ident_birthday',
        'gum_ident_idnum',
        'gum_ident_id_coid'
    )

    # Search by name or RBID through GumIdent
    if search_query:
        ident_qs = ident_qs.filter(
            models.Q(gum_ident_rbid__gum_ident_first_name__icontains=search_query) |
            models.Q(gum_ident_rbid__gum_ident_last_name__icontains=search_query)
        )

    if rbid_query:
        stubi_qs = stubi_qs.filter(gum_ident_rbid__gum_ident_rbid__icontains=rbid_query)

    # Order by last_name, first_name from GumIdent
    ident_qs = ident_qs.order_by(
        'gum_ident_rbid__gum_ident_last_name',
        'gum_ident_rbid__gum_ident_first_name'
    )

    # Limit to 2000 results for safety
    ident_list = ident_qs[:2000]

    # Build student records
    persons: List = []
    for ident in ident_list:
        persons.append(make_person_record(ident.gum_ident_rbid, ident))

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
            return redirect('person_detail', student_rbid=student_rbid)
        except Exception as e:
            messages.error(request, f'Error updating student: {e}')

    context = {
        'student': record,
        'enrollments': enrollments,
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
            return redirect('course_detail', course_id=course_id)
        except Exception as e:
            messages.error(request, f'Error updating course: {e}')

    context = {
        'course': course,
        'sections': sections,
        'enrollments': enrollments,
    }
    return render(request, 'sis/course_detail.html', context)
