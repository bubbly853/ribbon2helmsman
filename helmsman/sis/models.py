# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FglFyear(models.Model):
    fgl_fyear_fyid = models.CharField(primary_key=True, max_length=4, db_comment='Financial aid year code.')
    fgl_fyear_desc = models.CharField(max_length=40, db_comment='Financial aid year description.')

    class Meta:
        managed = False
        db_table = '"finance"."fgl_fyear"'
        db_table_comment = 'Financial aid year definition table.'


class GglCitzn(models.Model):
    ggl_citzn_czid = models.CharField(primary_key=True, max_length=4, db_comment='Citizenship ID')
    ggl_citzn_hr_name = models.CharField(max_length=64, db_comment='Citizenship human readable name')
    ggl_citzn_study_visa_ind = models.CharField(max_length=1, blank=True, null=True, db_comment='Indicates if this citizenship status reqires study/student visa')
    ggl_citzn_employ_visa_ind = models.CharField(max_length=1, blank=True, null=True, db_comment='Indicates if this citizenship status reqires employment visa')

    class Meta:
        managed = False
        db_table = '"general"."ggl_citzn"'
        db_table_comment = 'Citizenship lookup table.'


class GglCount(models.Model):
    ggl_count_coid = models.CharField(primary_key=True, max_length=2, db_comment='Country ID, Alpha-2 code.')
    ggl_count_hr_name = models.CharField(max_length=64, db_comment='Country human-readable name.')

    class Meta:
        managed = False
        db_table = '"general"."ggl_count"'
        db_table_comment = 'Country definition table.'


class GrlRcens(models.Model):
    grl_rcens_rcid = models.CharField(primary_key=True, max_length=4, db_comment='Census Race ID')
    grl_rcens_hr_name = models.CharField(max_length=64, db_comment='Census Race human readable name')
    grl_rcens_govt_1 = models.CharField(max_length=23, blank=True, null=True, db_comment='Census Race additional government/reporting field 1.')
    grl_rcens_govt_2 = models.CharField(max_length=23, blank=True, null=True, db_comment='Census Race additional government/reporting field 2.')
    grl_rcens_govt_3 = models.CharField(max_length=23, blank=True, null=True, db_comment='Census Race additional government/reporting field 3.')

    class Meta:
        managed = False
        db_table = '"general"."grl_rcens"'
        db_table_comment = 'Census/Goverment Race lookup table'


class GrlRdetl(models.Model):
    grl_rdetl_rdid = models.CharField(primary_key=True, max_length=4, db_comment='Race Detail ID')
    grl_rdetl_hr_name = models.CharField(max_length=64, db_comment='Race Detail human readable name')
    grl_rdetl_rcid = models.ForeignKey(GrlRcens, models.DO_NOTHING, db_column='grl_rdetl_rcid', blank=True, null=True, db_comment='Census Race ID associated with Race Detail Code')

    class Meta:
        managed = False
        db_table = '"general"."grl_rdetl"'
        db_table_comment = 'Race Detail lookup table'


class GumAdinf(models.Model):
    gum_adinf_rbid = models.OneToOneField('GumIdent', models.DO_NOTHING, db_column='gum_adinf_rbid', primary_key=True, db_comment='Ribbon ID (foreign key to gum_ident).')
    gum_adinf_pref_first_name = models.CharField(max_length=32, blank=True, null=True, db_comment='Preferred first name (may differ from legal name).')
    gum_adinf_prefix = models.CharField(max_length=16, blank=True, null=True, db_comment='Name prefix (e.g., Mr., Mrs., Dr.).')
    gum_adinf_suffix = models.CharField(max_length=16, blank=True, null=True, db_comment='Name suffix (e.g., Jr., Sr., III).')
    gum_adinf_username = models.CharField(unique=True, max_length=16, blank=True, null=True, db_comment='System username for authentication.')
    gum_adinf_rcid = models.ForeignKey(GrlRcens, models.DO_NOTHING, db_column='gum_adinf_rcid', blank=True, null=True, db_comment='Census race ID (for government reporting).')
    gum_adinf_hispanic_ind = models.CharField(max_length=1, blank=True, null=True, db_comment='Hispanic/Latino ethnicity indicator (Y/N).')
    gum_adinf_rdid_1 = models.ForeignKey(GrlRdetl, models.DO_NOTHING, db_column='gum_adinf_rdid_1', blank=True, null=True, db_comment='Primary race detail ID.')
    gum_adinf_rdid_2 = models.ForeignKey(GrlRdetl, models.DO_NOTHING, db_column='gum_adinf_rdid_2', related_name='gumadinf_gum_adinf_rdid_2_set', blank=True, null=True, db_comment='Secondary race detail ID (for multi-racial individuals).')
    gum_adinf_rdid_3 = models.ForeignKey(GrlRdetl, models.DO_NOTHING, db_column='gum_adinf_rdid_3', related_name='gumadinf_gum_adinf_rdid_3_set', blank=True, null=True, db_comment='Tertiary race detail ID (for multi-racial individuals).')
    gum_adinf_czid = models.ForeignKey(GglCitzn, models.DO_NOTHING, db_column='gum_adinf_czid', blank=True, null=True, db_comment='Citizenship status ID.')
    gum_adinf_citizen_coid = models.ForeignKey(GglCount, models.DO_NOTHING, db_column='gum_adinf_citizen_coid', blank=True, null=True, db_comment='Country of citizenship (foreign key to ggl_count).')
    gum_adinf_created_date = models.DateField(db_comment='Date record was created.')
    gum_adinf_activity_date = models.DateField(blank=True, null=True, db_comment='Date record was last modified.')
    gum_adinf_modified_by = models.CharField(max_length=40, blank=True, null=True, db_comment='User who last modified record.')

    class Meta:
        managed = False
        db_table = '"general"."gum_adinf"'
        db_table_comment = 'Additional user information table - extended demographics and preferences.'


