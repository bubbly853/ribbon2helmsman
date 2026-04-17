"""
SIS Views - Banner-style pages with campus per major support
Place this in /srv/ribbon2helmsman/helmsman/sis/views.py
"""
from django.db import models
from dataclasses import dataclass
from typing import Optional, List

from django.db import connections
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.urls import reverse
import datetime
from django.http import Http404

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
    HsvAudit,
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
class CurriculumRecord:
    curriculum_version_id: str 
    major_id: Optional[str]
    effective_term: Optional[str]
    name: Optional[str]
    type_id: Optional[str]
    type: Optional[str]
    mark_average: Optional[str]
    gpa_min: Optional[str]
    min_credits: Optional[str]

@dataclass
class MajorRecord:
    mrid: str
    name: Optional[str]
    short_name: Optional[str]
    college: Optional[str]
    degree: Optional[str]
    major_ind: Optional[str]
    minor_ind: Optional[str]
    cip: Optional[str]
    isced: Optional[HgvPrson] = None

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
    Build StudentDetail from HsvLtsts.
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
    else:
        raise Http404("Student does not exist")

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
    Build Course Record from HsvAllcr object.
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
    Build Course Detail from SrlCours and its select_related objects.
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
    else:
        raise Http404("Course does not exist")

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
    Build Section Record from HsvSects object.
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
    Build section Detail from SrbSects and its select_related objects.
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
    else:
        raise Http404("Section does not exist")


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
    Build Person Record from HsvPrson object.
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

def make_curriculum_record(crcrc: Optional[HsvCrcrc]) -> PersonRecord:
    """
    Build Curriculum Record from HsvCrcrc Object.
    """

    # --------------------
    # HsvCrcrc fields
    # --------------------
    curriculum_version_id = None
    major_id = None
    effective_term = None
    name = None
    type_id = None
    type = None
    mark_average = None
    gpa_min = None
    min_credits = None

    if crcrc:
        curriculum_version_id = crcrc.hsv_crcrc_cvid
        major_id = crcrc.hsv_crcrc_mrid
        effective_term = crcrc.hsv_crcrc_effective_term
        name = crcrc.hsv_crcrc_hr_name
        type_id = crcrc.hsv_crcrc_ctid
        type = crcrc.hsv_crcrc_curr_type
        mark_average = crcrc.hsv_crcrc_mark_avg
        gpa_min = crcrc.hsv_crcrc_min_gpa
        min_credits = crcrc.hsv_crcrc_min_credits

    return CurriculumRecord(
        curriculum_version_id=curriculum_version_id,
        major_id=major_id,
        effective_term=effective_term,
        name=name,
        type_id=type_id,
        type=type,
        mark_average=mark_average,
        gpa_min=gpa_min,
        min_credits=min_credits,
    )

def make_major_record(major: Optional[SclMajor]) -> PersonRecord:
    """
    Build Curriculum Record from HsvCrcrc Object.
    """

    # --------------------
    # SclMajor fields
    # --------------------
    mrid = None
    name = None
    short_name = None
    college = None
    degree = None
    major_ind = None
    minor_ind = None
    cip = None
    isced = None

    if major:
        mrid = major.scl_major_mrid
        name = major.scl_major_hr_name
        short_name = major.scl_major_short_name
        college = major.scl_major_cgid.sdl_coleg_hr_name
        degree = major.scl_major_dgid.scl_degrs_dgid
        major_ind = major.scl_major_major_ind
        minor_ind = major.scl_major_minor_ind
        cip = major.scl_major_ciid.scl_cipcd_hr_name if major.scl_major_ciid else None
        isced = major.scl_major_ifid.scl_iscdf_hr_name if major.scl_major_ifid else None


    return MajorRecord(
        mrid=mrid,
        name=name,
        short_name=short_name,
        college=college,
        degree=degree,
        major_ind=major_ind,
        minor_ind=minor_ind,
        cip=cip,
        isced=isced,
    )

