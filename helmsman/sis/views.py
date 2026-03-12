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
    HsvSects,
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
class CourseRecord:
    crid: str
    sbid: str
    number: str
    subject: str
    department: str
    name: str
    status: str
    actcr: Optional[HsvAllcr] = None

@dataclass
class CourseDetail:
    crid: str
    sbid: str
    number: str
    subject: str
    dpid: str
    department: str
    name: str
    status: str
    credit_hours: str
    cours: Optional[SrlCours] = None

@dataclass
class SectionRecord:
    stid: str
    tmid: str
    crid: str
    seq: str
    name: str
    prim_inst: str
    scnd_inst: str
    sects: Optional[HsvSects] = None

@dataclass
class SectionDetail:
    stid: str
    tmid: str
    crid: str
    seq: str
    name: str
    prim_rbid: str
    prim_inst: str
    scnd_rbid: Optional[str]
    scnd_inst: Optional[str]
    sects: Optional[SrbSects] = None

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

def make_course_record(allcr: Optional[HsvAllcr]) -> CourseRecord:
    """
    Build StudentRecord from HsvStdnt object.
    """

    crid = None
    sbid = None
    number = None
    subject = None
    department = None
    name = None
    status = None

    if allcr:
        crid = allcr.hsv_allcr_crid
        sbid = allcr.hsv_allcr_sbid
        number = allcr.hsv_allcr_crse_num
        subject = allcr.hsv_allcr_subject
        department = allcr.hsv_allcr_department
        name = allcr.hsv_allcr_name
        status = allcr.hsv_allcr_active_ind
    
    return CourseRecord (
    crid=crid,
    sbid=sbid,
    number=number,
    subject=subject,
    department=department,
    name=name,
    status=status,
    )

def make_course_detail_record(search_crid: str) -> CourseDetail:
    """
    Build StudentDetail from HsvLtsts and its select_related objects.
    """

    crid = None
    sbid = None
    number = None
    subject = None
    dpid = None
    department = None
    name = None
    status = None
    credit_hours = None
    cours = SrlCours.objects.using('sis').filter(srl_cours_crid=search_crid).select_related('srl_cours_sbid', 'srl_cours_sbid__srl_subjs_dpid').first()
    if cours:
        crid = cours.srl_cours_crid
        sbid = cours.srl_cours_sbid_id
        number = cours.srl_cours_crse_num
        subject = cours.srl_cours_sbid.srl_subjs_hr_name
        dpid = cours.srl_cours_sbid.srl_subjs_dpid_id
        department = cours.srl_cours_sbid.srl_subjs_dpid.sdl_depts_hr_name
        name = cours.srl_cours_hr_name
        status = cours.srl_cours_active_ind
        credit_hours = cours.srl_cours_credit_hours


    return CourseDetail(
        crid=crid,
        sbid=sbid,
        number=number,
        subject=subject,
        dpid=dpid,
        department=department,
        name=name,
        status=status,
        credit_hours=credit_hours,
        cours=cours,
    )

def make_section_record(sects: Optional[HsvSects]) -> SectionRecord:
    """
    Build StudentRecord from HsvStdnt object.
    """

    stid = None
    tmid = None
    crid = None
    seq = None
    name = None
    prim_inst = None
    scnd_inst = None

    if sects:
        stid = sects.hsv_sects_stid
        tmid = sects.hsv_sects_tmid
        crid = sects.hsv_sects_crid
        seq = sects.hsv_sects_seq
        name = sects.hsv_sects_name
        prim_inst = sects.hsv_sects_prim_inst
        scnd_inst = sects.hsv_sects_scnd_inst
    
    return SectionRecord (
    stid=stid,
    tmid=tmid,
    crid=crid,
    seq=seq,
    name=name,
    prim_inst=prim_inst,
    scnd_inst=scnd_inst,
    )