class GumIdent(models.Model):
    gum_ident_rbid = models.CharField(primary_key=True, max_length=9, db_comment='Ribbon ID.')
    gum_ident_first_name = models.CharField(max_length=32, db_comment='User first name.')
    gum_ident_last_name = models.CharField(max_length=32, db_comment='User last name.')
    gum_ident_middle_name = models.CharField(max_length=32, blank=True, null=True, db_comment='User middle name.')
    gum_ident_birthday = models.DateField(blank=True, null=True, db_comment='User birth date.')
    gum_ident_idnum = models.CharField(max_length=32, blank=True, null=True, db_comment='User national identification number.')
    gum_ident_id_coid = models.ForeignKey(GglCount, models.DO_NOTHING, db_column='gum_ident_id_coid', blank=True, null=True, db_comment='User national ID country of origin.')
    gum_ident_created_date = models.DateField(db_comment='Date record was created.')
    gum_ident_activity_date = models.DateField(blank=True, null=True, db_comment='Date record was last modified.')
    gum_ident_modified_by = models.CharField(max_length=40, blank=True, null=True, db_comment='User who last modified record.')

    class Meta:
        managed = False
        db_table = '"general"."gum_ident"'
        db_table_comment = 'Person identity base record table.'


class SalAvtyp(models.Model):
    sal_avtyp_avid = models.CharField(primary_key=True, max_length=4)
    sal_avtyp_hr_name = models.CharField(max_length=32, blank=True, null=True)
    sal_avtyp_created_date = models.DateField()
    sal_avtyp_activity_date = models.DateField()
    sal_avtyp_modified_by = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = '"student"."sal_avtyp"'


class SarAdvrl(models.Model):
    sar_advrl_arid = models.CharField(primary_key=True, max_length=6)
    sar_advrl_avid = models.ForeignKey(SalAvtyp, models.DO_NOTHING, db_column='sar_advrl_avid')
    sar_advrl_begin_letter = models.CharField(max_length=1)
    sar_advrl_end_letter = models.CharField(max_length=1)
    sar_advrl_advr_rbid = models.CharField(max_length=9)
    sar_advrl_created_date = models.DateField()
    sar_advrl_activity_date = models.DateField()
    sar_advrl_modified_by = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = '"student"."sar_advrl"'
        unique_together = (('sar_advrl_avid', 'sar_advrl_begin_letter', 'sar_advrl_end_letter'),)


class SarOvrar(models.Model):
    sar_ovrar_oaid = models.CharField(primary_key=True, max_length=15)
    sar_ovrar_arid = models.CharField(max_length=6)
    sar_ovrar_stdn_rbid = models.CharField(max_length=9)
    sar_ovrar_advr_rbid = models.CharField(max_length=9)
    scr_ovmrk_reason = models.TextField()
    scr_ovmrk_approved_by = models.CharField(max_length=9)
    sar_ovrar_created_date = models.DateField()
    sar_ovrar_activity_date = models.DateField()
    sar_ovrar_modified_by = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = '"student"."sar_ovrar"'
        unique_together = (('sar_ovrar_arid', 'sar_ovrar_stdn_rbid'),)


class SclCipcd(models.Model):
    scl_cipcd_ciid = models.CharField(primary_key=True, max_length=7, db_comment='CIP code ID in NCES format (2, 4, or 6 digit structure).')
    scl_cipcd_hr_name = models.CharField(max_length=50, db_comment='CIP code human-readable name.')
    scl_cipcd_cal_sp04_code = models.CharField(max_length=5, blank=True, null=True, db_comment='SP04 reporting code for the CIP classification.')
    scl_cipcd_publish_date = models.DateField(blank=True, null=True, db_comment='Date the CIP code was published.')

    class Meta:
        managed = False
        db_table = '"student"."scl_cipcd"'
        db_table_comment = 'CIP code definition table.'


class SclCrtyp(models.Model):
    scl_crtyp_ctid = models.CharField(primary_key=True, max_length=4, db_comment='Curriculum type ID.')
    scl_crtyp_hr_name = models.CharField(max_length=32, blank=True, null=True, db_comment='Curriculum type human-readable name.')
    scl_crtyp_major_ind = models.CharField(max_length=1, blank=True, null=True, db_comment='Indicates if this type can be a major (Y/N).')

    class Meta:
        managed = False
        db_table = '"student"."scl_crtyp"'
        db_table_comment = 'Curriculum type lookup table (e.g., Major, Minor, Certificate).'


class SclCurrv(models.Model):
    scl_currv_cvid = models.CharField(primary_key=True, max_length=14, db_comment='Curriculum version ID (auto-generated from major + term).')
    scl_currv_mrid = models.ForeignKey('SclMajor', models.DO_NOTHING, db_column='scl_currv_mrid', db_comment='Major ID (foreign key to scl_major).')
    scl_currv_ctid = models.ForeignKey(SclCrtyp, models.DO_NOTHING, db_column='scl_currv_ctid')
    scl_currv_effective_term = models.ForeignKey('SglTerms', models.DO_NOTHING, db_column='scl_currv_effective_term', related_name='eff_term')
    scl_currv_end_term = models.ForeignKey('SglTerms', models.DO_NOTHING, db_column='scl_currv_end_term', related_name='end_term')
    scl_currv_min_mark_avg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, db_comment='Minimum GPA required for graduation under this curriculum.')
    scl_currv_min_gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, db_comment='Minimum cumulative GPA required.')
    scl_currv_min_credits = models.IntegerField(db_comment='Minimum total credits required for graduation.')
    scl_currv_created_date = models.DateField()
    scl_currv_activity_date = models.DateField(blank=True, null=True)
    scl_currv_modified_by = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"student"."scl_currv"'
        unique_together = (('scl_currv_mrid', 'scl_currv_effective_term'),)
        db_table_comment = 'Curriculum version table - tracks changes to major/degree requirements over time.'


