"""
SIS Views - Banner-style pages with campus per major support
Place this in /srv/ribbon2helmsman/helmsman/sis/views.py
"""
from django.db import models
from dataclasses import dataclass
from typing import Optional, List
import traceback

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
    HsvLtsts,
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
class StudentDetail:
    rbid: str
    term: str
    tsid: str
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
    hsv_ltsts: Optional[HsvLtsts] = None
    sgm_stubi: Optional[SgmStubi] = None

@dataclass
class Enrollments:
    rbid: str
    section: str
    term: str
    subject: str
    number: str
    status: str
    activity_date: str
    sgm_stubi: Optional[SgmStubi] = None
    srh_enrol: Optional[SrhEnrol] = None


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

@dataclass
class PersonDetail:
    rbid: str
    preferred_name: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    birthday: Optional[str]
    id_num: Optional[str]
    id_coid: Optional[str]
    id_country: Optional[str]
    gum_ident: Optional[GumIdent] = None
    gum_adinf: Optional[GumAdinf] = None


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

def make_student_detail_record(search_rbid: str) -> StudentDetail:
    """
    Build StudentDetail from HsvLtsts and its select_related objects.
    """

    def safe_date(d):
        if d is None:
            return None
        if d.year < 1900:
            return None
        return d

    rbid = None
    term = None
    tsid = None
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
    ltsts = HsvLtsts.objects.using('sis').filter(hsv_ltsts_rbid=search_rbid).first()
    stubi = None 
    if ltsts:
        stubi = SgmStubi.objects.using('sis').filter(sgm_stubi_tsid=ltsts.hsv_ltsts_latest_tsid_id).first()
        ident = GumIdent.objects.using('sis').filter(gum_ident_rbid=stubi.sgm_stubi_rbid_id).first()
        adinf = GumAdinf.objects.using('sis').filter(gum_adinf_rbid_id=ident.gum_ident_rbid).first()
        level = SglLevel.objects.using('sis').filter(sgl_level_lvid=stubi.sgm_stubi_lvid_id).first()
        stype = SglStype.objects.using('sis').filter(sgl_stype_stid=stubi.sgm_stubi_stid_id).first()

        rbid = stubi.sgm_stubi_rbid_id
        term = stubi.sgm_stubi_tmid_id
        tsid = stubi.sgm_stubi_tsid_id
        preferred_name = adinf.gum_adinf_pref_first_name
        first_name = ident.gum_ident_first_name
        middle_name = ident.gum_ident_middle_name
        last_name = ident.gum_ident_last_name
        birthday = safe_date(ident.gum_ident_birthday)
        level_id = stubi.sgm_stubi_lvid_id
        level_name = level.sgl_level_hr_name
        student_type_id = stubi.sgm_stubi_stid_id
        student_type_name = stype.sgl_stype_hr_name
        active_ind = stubi.sgm_stubi_active_ind

    return StudentDetail(
        rbid=rbid,
        term=term,
        tsid=tsid,
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
        hsv_ltsts=ltsts,
        sgm_stubi=stubi,
    )