def make_section_detail_record(search_stid: str) -> SectionDetail:
    """
    Build StudentDetail from HsvLtsts and its select_related objects.
    """

    stid = None
    tmid = None
    crid = None
    seq = None
    name = None
    prim_rbid = None
    prim_inst = None
    scnd_rbid = None
    scnd_inst = None
    sects = SrbSects.objects.using('sis').filter(srb_sects_stid=search_stid).select_related('srb_sects_prim_inst', 'srb_sects_scnd_inst', 'srb_sects_crid').first()
    if sects:
        stid = sects.srb_sects_stid
        tmid = sects.srb_sects_tmid_id
        crid = sects.srb_sects_crid_id
        seq = sects.srb_sects_section_seq
        name = sects.srb_sects_crid.srl_cours_hr_name
        prim_rbid = sects.srb_sects_prim_inst.gum_ident_rbid
        prim_inst = sects.srb_sects_prim_inst.gum_ident_first_name + ' ' + sects.srb_sects_prim_inst.gum_ident_last_name
        if sects.srb_sects_scnd_inst:
            scnd_rbid = sects.srb_sects_scnd_inst.gum_ident_rbid
            scnd_inst = sects.srb_sects_scnd_inst.gum_ident_first_name + ' ' + sects.srb_sects_scnd_inst.gum_ident_last_name


    return SectionDetail(
        stid=stid,
        tmid=tmid,
        crid=crid,
        seq=seq,
        name=name,
        prim_rbid=prim_rbid,
        prim_inst=prim_inst,
        scnd_rbid=scnd_rbid,
        scnd_inst=scnd_inst,
        sects=sects,
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

# --- Search and Update Views ---
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
    url_name = request.resolver_match.url_name
    student_link_map = {
        'student_list': 'sis/student_list.html',
        'enrollment_create_student_select': 'sis/enrollment_create_student_select.html',
    }
    student_link = student_link_map.get(url_name, 'sis/student_list.html')

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
    return render(request, student_link, context)

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
                scid = request.POST.get('scid')
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

    course_qs = HsvAllcr.objects.using('sis').all()

    if search_query:
        course_qs = course_qs.filter(
            models.Q(hsv_allcr_crid__icontains=search_query) |
            models.Q(hsv_allcr_name__icontains=search_query) |
            models.Q(hsv_allcr_crse_num__icontains=search_query) |
            models.Q(hsv_allcr_sbid__icontains=search_query)
        )

    course_qs = course_qs.order_by('hsv_allcr_crid')

    # Build simple course objects for template convenience
    course_list = course_qs[:2000]
    courses: List = []
    for course in course_list:
        courses.append(make_course_record(course))

    paginator = Paginator(courses, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'sis/course_list.html', context)

@login_required
def course_detail(request, course_crid):
    """View/edit individual course by CRID"""
    # Get course (SrlCours)
    record = make_course_detail_record(course_crid)
    subjects = SrlSubjs.objects.using('sis').all()
    if request.method == 'POST':
        cours = record.cours
        try:
            with transaction.atomic(using='sis'):
                if cours:
                    cours.srl_cours_hr_name = request.POST.get('name', cours.srl_cours_hr_name)
                    cours.srl_cours_credit_hours = request.POST.get('credit_hr', cours.srl_cours_credit_hours )
                    cours.srl_cours_active_ind = request.POST.get('active_ind', cours.srl_cours_active_ind)
                    cours.save(using='sis')
            messages.success(request, 'Course updated successfully.')
            return redirect('sis:course_detail', course_crid=course_crid)
        except Exception as e:
            messages.error(request, f'Error updating student: {e}')

    context = {
        'course': record,
        'subjects': subjects
    }
    return render(request, 'sis/course_detail.html', context)

@login_required
def section_list(request):
    """List all courses with search and pagination"""
    search_query = request.GET.get('search', '').strip()

    sections_qs = HsvSects.objects.using('sis').all()

    if search_query:
        sections_qs = sections_qs.filter(
            models.Q(hsv_sects_stid__icontains=search_query) |
            models.Q(hsv_sects_name__icontains=search_query) |
            models.Q(hsv_sects_tmid__icontains=search_query) |
            models.Q(hsv_sects_crid__icontains=search_query)
        )

    sections_qs = sections_qs.order_by('hsv_sects_tmid')

    section_list = sections_qs[:2000]
    sections: List = []
    for section in section_list:
        sections.append(make_section_record(section))

    paginator = Paginator(sections, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'sis/section_list.html', context)

@login_required
def section_detail(request, section_stid):
    """View/edit individual course by CRID"""
    # Get course (SrlCours)
    record = make_section_detail_record(section_stid)
    persons = GumIdent.objects.using('sis').all()
    if request.method == 'POST':
        sects = record.sects
        try:
            with transaction.atomic(using='sis'):
                if sects:
                    sects.save(using='sis')
            messages.success(request, 'Course updated successfully.')
            return redirect('sis:section_detail', section_stid=section_stid)
        except Exception as e:
            messages.error(request, f'Error updating student: {e}')

    context = {
        'section': record,
        'persons': persons
    }
    return render(request, 'sis/section_detail.html', context)

@login_required
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
    if not record:
        return get_object_or_404(GumIdent, gum_ident_rbid=person_rbid)

    if request.method == 'POST':
        ident = record.gum_ident
        adinf = record.gum_adinf
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

# --- Create Views ---
@login_required
def section_create(request):
    courses = SrlCours.objects.using('sis').all().order_by('srl_cours_crid')
    courses = courses.filter(srl_cours_active_ind__exact='Y')
    terms = SglTerms.objects.using('sis').all().order_by('-sgl_terms_tmid')
    persons = GumIdent.objects.using('sis').all().order_by('gum_ident_last_name', 'gum_ident_first_name')

    if request.method == 'POST':
        
        try:
            course = None
            term = None
            prim_inst = None
            scnd_inst = None
            if request.POST.get('scnd_inst') != 'NULL':
                scnd_inst = request.POST.get('scnd_inst')
            course = request.POST.get('course')
            term = request.POST.get('term')
            prim_inst = request.POST.get('prim_inst')
            sect = SrbSects.objects.using('sis')
            with transaction.atomic(using='sis'):
                print (course + ' ' + term + ' ' + prim_inst)
                sect.create(srb_sects_crid_id=course, srb_sects_tmid_id=term, srb_sects_prim_inst_id=prim_inst, srb_sects_scnd_inst_id=scnd_inst)
            messages.success(request, 'Section created successfully.')
            return redirect('sis:section_create')
        except Exception as e:
            messages.error(request, f'Error creating section: {e}')

    context = {
        'courses': courses,
        'terms': terms,
        'persons': persons,
    }
    return render(request, 'sis/section_create.html', context)

def enrollment_create_term_select(request, student_id):
    person = GumIdent.objects.using('sis').select_related('gumadinf').filter(gum_ident_rbid=student_id).first()
    terms = SrhSterm.objects.using('sis').select_related('srh_sterm_tmid').filter(srh_sterm_rbid=student_id)

    if request.method == 'POST':
        tsid = request.POST.get('term')

        if not tsid:
            persons = GumIdent.objects.using('sis').filter(sgmstubi__isnull=False).order_by('gum_ident_last_name', 'gum_ident_first_name').distinct()
            messages.error(request, 'Please select a term.')
            return render(request, 'sis/enrollment_create_term_select.html', {
                'persons': persons,
            })
    
        return redirect('sis:enrollment_create', student_term_tsid=tsid)

    # Initial page load
    persons = GumIdent.objects.using('sis').filter(sgmstubi__isnull=False).order_by('gum_ident_last_name', 'gum_ident_first_name').distinct()
    return render(request, 'sis/enrollment_create_term_select.html', {'person': person,'terms': terms,})

def enrollment_create(request, student_term_tsid):
    sterm = SrhSterm.objects.using('sis').filter(srh_sterm_tsid=student_term_tsid).select_related('srh_sterm_rbid').first()
    term = sterm.srh_sterm_tmid_id
    sects = SrbSects.objects.using('sis').filter(srb_sects_tmid=term).select_related('srb_sects_crid').all()
    context = {
        'sterm': sterm,
        'sects': sects,
    }
    if request.method == 'POST':
        
        try:
            esid = 'RA'
            stid = request.POST.get('section')
            rbid = sterm.srh_sterm_rbid_id
            enrol = SrhEnrol.objects.using('sis')
            with transaction.atomic(using='sis'):
                print (rbid + ' ' + stid + ' ' + esid)
                enrol.create(srh_enrol_rbid_id=rbid, srh_enrol_stid_id=stid, srh_enrol_esid_id=esid)
            messages.success(request, 'Enrollment created successfully.')
            return redirect('sis:enrollment_create', student_term_tsid=student_term_tsid)
        except Exception as e:
            messages.error(request, f'Error creating enrollment: {e}')
    return render(request, 'sis/enrollment_create.html', context)