class SclDegrs(models.Model):
    scl_degrs_dgid = models.CharField(primary_key=True, max_length=6, db_comment='Degree ID.')
    scl_degrs_hr_name = models.CharField(max_length=64, db_comment='Degree human-readable name.')
    scl_degrs_dlid = models.ForeignKey('SclDlevl', models.DO_NOTHING, db_column='scl_degrs_dlid', db_comment='Degree level ID.')
    scl_degrs_finaid_ind = models.CharField(max_length=1, blank=True, null=True, db_comment='Degree financial aid indicator.')

    class Meta:
        managed = False
        db_table = '"student"."scl_degrs"'
        db_table_comment = 'Degree lookup table.'


class SclDlevl(models.Model):
    scl_dlevl_dlid = models.CharField(primary_key=True, max_length=4, db_comment='Degree level ID.')
    scl_dlevl_hr_name = models.CharField(max_length=32, db_comment='Degree level human-readable name.')
    scl_dlevl_nslds_equiv = models.CharField(max_length=2, blank=True, null=True, db_comment='Degree level National Student Loan Data System category code.')
    scl_dlevl_eqf_equiv = models.CharField(max_length=1, blank=True, null=True, db_comment='European Qualifications Framework equivalency.')
    scl_dlevl_lvid = models.ForeignKey('SglLevel', models.DO_NOTHING, db_column='scl_dlevl_lvid', db_comment='Student level ID.')

    class Meta:
        managed = False
        db_table = '"student"."scl_dlevl"'
        db_table_comment = 'Degree level lookup table.'


class SclIscdf(models.Model):
    scl_iscdf_ifid = models.CharField(primary_key=True, max_length=4)
    scl_iscdf_hr_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = '"student"."scl_iscdf"'


class SclMajor(models.Model):
    scl_major_mrid = models.CharField(primary_key=True, max_length=8, db_comment='Major ID.')
    scl_major_hr_name = models.CharField(max_length=64, db_comment='Major title.')
    scl_major_short_name = models.CharField(max_length=32, db_comment='Major short name.')
    scl_major_cgid = models.ForeignKey('SdlColeg', models.DO_NOTHING, db_column='scl_major_cgid', db_comment='Major college ID.')
    scl_major_dgid = models.ForeignKey(SclDegrs, models.DO_NOTHING, db_column='scl_major_dgid', db_comment='Major degree ID.')
    scl_major_ciid = models.ForeignKey(SclCipcd, models.DO_NOTHING, db_column='scl_major_ciid', blank=True, null=True, db_comment='Major CIP Code.')
    scl_major_major_ind = models.CharField(max_length=1, db_comment='Indicates if this program can be declared as a major (Y/N).')
    scl_major_minor_ind = models.CharField(max_length=1, db_comment='Indicates if this program can be declared as a minor (Y/N).')
    scl_major_ifid = models.ForeignKey(SclIscdf, models.DO_NOTHING, db_column='scl_major_ifid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"student"."scl_major"'
        db_table_comment = 'Major report table.'


class ScmStucv(models.Model):
    scm_stucv_scid = models.CharField(primary_key=True, max_length=23)
    scm_stucv_rbid = models.ForeignKey(GumIdent, models.DO_NOTHING, db_column='scm_stucv_rbid')
    scm_stucv_cvid = models.ForeignKey(SclCurrv, models.DO_NOTHING, db_column='scm_stucv_cvid')
    scm_stucv_admit_term = models.CharField(max_length=6)
    scm_stucv_active_ind = models.CharField(max_length=1)
    scm_stucv_cpid = models.ForeignKey('SdlCamps', models.DO_NOTHING, db_column='scm_stucv_cpid')

    class Meta:
        managed = False
        db_table = '"student"."scm_stucv"'
        unique_together = (('scm_stucv_rbid', 'scm_stucv_cvid'),)


class ScrCreqs(models.Model):
    scr_creqs_rqid = models.CharField(primary_key=True, max_length=24, db_comment='Requirement ID (auto-generated).')
    scr_creqs_cvid = models.ForeignKey(SclCurrv, models.DO_NOTHING, db_column='scr_creqs_cvid', db_comment='Curriculum version ID.')
    scr_creqs_crid = models.ForeignKey('SrlCours', models.DO_NOTHING, db_column='scr_creqs_crid', db_comment='Course ID.')
    scr_creqs_rtid = models.ForeignKey('SrlRqtyp', models.DO_NOTHING, db_column='scr_creqs_rtid', db_comment='Requirement type ID (CORE, ELCA, ELCB, etc.).')
    scr_creqs_min_credits = models.IntegerField(blank=True, null=True, db_comment='Minimum credits required (typically matches course credits).')
    scr_creqs_min_mkid = models.ForeignKey('StlMarks', models.DO_NOTHING, db_column='scr_creqs_min_mkid', blank=True, null=True, db_comment='Minimum grade letter required.')
    scr_creqs_min_mark_avg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, db_comment='Minimum numeric grade required.')
    scr_creqs_created_date = models.DateField(db_comment='Date record was created.')
    scr_creqs_activity_date = models.DateField(blank=True, null=True, db_comment='Date record was last modified.')
    scr_creqs_modified_by = models.CharField(max_length=40, blank=True, null=True, db_comment='User who last modified record.')

    class Meta:
        managed = False
        db_table = '"student"."scr_creqs"'
        unique_together = (('scr_creqs_cvid', 'scr_creqs_crid'),)
        db_table_comment = 'Course requirements - individual courses required for curriculum. Links to groups for elective blocks.'