def make_person_detail_record(search_rbid: str) -> PersonDetail:
    """
    Build StudentDetail from HsvLtsts and its select_related objects.
    """

    def safe_date(d):
        if d is None:
            return None
        if d.year < 1900:
            return None
        return d

    rbid = None
    preferred_name = None
    first_name = None
    middle_name = None
    last_name = None
    username = None
    birthday = None
    id_num = None
    id_coid = None
    id_country = None
    ident = GumIdent.objects.using('sis').filter(gum_ident_rbid=search_rbid).first()
    adinf = None 
    if ident:
        adinf = GumAdinf.objects.using('sis').filter(gum_adinf_rbid_id=ident.gum_ident_rbid).first()
        count = GglCount.objects.using('sis').filter(ggl_count_coid=ident.gum_ident_id_coid_id).first()

        rbid = ident.gum_ident_rbid
        preferred_name = adinf.gum_adinf_pref_first_name
        first_name = ident.gum_ident_first_name
        middle_name = ident.gum_ident_middle_name
        last_name = ident.gum_ident_last_name
        birthday = safe_date(ident.gum_ident_birthday)
        username = adinf.gum_adinf_username
        id_num = ident.gum_ident_idnum
        id_coid = ident.gum_ident_id_coid_id
        id_country =count.ggl_count_hr_name


    return PersonDetail(
        rbid=rbid,
        preferred_name=preferred_name,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        username=username,
        birthday=birthday,
        id_num=id_num,
        id_coid=id_coid,
        id_country=id_country,
        gum_ident=ident,
        gum_adinf=adinf,
    )
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
    record = make_student_detail_record(student_rbid)
    if not record:
        # mimic get_object_or_404 behaviour
        return get_object_or_404(GumIdent, gum_ident_rbid=student_rbid)
    stypes = SglStype.objects.using('sis').all()
    levels = SglLevel.objects.using('sis').all()
    camps = SdlCamps.objects.using('sis').all()
    
    print(f"stid: '{record.student_type_id}' type: {type(record.student_type_id)}")
    print(f"sgl_stype_stid sample: '{stypes.first().sgl_stype_stid}' type: {type(stypes.first().sgl_stype_stid)}")

    print(f"lvid: '{record.level_id}' type: {type(record.level_id)}")
    print(f"sgl_stype_stid sample: '{levels.first().sgl_level_lvid}' type: {type(levels.first().sgl_level_lvid)}")
    
    # Enrollments for student: SrhEnrol rows where srh_enrol_rbid = student's rbid
    enrollments = SrhEnrol.objects.using('sis').filter(
        srh_enrol_rbid=student_rbid
    ).select_related(
        'srh_enrol_esid', 
        'srh_enrol_stid__srb_sects_crid',
        'srh_enrol_stid__srb_sects_tmid'
    )

    majors = ScmStucv.objects.using('sis').filter(
        scm_stucv_rbid=student_rbid
    ).select_related(
        'scm_stucv_cvid__scl_currv_mrid',
        'scm_stucv_cvid__scl_currv_mrid__scl_major_dgid',
        'scm_stucv_cpid',
        'scm_stucv_cvid__scl_currv_ctid',
    )

    if request.method == 'POST' and 'stubi-post' in request.POST:
        # Accept only a small set of editable fields for safety
        # Update GumIdent: first_name, last_name, idnum
        # Update SgmStubi: active_ind
        stubi = record.sgm_stubi

        # use transaction to keep changes consistent
        try:
            with transaction.atomic(using='sis'):
                if stubi:
                    stubi.sgm_stubi_active_ind = request.POST.get('active_ind', stubi.sgm_stubi_active_ind )
                    stubi.sgm_stubi_lvid_id = request.POST.get('level', stubi.sgm_stubi_lvid_id )
                    stubi.sgm_stubi_stid_id = request.POST.get('stype', stubi.sgm_stubi_stid_id )
                    stubi.save(using='sis')

            messages.success(request, 'Student updated successfully.')
            return redirect('sis:student_detail', student_rbid=student_rbid)
        except Exception as e:
            messages.error(request, f'Error updating student: {e}')

    if request.method == 'POST' and 'update_major' in request.POST:
        try:
            with transaction.atomic(using='sis'):
                scid = request.POST.get('update_major')
                print(scid)
                stucv = ScmStucv.objects.using('sis').filter(
                    scm_stucv_scid=scid
                ).first()
                stucv.scm_stucv_cpid_id = request.POST.get('cpid', stucv.scm_stucv_cpid_id )
                stucv.scm_stucv_active_ind = request.POST.get('m_active_ind', stucv.scm_stucv_active_ind )
                stucv.save()
                messages.success(request, 'Major updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating student: {e}')

    context = {
        'student': record,
        'enrollments': enrollments,
        'levels': levels,
        'stypes': stypes,
        'majors': majors,
        'camps': camps,
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
    record = make_person_detail_record(person_rbid)
    countries = GglCount.objects.using('sis').all()
    print(f"id_coid: '{record.id_coid}' type: {type(record.id_coid)}")
    print(f"ggl_count_coid sample: '{countries.first().ggl_count_coid}' type: {type(countries.first().ggl_count_coid)}")
    if not record:
        return get_object_or_404(GumIdent, gum_ident_rbid=person_rbid)

    if request.method == 'POST':
        ident = record.gum_ident
        adinf = record.gum_adinf

        # use transaction to keep changes consistent
        try:
            with transaction.atomic(using='sis'):
                if ident:
                    ident.gum_ident_first_name = request.POST.get('first_name', ident.gum_ident_first_name)
                    ident.gum_ident_middle_name = request.POST.get('middle_name', ident.gum_ident_middle_name)
                    ident.gum_ident_last_name = request.POST.get('last_name', ident.gum_ident_last_name)
                    ident.gum_ident_idnum = request.POST.get('id_num', ident.gum_ident_idnum)
                    ident.gum_ident_id_coid_id = request.POST.get('id_country', ident.gum_ident_id_coid_id)
                    ident.save(using='sis')
                if adinf:
                    adinf.gum_adinf_pref_first_name = request.POST.get('preferred_name', adinf.gum_adinf_pref_first_name)
                    adinf.gum_adinf_username = request.POST.get('username', adinf.gum_adinf_username)
                    adinf.save(using='sis')

            messages.success(request, 'Persson updated successfully.')
            return redirect('sis:person_detail', person_rbid=person_rbid)
        except Exception as e:
            messages.error(request, f'Error updating student: {e}')

    context = {
        'person': record,
        'countries': countries,
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