# --- Search and Update Views ---
@login_required
def dashboard(request):
    """Main dashboard/home page"""
    cards = [
        {"url": reverse("sis:student_list"), "title": "Students", "desc": "View and manage student records", "icon": "👨‍🎓"},
        {"url": reverse("sis:person_list"), "title": "Persons",  "desc": "View and manage person records",  "icon": "🧑"},
        {"url": reverse("sis:course_list"), "title": "Courses",  "desc": "View and manage course records",  "icon": "📚"},
        {"url": reverse("sis:section_list"), "title": "Sections",  "desc": "View and manage section records",  "icon": "📅"},
        {"url": reverse("sis:curriculum_list"), "title": "Curriculums",  "desc": "View and manage curriculum",  "icon": "📋"},
        {"url": reverse("sis:curriculum_audit_student_select"), "title": "Degree Audit",  "desc": "View student degree audit",  "icon": "✅📋"},
        {"url": reverse("sis:term_list"), "title": "Terms",  "desc": "View and manage terms",  "icon": "🗓️"},
        {"url": reverse("sis:person_create"), "title": "Create Person",  "desc": "Create a person records",  "icon": "🧑✚"},
        {"url": reverse("sis:section_create"), "title": "Create Section",  "desc": "Create a new section record",  "icon": "📅✚"},
        {"url": reverse("sis:enrollment_create_student_select"), "title": "Create Enrollment",  "desc": "Enroll a student in a section",  "icon": "👨‍🎓📅✚"},
        {"url": reverse("sis:student_create_person_select"), "title": "Create Student Term Record",  "desc": "Create a term record for a student, creates a student record if needed",  "icon": "👨‍🎓✚"},
        {"url": reverse("sis:term_create"), "title": "Create Term",  "desc": "Create a term",  "icon": "🗓️✚"},
        {"url": reverse("sis:course_create"), "title": "Create Course",  "desc": "Create a course",  "icon": "📚✚"},
        {"url": reverse("sis:marks_enter_section_select"), "title": "Enter or Update Final Marks",  "desc": "Enter or update final marks for a section",  "icon": "✅📝"},
        {"url": "/admin/", "title": "Admin",  "desc": "Django administration panels",  "icon": "⚙️"},
    ]
    context = {
        'cards': cards,
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
        'curriculum_audit_student_select': 'sis/curriculum_audit_student_select.html'
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
def major_list(request):
    """List  majors with search and pagination"""
    search_query = request.GET.get('search', '').strip()
    rbid_query = request.GET.get('rbid', '').strip()
    url_name = request.resolver_match.url_name

    major_link_map = {
        'major_list': 'sis/major_list.html'
    }
    major_link = major_link_map.get(url_name, 'sis/major_list.html')

    # Base queryset: only majors that have a SGM_majr record
    majr_qs = SclMajor.objects.using('sis').all()

    # Search by name or RBID through GumIdent
    if search_query:
        majr_qs = majr_qs.filter(
            models.Q(scl_major_mrid__icontains=search_query) |
            models.Q(scl_major_hr_name__icontains=search_query) |
            models.Q(scl_major_shor_name__icontains=search_query)
        )

    # Order by last_name, first_name from GumIdent
    majr_qs = majr_qs.order_by(
        'scl_major_hr_name'
    )

    # Limit to 2000 results for safety
    majr_list = majr_qs[:2000]

    # Build major records
    majors: List = []
    for majr in majr_list:
        majors.append(make_major_record(majr))

    # Pagination
    paginator = Paginator(majors, 25)  # 25 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, major_link, context)

@login_required
def student_detail(request, student_rbid):
    """View/edit individual student by RBID"""
    # Build combined student record
    record = make_student_detail_record(student_rbid)

    if not record:
        raise Http404("Student does not exist")
    
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

    if request.method == 'POST':
        if 'stubi-post' in request.POST:
            stubi = record.sgm_stubi

            # use transaction to keep changes consistent
            try:
                active_ind = request.POST.get('active_ind')
                level = request.POST.get('level')
                stype = request.POST.get('stype')
                with transaction.atomic(using='sis'):
                    if stubi:
                        stubi.sgm_stubi_active_ind = active_ind
                        stubi.sgm_stubi_lvid_id = level
                        stubi.sgm_stubi_stid_id = stype
                        stubi.save(using='sis')

                messages.success(request, 'Student updated successfully.')
                return redirect('sis:student_detail', student_rbid=student_rbid)
            except Exception as e:
                messages.error(request, f'Error updating student: {e}')

        elif 'update_major' in request.POST:
            try:
                scid = request.POST.get('scid')
                cpid = request.POST.get('cpid')
                m_active_ind = stucv.scm_stucv_active_ind = request.POST.get('m_active_ind')
                stucv = ScmStucv.objects.using('sis').filter(
                    scm_stucv_scid=scid
                ).first()

                with transaction.atomic(using='sis'):
                    stucv.scm_stucv_cpid_id = cpid
                    stucv.scm_stucv_active_ind = m_active_ind
                    stucv.save()
                    messages.success(request, 'Major updated successfully.')
            except Exception as e:
                messages.error(request, f'Error updating major: {e}')

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

    if not record:
        raise Http404("Course does not exist")
    
    subjects = SrlSubjs.objects.using('sis').all()

    if request.method == 'POST':
        cours = record.cours
        try:
            name = request.POST.get('name')
            credit_hr = request.POST.get('credit_hr')
            active_ind = request.POST.get('active_ind')
            with transaction.atomic(using='sis'):
                if cours:
                    cours.srl_cours_hr_name = name
                    cours.srl_cours_credit_hours = credit_hr
                    cours.srl_cours_active_ind = active_ind
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
    """List all sections with search and pagination"""
    search_query = request.GET.get('search', '').strip()
    search_query = request.GET.get('search', '').strip()
    url_name = request.resolver_match.url_name

    section_link_map = {
        'section_list': 'sis/section_list.html',
        'marks_enter_section_select': 'sis/marks_enter_section_select.html',
    }

    section_link = section_link_map.get(url_name, 'sis/section_list.html')
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
    return render(request, section_link, context)

@login_required
def section_detail(request, section_stid):
    """View/edit individual section by STID"""
    # Get course (SrlCours)
    record = make_section_detail_record(section_stid)

    if not record:
        raise Http404("Section does not exist")
    
    persons = GumIdent.objects.using('sis').all()

    if request.method == 'POST':
        sects = record.sects
        try:
            prim_inst = request.POST.get('prim_inst')
            scnd_inst = v_scnd_inst if (v_scnd_inst := request.POST.get('scnd_inst')) != 'NULL' else None
            with transaction.atomic(using='sis'):
                sects.srb_sects_prim_inst_id = prim_inst
                sects.srb_sects_scnd_inst_id = scnd_inst
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
    """List all persons with search and pagination"""
    search_query = request.GET.get('search', '').strip()
    rbid_query = request.GET.get('rbid', '').strip()
    url_name = request.resolver_match.url_name
    person_link_map = {
        'person_list': 'sis/person_list.html',
        'student_create_person_select': 'sis/student_create_person_select.html',
    }
    person_link = person_link_map.get(url_name, 'sis/person_list.html')


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
    return render(request, person_link, context)

@login_required
def person_detail(request, person_rbid):
    """View/edit individual person by RBID"""
    ident = GumIdent.objects.using('sis').filter(gum_ident_rbid=person_rbid).first()
    adinf = GumAdinf.objects.using('sis').filter(gum_adinf_rbid_id=person_rbid).first()
    countries = GglCount.objects.using('sis').all().order_by('ggl_count_hr_name')
    craces = GrlRcens.objects.using('sis').all().order_by('grl_rcens_hr_name')
    draces = GrlRdetl.objects.using('sis').all().order_by('grl_rdetl_hr_name')
    czcodes = GglCitzn.objects.using('sis').all().order_by('ggl_citzn_hr_name')

    if not ident:
        raise Http404("Person Base Record does not exist")
    
    if not adinf:
        raise Http404("Person Aditional Info Record does not exist")

    if request.method == 'POST':
        try:
            preferred_name = request.POST.get('preferred_name') if request.POST.get('preferred_name') != '' else None
            prefix = request.POST.get('prefix') if request.POST.get('prefix') != '' else None
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name') if request.POST.get('middle_name') != '' else None
            last_name = request.POST.get('last_name')
            suffix = request.POST.get('suffix') if request.POST.get('suffix') != '' else None
            birthday = datetime.datetime.strptime(request.POST.get('birthday'), '%Y-%m-%d').date()
            id_num = request.POST.get('id_num')
            id_country = request.POST.get('id_country')
            username = request.POST.get('username') if request.POST.get('username') != '' else None
            rcid = request.POST.get('rcid')
            hispanic = request.POST.get('hispanic')
            rdid1 = request.POST.get('rdid1')
            rdid2 = request.POST.get('rdid2') if request.POST.get('rdid2') != 'NULL' else None
            czid = request.POST.get('czid')
            legal_country = request.POST.get('legal_country')
            with transaction.atomic(using='sis'):
                if ident:
                    ident.gum_ident_first_name = first_name
                    ident.gum_ident_middle_name = middle_name
                    ident.gum_ident_last_name = last_name
                    ident.gum_ident_birthday = birthday
                    ident.gum_ident_idnum = id_num
                    ident.gum_ident_id_coid_id = id_country
                    ident.save(using='sis')
                if adinf:
                    adinf.gum_adinf_pref_first_name = preferred_name
                    adinf.gum_adinf_prefix = prefix
                    adinf.gum_adinf_suffix = suffix
                    adinf.gum_adinf_username = username
                    adinf.gum_adinf_rcid_id = rcid
                    adinf.gum_adinf_hispanic_ind = hispanic
                    adinf.gum_adinf_rdid_1_id = rdid1
                    adinf.gum_adinf_rdid_2_id =rdid2
                    adinf.gum_adinf_czid_id = czid
                    adinf.gum_adinf_citizen_coid_id = legal_country
                    adinf.save(using='sis')

            messages.success(request, 'Persson updated successfully.')
            return redirect('sis:person_detail', person_rbid=person_rbid)
        except Exception as e:
            messages.error(request, f'Error updating student: {e}')

    context = {
        'ident': ident,
        'adinf': adinf,
        'countries': countries,
        'craces': craces,
        'draces': draces,
        'czcodes': czcodes
    }
    return render(request, 'sis/person_detail.html', context)

@login_required
def curriculum_list(request):
    """List  students with search and pagination"""
    search_query = request.GET.get('search', '').strip()
    url_name = request.resolver_match.url_name
    curriculum_link_map = {
        'curriculum_list': 'sis/curriculum_list.html',
    }
    curriculum_link = curriculum_link_map.get(url_name, 'sis/curriculum_list.html')

    crcrc_qs = HsvCrcrc.objects.using('sis').all()

    # Search by name or RBID through HsvCrcrc
    if search_query:
        crcrc_qs = crcrc_qs.filter(
            models.Q(hsv_crcrc_cvid__contains=search_query) |
            models.Q(hsv_crcrc_mrid__contains=search_query) |
            models.Q(hsv_crcrc_hr_name__icontains=search_query)
        )

    # Order by major name HsvCrcrc
    crcrc_qs = crcrc_qs.order_by(
        'hsv_crcrc_hr_name'
    )

    # Limit to 2000 results for safety
    crcrc_list = crcrc_qs[:2000]

    # Build student records
    curriculums: List = []
    for crcrc in crcrc_list:
        curriculums.append(make_curriculum_record(crcrc))

    # Pagination
    paginator = Paginator(curriculums, 25)  # 25 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, curriculum_link, context)

@login_required
def curriculum_audit_curriculum_select(request, student_id):
    stucv = ScmStucv.objects.using('sis').filter(scm_stucv_rbid=student_id).all()
    ident = GumIdent.objects.using('sis').filter(gum_ident_rbid=student_id).first()
    if not stucv:
        raise Http404("Curriculum does not exist")
    context = {
        'ident': ident,
        'stucvs': stucv,
    }
    return render(request, 'sis/curriculum_audit_curriculum_select.html', context)

@login_required
def curriculum_detail(request, curriculum_cvid):
    """View/edit individual curriculum by CVID"""
    currv = SclCurrv.objects.using('sis').filter(
        scl_currv_cvid=curriculum_cvid
    ).first()

    if not currv:
        raise Http404("Curriculum does not exist")
    
    creqs = ScrCreqs.objects.using('sis').filter(
        scr_creqs_cvid_id=curriculum_cvid
    ).all().order_by(
        'scr_creqs_rtid__srl_rqtyp_hr_name',
        'scr_creqs_crid__srl_cours_hr_name'
    )

    rqgrps= ScrRqgrp.objects.using('sis').filter(
        scr_rqgrp_cvid=curriculum_cvid
    ).all().order_by('scr_rqgrp_hr_name')

    grqtyps = SrlRqtyp.objects.using('sis').filter(
        srl_rqtyp_group_ind='Y'
    ).all().order_by('srl_rqtyp_hr_name')

    rqtyps = SrlRqtyp.objects.using('sis').all().order_by('srl_rqtyp_hr_name')

    crtyps = SclCrtyp.objects.using('sis').all().order_by('scl_crtyp_hr_name')
    
    terms = SglTerms.objects.using('sis').all().order_by('sgl_terms_hr_name')

    marks = StlMarks.objects.using('sis').all().order_by('stl_marks_mkid')

    courses = SrlCours.objects.using('sis').all().order_by('srl_cours_hr_name')
    context = {
        'currv': currv,
        'creqs': creqs,
        'rqtyps': rqtyps,
        'grqtyps': grqtyps,
        'rqgrps': rqgrps,
        'crtyps': crtyps,
        'terms': terms,
        'marks': marks,
        'courses': courses,
        'cvid': curriculum_cvid
    }

    if request.method == 'POST':
        if 'update_currv' in request.POST:
            try:
                um_currv = SclCurrv.objects.using('sis').filter(
                scl_currv_cvid=curriculum_cvid
            ).first()
                um_eff_term = request.POST.get('eff_term')
                um_crtyp = request.POST.get('crtyp')
                um_end_term = v_term if (v_term := request.POST.get('end_term')) != 'NULL' else None
                um_marks = float(v_mark) if (v_mark := request.POST.get('mark_avg')) != '' else None
                um_gpa = float(v_gpa) if (v_gpa := request.POST.get('min_gpa')) != '' else None
                um_credits = float(v_credit) if (v_credit := request.POST.get('min_credits')) != '' else None               
                with transaction.atomic(using='sis'):
                    um_currv.scl_currv_ctid_id=um_crtyp
                    um_currv.scl_currv_effective_term_id=um_eff_term
                    um_currv.scl_currv_end_term_id=um_end_term
                    um_currv.scl_currv_min_mark_avg=um_marks
                    um_currv.scl_currv_min_gpa=um_gpa
                    um_currv.scl_currv_min_credits=um_credits
                    um_currv.save()
                    messages.success(request, 'Curriculum updated successfully.')
                    return redirect('sis:curriculum_detail', curriculum_cvid=curriculum_cvid)
            except Exception as e:
                messages.error(request, f'Error updating curriculum: {e}')

        if 'update_creq' in request.POST:
            try:
                uc_creqs = ScrCreqs.objects.using('sis').filter(
                    scr_creqs_rqid=request.POST.get('rqid')
                ).first()
                uc_type = request.POST.get('creq_rtid')
                uc_marks = float(v_mark) if (v_mark := request.POST.get('min_creq_mark_avg')) != '' else None
                uc_mkid = v_mkid if (v_mkid := request.POST.get('min_creq_letter_mark')) != 'NULL' else None
                uc_credits = float(v_credit) if (v_credit := request.POST.get('min_creq_credits')) != '' else None
                with transaction.atomic(using='sis'):
                    uc_creqs.scr_cres_rtid=uc_type
                    uc_creqs.scr_creqs_min_mark_avg=uc_marks
                    uc_creqs.scr_creqs_min_mkid=uc_mkid
                    uc_creqs.scr_creqs_min_credits=uc_credits
                    uc_creqs.save()
                messages.success(request, 'Requirement updated successfully.')
                return redirect('sis:curriculum_detail', curriculum_cvid=curriculum_cvid)
            except Exception as e:
                messages.error(request, f'Error updating requirement: {e}')

        if 'create_creq' in request.POST:
            try:
                cc_creqs = ScrCreqs.objects.using('sis')
                cc_crid =  request.POST.get('creq_crid')
                cc_type = request.POST.get('creq_rtid')
                cc_marks = float(v_mark) if (v_mark := request.POST.get('min_creq_mark_avg')) != '' else None
                cc_mkid = v_mkid if (v_mkid := request.POST.get('min_creq_letter_mark')) != 'NULL' else None
                cc_credits = float(v_credit) if (v_credit := request.POST.get('min_creq_credits')) != '' else None
                with transaction.atomic(using='sis'):
                    cc_creqs.create(scr_creqs_cvid_id=curriculum_cvid, scr_creqs_crid_id=cc_crid, scr_creqs_rtid_id=cc_type, scr_creqs_min_credits=cc_credits, scr_creqs_min_mkid_id=cc_mkid, scr_creqs_min_mark_avg=cc_marks)
                messages.success(request, 'Requirement created successfully.')
                return redirect('sis:curriculum_detail', curriculum_cvid=curriculum_cvid)
            except Exception as e:
                messages.error(request, f'Error creating requirement: {e}')

        if 'update_rqgrp' in request.POST:
            try:
                ug_rqgrp = ScrRqgrp.objects.using('sis').filter(
                    scr_rqgrp_rgid=request.POST.get('rgid')
                ).first()
                ug_name =  request.POST.get('rqgrp_name')
                ug_type = request.POST.get('rqgrp_rtid')
                ug_courses = float(v_course) if (v_course := request.POST.get('min_grp_courses')) != '' else None
                ug_credits = float(v_credit) if (v_credit := request.POST.get('min_grp_credits')) != '' else None
                ug_marks = float(v_mark) if (v_mark := request.POST.get('min_grp_mark')) != '' else None
                print(ug_type)
                with transaction.atomic(using='sis'):
                    ug_rqgrp.scr_rqgrp_rtid_id=ug_type
                    ug_rqgrp.scr_rqgrp_hr_name=ug_name
                    ug_rqgrp.scr_rqgrp_min_courses=ug_courses
                    ug_rqgrp.scr_rqgrp_min_credits=ug_credits
                    ug_rqgrp.scr_rqgrp_min_mark_avg=ug_marks
                    ug_rqgrp.save()
                messages.success(request, 'Requirement updated successfully.')
                return redirect('sis:curriculum_detail', curriculum_cvid=curriculum_cvid)
            except Exception as e:
                messages.error(request, f'Error updating requirement: {e}')

        if 'create_rqgrp' in request.POST:
            try:
                cg_rqgrp = ScrRqgrp.objects.using('sis')
                cg_name =  request.POST.get('rqgrp_name')
                cg_type = request.POST.get('rqgrp_rtid')
                cg_courses = float(v_course) if (v_course := request.POST.get('min_grp_courses')) != '' else None
                cg_credits = float(v_credit) if (v_credit := request.POST.get('min_grp_credits')) != '' else None
                cg_marks = float(v_mark) if (v_mark := request.POST.get('min_grp_mark')) != '' else None
                with transaction.atomic(using='sis'):
                    cg_rqgrp.create(scr_rqgrp_cvid_id=curriculum_cvid, scr_rqgrp_rtid_id=cg_type, scr_rqgrp_hr_name=cg_name, scr_rqgrp_min_courses=cg_courses, scr_rqgrp_min_credits=cg_credits, scr_rqgrp_min_mark_avg=cg_marks)
                messages.success(request, 'Group created successfully.')
                return redirect('sis:curriculum_detail', curriculum_cvid=curriculum_cvid)
            except Exception as e:
                messages.error(request, f'Error creating group: {e}')

    
    return render(request, 'sis/curriculum_detail.html', context)

@login_required
def term_list(request):
    """List terms with search and pagination"""
    search_query = request.GET.get('search', '').strip()
    url_name = request.resolver_match.url_name
    term_link_map = {
        'term_list': 'sis/term_list.html',
    }
    term_link = term_link_map.get(url_name, 'sis/student_list.html')

    # Base queryset:
    terms_qs = SglTerms.objects.using('sis').all()

    # Search by name or RBID through GumIdent
    if search_query:
        terms_qs = terms_qs.filter(
            models.Q(sgl_terms_tmid__icontains=search_query) |
            models.Q(sgl_terms_year__icontains=search_query) |
            models.Q(sgl_terms_hr_name__icontains=search_query)
        )

    # Order by tmid
    terms_qs = terms_qs.order_by(
        'sgl_terms_tmid',
    )

    # Limit to 2000 results for safety
    term_list = terms_qs[:2000]

    # Build term records
    terms: List = []
    for term in term_list:
        terms.append(SglTerms.objects.using('sis').filter(sgl_terms_tmid=term.sgl_terms_tmid).first())

    # Pagination
    paginator = Paginator(terms, 25)  # 25 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, term_link, context)

@login_required
def term_detail(request, term_tmid):
    """View/edit individual term by TMID"""
    term = SglTerms.objects.using('sis').filter(sgl_terms_tmid=term_tmid).first()

    if not term:
       raise Http404("Term does not exist")
    
    fyears = FglFyear.objects.using('sis').all().order_by('fgl_fyear_fyid')

    if request.method == 'POST':
        try:
            with transaction.atomic(using='sis'):
                if term:
                    term.sgl_terms_year = request.POST.get('year', term.sgl_terms_year)
                    term.sgl_terms_start_date = datetime.datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
                    term.sgl_terms_end_date = datetime.datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()
                    term.save(using='sis')
            messages.success(request, 'Term updated successfully.')
            return redirect('sis:term_detail', term_tmid=term_tmid)
        except Exception as e:
            messages.error(request, f'Error updating term: {e}')

    context = {
        'term': term,
        'fyears': fyears,
    }
    return render(request, 'sis/term_detail.html', context)

@login_required
def marks_enter(request, section_stid):
    """View and enter marks per section"""                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    enrol = SrhEnrol.objects.using('sis').filter(
        srh_enrol_stid_id=section_stid
    ).select_related(
        'srh_enrol_rbid__gumadinf',
        'sthcrtrn'
    ).order_by(
        'srh_enrol_rbid__gum_ident_last_name',
        'srh_enrol_rbid__gumadinf__gum_adinf_pref_first_name',
        'srh_enrol_rbid__gum_ident_first_name'
    ).all()

    if not enrol:
       raise Http404("Enrollments do not exist")

    marks = StlMarks.objects.using('sis').all().order_by('stl_marks_mkid')
    context = {
        'enrol': enrol,
        'stid': section_stid,
        'marks': marks
    }

    if request.method == 'POST':
        i = 1
        errors = []
        while True:
            erid = request.POST.get(f'erid_{i}')
            stid = section_stid
            rbid = request.POST.get(f'rbid_{i}')
            if erid is None:
                break

            mark_avg  = request.POST.get(f'mark_avg_{i}') or None
            final_mkid = request.POST.get(f'final_mkid_{i}') if request.POST.get(f'final_mkid_{i}') != 'NULL' else None

            try:
                SthCrtrn.objects.using('sis').update_or_create(
                    sth_crtrn_erid_id=erid,
                    sth_crtrn_rbid_id=rbid,
                    sth_crtrn_stid_id=stid,
                    defaults={
                        'sth_crtrn_final_mark_avg': mark_avg,
                        'sth_crtrn_final_mkid_id': final_mkid,
                    }
                )
            except Exception as e:
                errors.append(f'Row {i} (erid {erid}): {e}')
            
            i += 1

        if errors:
            for error in errors:
                messages.error(request, f'Error updating marks: {error}')
        else:
            messages.success(request, 'marks updated successfully.')
        return redirect('sis:marks_enter', section_stid=section_stid)
    
    return render(request, 'sis/marks_enter.html', context)

@login_required
def major_detail(request, major_mrid):
    """View or Manage a Major"""
    major = SclMajor.objects.using('sis').filter(scl_major_mrid=major_mrid).first()

    if not major:
       raise Http404("Enrollments do not exist")
    
    colegs = SdlColeg.objects.using('sis').all().order_by('sdl_coleg_hr_name')
    degrs = SclDegrs.objects.using('sis').all().order_by('scl_degrs_hr_name')
    cicpds = SclCipcd.objects.using('sis').all().order_by('scl_cipcd_hr_name')
    iscdfs = SclIscdf.objects.using('sis').all().order_by('scl_iscdf_hr_name')
    

    if request.method == 'POST':
        try:
            sname = request.POST.get('sname')
            cgid = request.POST.get('cgid')
            dgid = request.POST.get('dgid')
            major_ind = request.POST.get('major_ind')
            minor_ind = request.POST.get('minor_ind')
            ciid = v_ciid if (v_ciid := request.POST.get('ciid')) != 'NULL' else None
            ifid = v_ifid if (v_ifid := request.POST.get('ifid')) != 'NULL' else None
            with transaction.atomic(using='sis'):
                major.scl_major_short_name=sname
                major.scl_major_cgid_id=cgid
                major.scl_major_dgid_id=dgid
                major.scl_major_major_ind=major_ind
                major.scl_major_minor_ind=minor_ind
                major.scl_major_ciid_id=ciid
                major.scl_major_ifid_id=ifid
            messages.success(request, 'Major updated successfully.')
            return redirect('sis:major_detail', major_mrid=major_mrid)
        except Exception as e:
            messages.error(request, f'Error updating major: {e}')

    context = {
        'major': major,
        'colegs': colegs,
        'degrs': degrs,
        'cicpds': cicpds,
        'iscdfs': iscdfs,
    }
    return render(request, 'sis/major_detail.html', context)

@login_required
def curriculum_audit(request, stucv_scid):
    stucv=ScmStucv.objects.using('sis').filter(scm_stucv_scid=stucv_scid).first()

    if not stucv:
       raise Http404("Curriculum does not exist")

    ident=GumIdent.objects.using('sis').filter(gum_ident_rbid=stucv.scm_stucv_rbid_id).first()
    rqgrp=ScrRqgrp.objects.using('sis').filter(scr_rqgrp_cvid_id=stucv.scm_stucv_cvid_id).all().order_by('scr_rqgrp_hr_name')
    audit=HsvAudit.objects.using('sis').filter(hsv_audit_scid=stucv_scid).all().order_by('hsv_audit_sbid', 'hsv_audit_crse_numb')
    context = {
        'stucv': stucv,
        'ident': ident,
        'rqgrps': rqgrp,
        'audits': audit,
    }
    return render(request, 'sis/curriculum_audit.html', context)

# --- Create Views ---
@login_required
def person_create(request):
    """Create a person"""
    countries = GglCount.objects.using('sis').all().order_by('ggl_count_hr_name')
    craces = GrlRcens.objects.using('sis').all().order_by('grl_rcens_hr_name')
    draces = GrlRdetl.objects.using('sis').all().order_by('grl_rdetl_hr_name')
    czcodes = GglCitzn.objects.using('sis').all().order_by('ggl_citzn_hr_name')
    if request.method == 'POST':
        preferred_name = request.POST.get('preferred_name') if request.POST.get('preferred_name') != '' else None
        prefix = request.POST.get('prefix') if request.POST.get('prefix') != '' else None
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name') if request.POST.get('middle_name') != '' else None
        last_name = request.POST.get('last_name')
        suffix = request.POST.get('suffix') if request.POST.get('suffix') != '' else None
        birthday = datetime.datetime.strptime(request.POST.get('birthday'), '%Y-%m-%d').date()
        id_num = request.POST.get('id_num')
        id_country = request.POST.get('id_country')
        username = request.POST.get('username') if request.POST.get('username') != '' else None
        rcid = request.POST.get('rcid')
        hispanic = request.POST.get('hispanic')
        rdid1 = request.POST.get('rdid1')
        rdid2 = request.POST.get('rdid2') if request.POST.get('rdid2') != 'NULL' else None
        czid = request.POST.get('czid')
        legal_country = request.POST.get('legal_country')
        try:
            ident = GumIdent.objects.using('sis')
            adinf = GumAdinf.objects.using('sis')

            print({
                "preferred_name": preferred_name,
                "prefix": prefix,
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "suffix": suffix,
                "birthday": birthday,
                "id_num": id_num,
                "id_country": id_country,
                "username": username,
                "rcid": rcid,
                "rdid1": rdid1,
                "rdid2": rdid2,
                "czid": czid,
                "legal_country": legal_country,
            })
            with transaction.atomic(using='sis'):
                new_rbid = None
                with connections['sis'].cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO general.gum_ident 
                        (gum_ident_first_name, gum_ident_middle_name, gum_ident_last_name, 
                        gum_ident_birthday, gum_ident_idnum, gum_ident_id_coid)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING gum_ident_rbid
                    """, [first_name, middle_name, last_name, birthday, id_num, id_country])
                    
                    new_rbid = cursor.fetchone()[0]
                adinf.create(gum_adinf_rbid_id=new_rbid, gum_adinf_pref_first_name=preferred_name, gum_adinf_prefix=prefix, gum_adinf_suffix=suffix, gum_adinf_username=username, gum_adinf_rcid_id=rcid, gum_adinf_hispanic_ind=hispanic, gum_adinf_rdid_1_id=rdid1, gum_adinf_rdid_2_id=rdid2, gum_adinf_czid_id=czid, gum_adinf_citizen_coid_id=legal_country)
            messages.success(request, 'Person created successfully.')
            return redirect('sis:person_create')
        except Exception as e:
            messages.error(request, f'Error creating person: {e}')

    context = {
        'countries': countries,
        'craces': craces,
        'draces': draces,
        'czcodes': czcodes,
    }
    return render(request, 'sis/person_create.html', context)

@login_required
def section_create(request):
    """Create a section"""
    courses = SrlCours.objects.using('sis').all().order_by('srl_cours_crid')
    courses = courses.filter(srl_cours_active_ind__exact='Y')
    terms = SglTerms.objects.using('sis').all().order_by('-sgl_terms_tmid')
    persons = GumIdent.objects.using('sis').all().order_by('gum_ident_last_name', 'gum_ident_first_name')

    if request.method == 'POST':
        
        try:
            sect = SrbSects.objects.using('sis')
            scnd_inst = v_scnd_inst if (v_scnd_inst := request.POST.get('scnd_inst')) != 'NULL' else None
            course = request.POST.get('course')
            term = request.POST.get('term')
            prim_inst = request.POST.get('prim_inst')
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

@login_required
def course_create(request):
    """Create a Course"""
    subjs = SrlSubjs.objects.using('sis').all().order_by('srl_subjs_sbid')

    if request.method == 'POST':
        
        try:
            cours = SrlCours.objects.using('sis')
            subj = request.POST.get('subj')
            numb = request.POST.get('numb')
            name = request.POST.get('name')
            credit_hrs = request.POST.get('credit_hrs')
            with transaction.atomic(using='sis'):
                cours.create(srl_cours_sbid_id=subj, srl_cours_crse_num=numb, srl_cours_hr_name=name, srl_cours_credit_hours=credit_hrs, srl_cours_active_ind='Y')
            messages.success(request, 'Course created successfully.')
            return redirect('sis:course_create')
        except Exception as e:
            messages.error(request, f'Error creating course: {e}')

    context = {
        'subjs': subjs,
    }
    return render(request, 'sis/course_create.html', context)

@login_required
def enrollment_create_term_select(request, student_id):
    """For a student, select an available enrollment term"""
    person = GumIdent.objects.using('sis').select_related('gumadinf').filter(gum_ident_rbid=student_id).first()

    if not person:
       raise Http404("Person does not exist")

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

@login_required
def enrollment_create(request, student_term_tsid):
    """Create an enrollment for a student term TSID"""
    sterm = SrhSterm.objects.using('sis').filter(srh_sterm_tsid=student_term_tsid).select_related('srh_sterm_rbid').first()

    if not sterm:
       raise Http404("Student does not exist for the term")

    person = GumIdent.objects.using('sis').select_related('gumadinf').filter(gum_ident_rbid=sterm.srh_sterm_rbid_id).first()
    term = sterm.srh_sterm_tmid_id
    sects = SrbSects.objects.using('sis').filter(srb_sects_tmid=term).select_related('srb_sects_crid').all()
    context = {
        'person': person,
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

@login_required
def student_create_term_select(request, person_rbid):
    """Select a term for a person by RBID, creating a student record"""
    person = GumIdent.objects.using('sis').select_related('gumadinf').filter(gum_ident_rbid=person_rbid).first()

    if not person:
       raise Http404("Person does not exist")
    
    srh_tmids = SrhSterm.objects.using('sis').filter(srh_sterm_rbid=person_rbid).values_list('srh_sterm_tmid', flat=True)
    terms = SglTerms.objects.using('sis').exclude(sgl_terms_tmid__in=srh_tmids)
    if request.method == 'POST':
        tmid = request.POST.get('term')

        if not tmid:
            messages.error(request, 'Please select a term.')
            return render(request, 'sis/student_create_term_select.html', {
                'person': person,
            })
        
        if tmid == "NULL":
            messages.error(request, 'Student record found for all available terms.')
            return render(request, 'sis/student_create_term_select.html', {
                'person': person,
            })
        try:
            rbid = person.gum_ident_rbid
            tmid = tmid
            sterm = SrhSterm.objects.using('sis')
            with transaction.atomic(using='sis'):
                sterm.create(srh_sterm_rbid_id=rbid, srh_sterm_tmid_id=tmid, srh_sterm_rgid_id='NS')
            messages.success(request, 'Student term record created successfully.')
        except Exception as e:
            messages.error(request, f'Error creating stduent_record: {e}')
    
        return render(request, 'sis/student_create_term_select.html', {'person': person,'terms': terms,})

    return render(request, 'sis/student_create_term_select.html', {'person': person,'terms': terms,})

@login_required
def term_create(request):
    """Create term"""
    smstrs = SglSmstr.objects.using('sis').all().order_by('sgl_smstr_smid')
    fyears = FglFyear.objects.using('sis').all().order_by('fgl_fyear_fyid')

    if request.method == 'POST':
        try:
            year = None
            smid = None
            name = None
            fyid = None
            start_date = None
            end_date = None

            year = request.POST.get('year')
            smid = request.POST.get('smid')
            name = request.POST.get('name')
            fyid = request.POST.get('fyid')
            start_date = datetime.datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()
            terms=SglTerms.objects.using('sis')
            with transaction.atomic(using='sis'):
                terms.create(sgl_terms_year=year, sgl_terms_smid_id=smid, sgl_terms_hr_name=name, sgl_terms_fyid=fyid, sgl_terms_start_date=start_date, sgl_terms_end_date=end_date)
            messages.success(request, 'Term created successfully.')
            return redirect('sis:term_create')
        except Exception as e:
            messages.error(request, f'Error creating term: {e}')

    context = {
        'fyears': fyears,
        'smstrs': smstrs,
        'today': datetime.date.today().isoformat(),
    }
    return render(request, 'sis/term_create.html', context)

@login_required
def major_create(request):
    """Create a Major"""
    colegs = SdlColeg.objects.using('sis').all().order_by('sdl_coleg_hr_name')
    degrs = SclDegrs.objects.using('sis').all().order_by('scl_degrs_hr_name')
    cicpds = SclCipcd.objects.using('sis').all().order_by('scl_cipcd_hr_name')
    iscdfs = SclIscdf.objects.using('sis').all().order_by('scl_iscdf_hr_name')
    

    if request.method == 'POST':
        
        try:
            major = SclMajor.objects.using('sis')
            mrid = request.POST.get('mrid')
            name = request.POST.get('name')
            sname = request.POST.get('sname')
            cgid = request.POST.get('cgid')
            dgid = request.POST.get('dgid')
            major_ind = request.POST.get('major_ind')
            minor_ind = request.POST.get('minor_ind')
            ciid = v_ciid if (v_ciid := request.POST.get('ciid')) != 'NULL' else None
            ifid = v_ifid if (v_ifid := request.POST.get('ifid')) != 'NULL' else None
            with transaction.atomic(using='sis'):
                major.create(scl_major_mrid=mrid, scl_major_hr_name=name, scl_major_short_name=sname, scl_major_cgid_id=cgid, scl_major_dgid_id=dgid, scl_major_major_ind=major_ind, scl_major_minor_ind=minor_ind, scl_major_ciid_id=ciid, scl_major_ifid_id=ifid)
            messages.success(request, 'Major created successfully.')
            return redirect('sis:major_create')
        except Exception as e:
            messages.error(request, f'Error creating major: {e}')

    context = {
        'colegs': colegs,
        'degrs': degrs,
        'cicpds': cicpds,
        'iscdfs': iscdfs,
    }
    return render(request, 'sis/major_create.html', context)