class ScrOvcls(models.Model):
    scr_ovcls_ocid = models.CharField(primary_key=True, max_length=41)
    scr_ovcls_scid = models.ForeignKey(ScmStucv, models.DO_NOTHING, db_column='scr_ovcls_scid')
    scr_ovcls_rqid = models.ForeignKey(ScrCreqs, models.DO_NOTHING, db_column='scr_ovcls_rqid')
    scr_ovcls_crid = models.ForeignKey('SrlCours', models.DO_NOTHING, db_column='scr_ovcls_crid')
    scr_ovcls_reason = models.TextField()
    scr_ovcls_approved_by = models.CharField(max_length=9)
    scr_ovcls_created_date = models.DateField()
    scr_ovcls_activity_date = models.DateField(blank=True, null=True)
    scr_ovcls_modified_by = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"student"."scr_ovcls"'
        unique_together = (('scr_ovcls_scid', 'scr_ovcls_rqid'),)


class ScrOvmrk(models.Model):
    scr_ovmrk_omid = models.CharField(primary_key=True, max_length=41)
    scr_ovmrk_scid = models.ForeignKey(ScmStucv, models.DO_NOTHING, db_column='scr_ovmrk_scid')
    scr_ovmrk_rqid = models.ForeignKey(ScrCreqs, models.DO_NOTHING, db_column='scr_ovmrk_rqid')
    scr_ovmrk_override_mkid = models.ForeignKey('StlMarks', models.DO_NOTHING, db_column='scr_ovmrk_override_mkid')
    scr_ovmrk_override_mark_avg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    scr_ovmrk_reason = models.TextField()
    scr_ovmrk_approved_by = models.CharField(max_length=9)
    scr_ovmrk_created_date = models.DateField()
    scr_ovmrk_activity_date = models.DateField(blank=True, null=True)
    scr_ovmrk_modified_by = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"student"."scr_ovmrk"'
        unique_together = (('scr_ovmrk_scid', 'scr_ovmrk_rqid'),)
        db_table_comment = 'Minimum grade/mark requirement overrides. Allows reducing or waiving the minimum grade requirement for specific curriculum requirements for individual students (e.g., accepting a C when B is normally required).'


class ScrPreqs(models.Model):
    scr_preqs_pqid = models.CharField(primary_key=True, max_length=12, db_comment='Prerequisite ID (auto-generated from course IDs).')
    scr_preqs_crid = models.ForeignKey('SrlCours', models.DO_NOTHING, db_column='scr_preqs_crid', db_comment='Course ID that has the prerequisite requirement.')
    scr_preqs_req_crid = models.ForeignKey('SrlCours', models.DO_NOTHING, db_column='scr_preqs_req_crid', related_name='scrpreqs_scr_preqs_req_crid_set', db_comment='Required prerequisite course ID.')
    scr_preqs_min_grade = models.CharField(max_length=1, blank=True, null=True, db_comment='Minimum grade required in prerequisite course.')

    class Meta:
        managed = False
        db_table = '"student"."scr_preqs"'
        db_table_comment = 'Course prerequisite mapping table.'


class ScrRqgrp(models.Model):
    scr_rqgrp_rgid = models.CharField(primary_key=True, max_length=18, db_comment='Requirement group ID (auto-generated).')
    scr_rqgrp_cvid = models.ForeignKey(SclCurrv, models.DO_NOTHING, db_column='scr_rqgrp_cvid', db_comment='Curriculum version ID.')
    scr_rqgrp_rtid = models.ForeignKey('SrlRqtyp', models.DO_NOTHING, db_column='scr_rqgrp_rtid', db_comment='Requirement type ID (typically ELCA, ELCB, ELCC, etc.).')
    scr_rqgrp_hr_name = models.CharField(max_length=64, db_comment='Group human-readable name (e.g., "Upper Division Technical Electives").')
    scr_rqgrp_min_courses = models.IntegerField(blank=True, null=True, db_comment='Minimum number of courses required from this group.')
    scr_rqgrp_min_credits = models.IntegerField(blank=True, null=True, db_comment='Minimum credit hours required from this group.')
    scr_rqgrp_min_mark_avg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, db_comment='Minimum average mark required for courses in this group.')
    scr_rqgrp_created_date = models.DateField()
    scr_rqgrp_activity_date = models.DateField(blank=True, null=True)
    scr_rqgrp_modified_by = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"student"."scr_rqgrp"'
        unique_together = (('scr_rqgrp_cvid', 'scr_rqgrp_rtid'),)
        db_table_comment = 'Requirement groups/blocks - defines elective blocks and course groups for curriculum. E.g., "6 credits from Block A courses".'


class SdlCamps(models.Model):
    sdl_camps_cpid = models.CharField(primary_key=True, max_length=2, db_comment='Campus ID.')
    sdl_camps_hr_name = models.CharField(max_length=32, db_comment='Campus human-readable name.')

    class Meta:
        managed = False
        db_table = '"student"."sdl_camps"'
        db_table_comment = 'Campus definition table.'


class SdlColeg(models.Model):
    sdl_coleg_cgid = models.CharField(primary_key=True, max_length=4, db_comment='Campus ID.')
    sdl_coleg_hr_name = models.CharField(max_length=64, db_comment='Campus human-readable name.')
    sdl_coleg_short_name = models.CharField(max_length=32, db_comment='College short name.')

    class Meta:
        managed = False
        db_table = '"student"."sdl_coleg"'
        db_table_comment = 'College/school definition table.'


class SdlDepts(models.Model):
    sdl_depts_dpid = models.CharField(primary_key=True, max_length=4, db_comment='Department ID.')
    sdl_depts_cgid = models.ForeignKey(SdlColeg, models.DO_NOTHING, db_column='sdl_depts_cgid', db_comment='College ID.')
    sdl_depts_hr_name = models.CharField(max_length=64, db_comment='Department human-readable name.')

    class Meta:
        managed = False
        db_table = '"student"."sdl_depts"'
        db_table_comment = 'Academic department lookup table.'


class SglLevel(models.Model):
    sgl_level_lvid = models.CharField(primary_key=True, max_length=2, db_comment='Level ID.')
    sgl_level_hr_name = models.CharField(max_length=32, db_comment='Level human-readable name.')
    sgl_level_degree_ind = models.CharField(max_length=1, db_comment='Degree-seeking indicator.')

    class Meta:
        managed = False
        db_table = '"student"."sgl_level"'
        db_table_comment = 'Student level lookup table.'


class SglSmstr(models.Model):
    sgl_smstr_smid = models.CharField(primary_key=True, max_length=4, db_comment='Semester ID.')
    sgl_smstr_hr_name = models.CharField(max_length=6, db_comment='Semester human-readable name.')

    class Meta:
        managed = False
        db_table = '"student"."sgl_smstr"'
        db_table_comment = 'Semester definition table.'


class SglStype(models.Model):
    sgl_stype_stid = models.CharField(primary_key=True, max_length=2, db_comment='Student type ID.')
    sgl_stype_hr_name = models.CharField(max_length=32, db_comment='Student type human-readable name.')
    sgl_stype_next_stid = models.ForeignKey('self', models.DO_NOTHING, db_column='sgl_stype_next_stid', blank=True, null=True, db_comment='Next student type ID for progression mappings.')

    class Meta:
        managed = False
        db_table = '"student"."sgl_stype"'
        db_table_comment = 'Student type lookup table.'


class SglTerms(models.Model):
    sgl_terms_tmid = models.CharField(primary_key=True, max_length=6, db_comment='Term ID. Format: YYYY + semester code (1S = Summer, 2F = Fall, 3W = Winter).')
    sgl_terms_year = models.IntegerField(db_comment='Calendar year of the term.')
    sgl_terms_smid = models.ForeignKey(SglSmstr, models.DO_NOTHING, db_column='sgl_terms_smid', db_comment='Semester ID.')
    sgl_terms_fyid = models.CharField(max_length=4, db_comment='Financial aid year code.')
    sgl_terms_start_date = models.DateField(db_comment='Term official start date.')
    sgl_terms_end_date = models.DateField(db_comment='Term official end date.')
    sgl_terms_hr_name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = '"student"."sgl_terms"'
        unique_together = (('sgl_terms_year', 'sgl_terms_smid'),)
        db_table_comment = 'Academic term definition table.'


class SgmStubi(models.Model):
    sgm_stubi_tsid = models.OneToOneField('SrhSterm', models.DO_NOTHING, db_column='sgm_stubi_tsid', primary_key=True)
    sgm_stubi_rbid = models.ForeignKey(GumIdent, models.DO_NOTHING, db_column='sgm_stubi_rbid')
    sgm_stubi_tmid = models.ForeignKey(SglTerms, models.DO_NOTHING, db_column='sgm_stubi_tmid')
    sgm_stubi_lvid = models.ForeignKey(SglLevel, models.DO_NOTHING, db_column='sgm_stubi_lvid')
    sgm_stubi_stid = models.ForeignKey(SglStype, models.DO_NOTHING, db_column='sgm_stubi_stid')
    sgm_stubi_active_ind = models.CharField(max_length=1)
    sgm_stubi_created_date = models.DateField()
    sgm_stubi_activity_date = models.DateField(blank=True, null=True)
    sgm_stubi_modified_by = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"student"."sgm_stubi"'
        unique_together = (('sgm_stubi_rbid', 'sgm_stubi_tmid'),)


class SrbSects(models.Model):
    srb_sects_stid = models.CharField(primary_key=True, max_length=18, db_comment='Course, Term, Sequence ID')
    srb_sects_tmid = models.ForeignKey(SglTerms, models.DO_NOTHING, db_column='srb_sects_tmid', db_comment='Term ID')
    srb_sects_crid = models.ForeignKey('SrlCours', models.DO_NOTHING, db_column='srb_sects_crid', db_comment='Course ID')
    srb_sects_section_seq = models.IntegerField(db_comment='Section Sequence Number')
    srb_sects_prim_inst = models.ForeignKey(GumIdent, models.DO_NOTHING, related_name='primary', db_column='srb_sects_prim_inst', db_comment='Primary Instructor')
    srb_sects_scnd_inst = models.ForeignKey(GumIdent, models.DO_NOTHING, related_name='secondary', db_column='srb_sects_scnd_inst', blank=True, null=True, db_comment='Secondary Instructor')

    class Meta:
        managed = False
        db_table = '"student"."srb_sects"'
        unique_together = (('srb_sects_tmid', 'srb_sects_crid', 'srb_sects_section_seq'),)
        db_table_comment = 'Section bridge table'


class SrhEnrol(models.Model):
    srh_enrol_erid = models.CharField(primary_key=True, max_length=27, db_comment='Enrollment ID (auto-generated)')
    srh_enrol_rbid = models.ForeignKey(GumIdent, models.DO_NOTHING, db_column='srh_enrol_rbid', db_comment='Ribbon ID')
    srh_enrol_stid = models.ForeignKey(SrbSects, models.DO_NOTHING, db_column='srh_enrol_stid', db_comment='Course section-term-sequence ID')
    srh_enrol_esid = models.ForeignKey('SrlEnrst', models.DO_NOTHING, db_column='srh_enrol_esid', db_comment='Enrollment status ID')
    srh_enrol_created_date = models.DateField(db_comment='Date record was created.')
    srh_enrol_activity_date = models.DateField(db_comment='Date record was last modified.')
    srh_enrol_modified_by = models.CharField(max_length=40, db_comment='User who last modified record.')

    class Meta:
        managed = False
        db_table = '"student"."srh_enrol"'
        unique_together = (('srh_enrol_rbid', 'srh_enrol_stid'),)
        db_table_comment = 'Registration Status History Table'


class SrhSterm(models.Model):
    srh_sterm_tsid = models.CharField(primary_key=True, max_length=15, db_comment='Student/Term ID (auto-generated)')
    srh_sterm_rbid = models.ForeignKey(GumIdent, models.DO_NOTHING, db_column='srh_sterm_rbid', db_comment='Ribbon ID')
    srh_sterm_tmid = models.ForeignKey(SglTerms, models.DO_NOTHING, db_column='srh_sterm_tmid', db_comment='Term ID')
    srh_sterm_rgid = models.ForeignKey('SrlRgtyp', models.DO_NOTHING, db_column='srh_sterm_rgid', db_comment='Registration Type ID')
    srh_sterm_created_date = models.DateField()
    srh_sterm_activity_date = models.DateField(blank=True, null=True, db_comment='Record last modification date.')
    srh_sterm_modified_by = models.CharField(max_length=40, blank=True, null=True, db_comment='User who last modified the record.')

    class Meta:
        managed = False
        db_table = '"student"."srh_sterm"'
        unique_together = (('srh_sterm_rbid', 'srh_sterm_tmid'),)
        db_table_comment = 'Student base information table.'


class SrlCours(models.Model):
    srl_cours_crid = models.CharField(primary_key=True, max_length=10, db_comment='Course ID')
    srl_cours_sbid = models.ForeignKey('SrlSubjs', models.DO_NOTHING, db_column='srl_cours_sbid', db_comment='Subject ID')
    srl_cours_crse_num = models.CharField(max_length=6, db_comment='Course Number')
    srl_cours_hr_name = models.CharField(max_length=64, db_comment='Course Title')
    srl_cours_active_ind = models.CharField(max_length=1)
    srl_cours_credit_hours = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"student"."srl_cours"'
        unique_together = (('srl_cours_sbid', 'srl_cours_crse_num'),)
        db_table_comment = 'Course lookup table'


class SrlEnrst(models.Model):
    srl_enrst_esid = models.CharField(primary_key=True, max_length=2, db_comment='Enrollment Status ID')
    srl_enrst_hr_name = models.CharField(max_length=32, db_comment='Enrollment Status Human Readable Name')
    srl_enrst_roll_ind = models.CharField(max_length=1, db_comment='Indicates if student is enrolled in the course (Y/N).')
    srl_enrst_credit_ind = models.CharField(max_length=1, db_comment='Indicates if student receives credit for the course (Y/N).')

    class Meta:
        managed = False
        db_table = '"student"."srl_enrst"'
        db_table_comment = 'Enrollment Status Lookup Table with Predefined Values. \n     Combines roll and credit flags to indicate enrollment semantics:\n     - Y,Y = Normal registration (Registered, Web Registered, Admin Registered, Vendor Registered)\n     - N,N = Withdrawal (Withdraw, Web Withdraw, Admin Withdraw, Vendor Withdraw)\n     - N,Y = Special cases (Credited Withdraw, Transfer Course, Honorary Course)\n     - Y,N = Audit'


class SrlRgtyp(models.Model):
    srl_rgtyp_rgid = models.CharField(primary_key=True, max_length=4)
    srl_rgtyp_hr_name = models.CharField(max_length=32, blank=True, null=True)
    srl_rgtyp_enrol_ind = models.CharField(max_length=1, blank=True, null=True)
    srl_rgtyp_count_ind = models.CharField(max_length=1, blank=True, null=True)
    srl_rgtyp_audit_ind = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"student"."srl_rgtyp"'


class SrlRqtyp(models.Model):
    srl_rqtyp_rtid = models.CharField(primary_key=True, max_length=4, db_comment='Requirement type ID.')
    srl_rqtyp_hr_name = models.CharField(max_length=32, db_comment='Requirement type human-readable name.')
    srl_rqtyp_group_ind = models.CharField(max_length=1, blank=True, null=True, db_comment='Indicates if this type represents a group/block of courses (Y/N).')

    class Meta:
        managed = False
        db_table = '"student"."srl_rqtyp"'
        db_table_comment = 'Requirement type lookup table (e.g., CORE, ELCA, ELCB for elective blocks).'


class SrlSubjs(models.Model):
    srl_subjs_sbid = models.CharField(primary_key=True, max_length=4, db_comment='Subject ID')
    srl_subjs_hr_name = models.CharField(max_length=64, blank=True, null=True, db_comment='Subject Human Readable Name')
    srl_subjs_dpid = models.ForeignKey(SdlDepts, models.DO_NOTHING, db_column='srl_subjs_dpid', blank=True, null=True, db_comment='Department ID - References DCR_DEPTS.DCR_DEPTS_DPID')

    class Meta:
        managed = False
        db_table = '"student"."srl_subjs"'
        db_table_comment = 'Course Subject Report Table'


class SthCrtrn(models.Model):
    sth_crtrn_erid = models.OneToOneField(SrhEnrol, models.DO_NOTHING, db_column='sth_crtrn_erid', primary_key=True, db_comment='Enrollment ID (foreign key to srh_enrol).')
    sth_crtrn_rbid = models.ForeignKey(GumIdent, models.DO_NOTHING, db_column='sth_crtrn_rbid', blank=False, null=False, db_comment='Person Ribbon ID (foriegn key to gum_ident)')
    sth_crtrn_stid = models.ForeignKey(SrlSubjs, models.DO_NOTHING, db_column='sth_crtrn_stid', blank=False, null=False, db_comment='Secton ID (foriegn key to srl_subjs)')
    sth_crtrn_final_mark_avg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, db_comment='Final numeric grade/percentage achieved.')
    sth_crtrn_final_mkid = models.ForeignKey('StlMarks', models.DO_NOTHING, db_column='sth_crtrn_final_mkid', blank=True, null=True, db_comment='Final letter grade (foreign key to stl_marks).')
    sth_crtrn_created_date = models.DateField(db_comment='Date grade was recorded.')
    sth_crtrn_activity_date = models.DateField(db_comment='Date grade was last modified.')
    sth_crtrn_modified_by = models.CharField(max_length=40, db_comment='User who last modified the grade.')

    class Meta:
        managed = False
        db_table = '"student"."sth_crtrn"'
        db_table_comment = 'Course transcript history - stores final grades for completed courses.'


class StlMarks(models.Model):
    stl_marks_mkid = models.CharField(primary_key=True, max_length=1, db_comment='Mark/Grade letter (A, B, C, D, F, etc.).')
    stl_marks_credit_hr_gp = models.IntegerField(blank=True, null=True, db_comment='Grade points per credit hour for GPA calculation (4.0 scale).')

    class Meta:
        managed = False
        db_table = '"student"."stl_marks"'
        db_table_comment = 'Grade marks/letters lookup table with quality points for GPA calculation.'

class HsvStdnt(models.Model):
    hsv_stdnt_tsid = models.CharField(primary_key=True, max_length=15, db_comment='Ribbon ID.')
    hsv_stdnt_rbid = models.CharField(max_length=9, db_comment='Ribbon ID.')
    hsv_stdnt_pref_first_name = models.CharField(max_length=32, blank=True, null=True, db_comment='Preferred first name.')
    hsv_stdnt_first_name = models.CharField(max_length=32, db_comment='Legal first name.')
    hsv_stdnt_middle_name = models.CharField(max_length=32, blank=True, null=True, db_comment='Middle name.')
    hsv_stdnt_last_name = models.CharField(max_length=32, db_comment='Last name.')
    hsv_stdnt_birthday = models.DateField(blank=True, null=True, db_comment='Date of birth.')
    hsv_stdnt_lvid = models.CharField(max_length=2, db_comment='Student level ID.')
    hsv_stdnt_level = models.CharField(max_length=32, db_comment='Student level human-readable name.')
    hsv_stdnt_stid = models.CharField(max_length=2, db_comment='Student type ID.')
    hsv_stdnt_student_type = models.CharField(max_length=32, db_comment='Student type human-readable name.')
    hsv_stdnt_active_ind = models.CharField(max_length=1, db_comment='Active enrollment indicator.')

    class Meta:
        managed = False
        db_table = '"helmsman"."hsv_stdnt"'
        db_table_comment = 'Helmsman student view - current term student record with level, type, major, and campus.'

class HgvPrson(models.Model):
    hgv_prson_rbid = models.CharField(primary_key=True, max_length=9, db_comment='Ribbon ID.')
    hgv_prson_pref_first_name = models.CharField(max_length=32, blank=True, null=True, db_comment='Preferred first name.')
    hgv_prson_first_name = models.CharField(max_length=32, db_comment='Legal first name.')
    hgv_prson_middle_name = models.CharField(max_length=32, blank=True, null=True, db_comment='Middle name.')
    hgv_prson_last_name = models.CharField(max_length=32, db_comment='Last name.')
    hgv_prson_birthday = models.DateField(blank=True, null=True, db_comment='Date of birth.')
    hgv_prson_idnum = models.CharField(max_length=32, blank=True, null=True, db_comment='National identification number.')
    hgv_prson_id_country = models.CharField(max_length=64, db_comment='Country of national ID human-readable name.')

    class Meta:
        managed = False
        db_table = '"helmsman"."hgv_prson"'
        db_table_comment = 'Helmsman person view - base identity record with preferred name and national ID country.'

class HsvActcr(models.Model):
    hsv_actcr_crid = models.CharField(primary_key=True, max_length=10, db_comment='Course ID.')
    hsv_actcr_sbid = models.CharField(max_length=4, db_comment='Subject ID.')
    hsv_actcr_crse_num = models.CharField(max_length=6, db_comment='Course number.')
    hsv_actcr_subject = models.CharField(max_length=64, blank=True, null=True, db_comment='Subject human-readable name.')
    hsv_actcr_department = models.CharField(max_length=64, db_comment='Department human-readable name.')
    hsv_actcr_name = models.CharField(max_length=64, db_comment='Course title.')
    hsv_actcr_active_ind = models.CharField(max_length=1, db_comment='active indicator - always N in this view.')

    class Meta:
        managed = False
        db_table = '"helmsman"."hsv_actcr"'
        db_table_comment = 'Helmsman active courses view - active courses only with subject and department.'

class HsvAllcr(models.Model):
    hsv_allcr_crid = models.CharField(primary_key=True, max_length=10, db_comment='Course ID.')
    hsv_allcr_sbid = models.CharField(max_length=4, db_comment='Subject ID.')
    hsv_allcr_crse_num = models.CharField(max_length=6, db_comment='Course number.')
    hsv_allcr_subject = models.CharField(max_length=64, blank=True, null=True, db_comment='Subject human-readable name.')
    hsv_allcr_department = models.CharField(max_length=64, db_comment='Department human-readable name.')
    hsv_allcr_name = models.CharField(max_length=64, db_comment='Course title.')
    hsv_allcr_active_ind = models.CharField(max_length=1, db_comment='active indicator.')

    class Meta:
        managed = False
        db_table = '"helmsman"."hsv_allcr"'
        db_table_comment = 'Helmsman all courses view - all courses regardless of active status with subject and department.'

class HsvCrcrc(models.Model):
    hsv_crcrc_cvid = models.CharField(primary_key=True, max_length=14, db_comment='Curriculum version ID.')
    hsv_crcrc_mrid = models.CharField(max_length=8, db_comment='Major ID.')
    hsv_crcrc_effective_term = models.CharField(max_length=6, db_comment='Term when this curriculum version became effective.')
    hsv_crcrc_hr_name = models.CharField(max_length=64, db_comment='Major human-readable name.')
    hsv_crcrc_ctid = models.CharField(max_length=4, db_comment='Curriculum type ID.')
    hsv_crcrc_curr_type = models.CharField(max_length=32, blank=True, null=True, db_comment='Curriculum type human-readable name.')
    hsv_crcrc_mark_avg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, db_comment='Minimum grade average required for graduation.')
    hsv_crcrc_min_gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, db_comment='Minimum cumulative GPA required.')
    hsv_crcrc_min_credits = models.IntegerField(db_comment='Minimum total credits required for graduation.')
    hsv_crcrc_created_date = models.DateField(db_comment='Date record was created.')
    hsv_crcrc_activity_date = models.DateField(blank=True, null=True, db_comment='Date record was last modified.')
    hsv_crcrc_modified_by = models.CharField(max_length=40, blank=True, null=True, db_comment='User who last modified record.')

    class Meta:
        managed = False
        db_table = '"helmsman"."hsv_crcrc"'
        db_table_comment = 'Helmsman current curriculum versions view - active curriculum versions only (no end term) with major and type details.'

class HsvLtsts(models.Model):
    hsv_ltsts_rbid = models.CharField(primary_key=True, max_length=9, db_comment='Ribbon ID')
    hsv_ltsts_latest_tsid = models.ForeignKey(SgmStubi, models.DO_NOTHING, db_column='hsv_ltsts_latest_tsid', blank=True, null=True, db_comment='Student Term ID - References SGM_STUBI.SGM_STUBI_TSID')
    class Meta:
        managed = False
        db_table = '"helmsman"."hsv_ltsts"'
        db_table_comment = 'Helmsman latest student term code table.'

class HsvSects(models.Model):
    hsv_sects_stid = models.CharField(primary_key=True, max_length=10, db_comment='Section record ID.')
    hsv_sects_tmid = models.CharField(max_length=6, db_comment='Term ID.')
    hsv_sects_crid = models.CharField(max_length=10, db_comment='Course ID.')
    hsv_sects_seq = models.IntegerField(db_comment='Section sequence number.')
    hsv_sects_name = models.CharField(max_length=64, db_comment='Course human-readable name.')
    hsv_sects_prim_inst = models.CharField(max_length=82, blank=True, null=True, db_comment='Primary instructor full name.')
    hsv_sects_scnd_inst = models.CharField(max_length=82, blank=True, null=True, db_comment='Secondary instructor full name.')

    class Meta:
        managed = False
        db_table = '"helmsman"."hsv_sects"'
        db_table_comment = 'Helmsman sections view - course sections with term, course, and instructor details.'

class HsvAudit(models.Model):
    hsv_audit_pkid = models.CharField(max_length=100, primary_key=True, help_text="Surrogate PK: concatenation of scm_stucv_scid || srl_cours_crid",)
    hsv_audit_scid = models.CharField(max_length=50, help_text="Student curriculum record ID (scm_stucv.scm_stucv_scid)",)
    hsv_audit_rbid = models.CharField(max_length=20, help_text="Enrollment record batch ID (scm_stucv.scm_stucv_rbid)",)
    hsv_audit_group_ind = models.CharField(max_length=1, null=True, blank=True, help_text="Requirement type group indicator (srl_rqtyp.srl_rqtyp_group_ind)",)
    hsv_audit_rtid = models.CharField(max_length=20, help_text="Requirement type ID (scr_creqs.scr_creqs_rtid)",)
    hsv_audit_sbid = models.CharField(max_length=10, help_text="Subject/department ID (srl_cours.srl_cours_sbid)",)
    hsv_audit_crse_numb = models.CharField(max_length=10, help_text="Course number (srl_cours.srl_cours_crse_num)",)
    hsv_audit_crse_name = models.CharField(max_length=64, db_comment='Course human-readable name.')
    hsv_audit_stid = models.CharField(max_length=50, null=True, blank=True, help_text="Section ID from the most recent qualifying transcript record (srb_sects.srb_sects_stid)",)
    hsv_audit_final_mark = models.DecimalField( max_digits=5, decimal_places=2, null=True, blank=True, help_text="Final mark average from the most recent qualifying transcript record",)
    hsv_audit_final_mkid = models.CharField( max_length=50, null=True, blank=True, help_text="Final mark grade ID from the most recent qualifying transcript record",)
    hsv_audit_progress_stid = models.CharField(max_length=50, null=True, blank=True, help_text="Section ID wtihout sequence from the current term",)


    class Meta:
        managed = False
        db_table = '"helmsman"."hsv_audit"'
        verbose_name = "Audit View Record"
        verbose_name_plural = "Audit View Records"