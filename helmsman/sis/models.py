# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class GglCount(models.Model):
    ggl_count_coid = models.CharField(primary_key=True, max_length=2, db_comment='Country ID, Alpha-2 code.')
    ggl_count_hr_name = models.CharField(max_length=64, db_comment='Country human-readable name.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'ggl_count'
        db_table_comment = 'Country definition table.'

class GumIdent(models.Model):
    gum_ident_rbid = models.CharField(primary_key=True, max_length=9, db_comment='Ribbon ID.')
    gum_ident_first_name = models.CharField(max_length=32, db_comment='User first name.')
    gum_ident_last_name = models.CharField(max_length=32, db_comment='User last name.')
    gum_ident_middle_name = models.CharField(max_length=32, null=True, blank=True, db_comment='User middle name.')
    gum_ident_birthday = models.DateField(null=True, blank=True, db_comment='User birth date.')
    gum_ident_idnum = models.CharField(max_length=32, null=True, blank=True, db_comment='User national identification number.')
    gum_ident_id_coid = models.ForeignKey(GglCount, on_delete=models.PROTECT, db_column='gum_ident_id_coid', null=True, blank=True, related_name='identities', db_comment='User national ID country of origin.')
    gum_ident_created_date = models.DateField(db_comment='Date record was created.')
    gum_ident_activity_date = models.DateField(null=True, blank=True, db_comment='Date record was last modified.')
    gum_ident_modified_by = models.CharField(max_length=40, null=True, blank=True, db_comment='User who last modified record.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'gum_ident'
        db_table_comment = 'Person identity base record table.'

class SdlColeg(models.Model):
    sdl_coleg_cgid = models.CharField(primary_key=True, max_length=4, db_comment='College ID.')
    sdl_coleg_hr_name = models.CharField(max_length=32, db_comment='College human-readable name.')
    sdl_coleg_short_name = models.CharField(max_length=12, db_comment='College short name.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'sdl_coleg'
        db_table_comment = 'College/school definition table.'

class SdlCamps(models.Model):
    sdl_camps_cpid = models.CharField(primary_key=True, max_length=2, db_comment='Campus ID.')
    sdl_camps_hr_name = models.CharField(max_length=32, db_comment='Campus human-readable name.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'sdl_camps'
        db_table_comment = 'Campus definition table.'

class SdlDepts(models.Model):
    sdl_depts_dpid = models.CharField(primary_key=True, max_length=4, db_comment='Department ID.')
    sdl_depts_cgid = models.ForeignKey(SdlColeg, on_delete=models.PROTECT, db_column='sdl_depts_cgid', related_name='departments', db_comment='College ID.')
    sdl_depts_hr_name = models.CharField(max_length=32, db_comment='Department human-readable name.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'sdl_depts'
        db_table_comment = 'Academic department lookup table.'

class SglLevel(models.Model):
    sgl_level_lvid = models.CharField(primary_key=True, max_length=2, db_comment='Level ID.')
    sgl_level_hr_name = models.CharField(max_length=32, db_comment='Level human-readable name.')
    sgl_level_degree_ind = models.CharField(max_length=1, db_comment='Degree-seeking indicator.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'sgl_level'
        db_table_comment = 'Student level lookup table.'

class SclDlevl(models.Model):
    scl_dlevl_dlid = models.CharField(primary_key=True, max_length=4, db_comment='Degree level ID.')
    scl_dlevl_hr_name = models.CharField(max_length=32, db_comment='Degree level human-readable name.')
    scl_dlevl_nslds_equiv = models.CharField(max_length=1, null=True, blank=True, db_comment='Degree level National Student Loan Data System category code.')
    scl_dlevl_eqf_equiv = models.CharField(max_length=1, null=True, blank=True, db_comment='European Qualifications Framework equivalency.')
    scl_dlevl_lvid = models.ForeignKey(SglLevel, on_delete=models.PROTECT, db_column='scl_dlevl_lvid', related_name='degree_levels', db_comment='Student level ID.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'scl_dlevl'
        db_table_comment = 'Degree level lookup table.'

class SclDegrs(models.Model):
    scl_degrs_dgid = models.CharField(primary_key=True, max_length=6, db_comment='Degree ID.')
    scl_degrs_hr_name = models.CharField(max_length=32, db_comment='Degree human-readable name.')
    scl_degrs_dlid = models.ForeignKey(SclDlevl, on_delete=models.PROTECT, db_column='scl_degrs_dlid', related_name='degrees', db_comment='Degree level ID.')
    scl_degrs_finaid_ind = models.CharField(max_length=1, null=True, blank=True, db_comment='Degree financial aid indicator.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'scl_degrs'
        db_table_comment = 'Degree lookup table.'

class SclCipcd(models.Model):
    scl_cipcd_ciid = models.CharField(primary_key=True, max_length=7, db_comment='CIP code ID in NCES format (2, 4, or 6 digit structure).')
    scl_cipcd_hr_name = models.CharField(max_length=50, db_comment='CIP code human-readable name.')
    scl_cipcd_cal_sp04_code = models.CharField(max_length=5, null=True, blank=True, db_comment='SP04 reporting code for the CIP classification.')
    scl_cipcd_publish_date = models.DateField(null=True, blank=True, db_comment='Date the CIP code was published.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'scl_cipcd'
        db_table_comment = 'CIP code definition table.'

class SclMajor(models.Model):
    scl_major_mrid = models.CharField(primary_key=True, max_length=8, db_comment='Major ID.')
    scl_major_hr_name = models.CharField(max_length=32, db_comment='Major title.')
    scl_major_short_name = models.CharField(max_length=12, db_comment='Major short name.')
    scl_major_cgid = models.ForeignKey(SdlColeg, on_delete=models.PROTECT, db_column='scl_major_cgid', related_name='majors', db_comment='Major college ID.')
    scl_major_dgid = models.ForeignKey(SclDegrs, on_delete=models.PROTECT, db_column='scl_major_dgid', related_name='majors', db_comment='Major degree ID.')
    scl_major_ciid = models.ForeignKey(SclCipcd, on_delete=models.PROTECT, db_column='scl_major_ciid', null=True, blank=True, related_name='majors', db_comment='Major CIP Code.')
    scl_major_major_ind = models.CharField(max_length=1, db_comment='Valid major indicator.')
    scl_major_minor_ind = models.CharField(max_length=1, db_comment='Valid minor indicator.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'scl_major'
        db_table_comment = 'Major report table.'

class ScbMjrcm(models.Model):
    scb_mjrcm_mcid = models.CharField(primary_key=True, max_length=10, db_comment='Major Campus ID.')
    scb_mjrcm_mrid = models.ForeignKey(SclMajor, on_delete=models.PROTECT, db_column='scb_mjrcm_mrid', related_name='campus_links')
    scb_mjrcm_cpid = models.ForeignKey(SdlCamps, on_delete=models.PROTECT, db_column='scb_mjrcm_cpid', related_name='campus_links')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'scb_mjrcm'
        db_table_comment = 'Major Campus Section Bridge Table.'
        unique_together = (('scb_mjrcm_mrid', 'scb_mjrcm_cpid'),)

class SglStype(models.Model):
    sgl_stype_stid = models.CharField(primary_key=True, max_length=2, db_comment='Student type ID.')
    sgl_stype_hr_name = models.CharField(max_length=32, db_comment='Student type human-readable name.')
    sgl_stype_next_stid = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, db_column='sgl_stype_next_stid', related_name='previous_types', db_comment='Next student type ID for progression mappings.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'sgl_stype'
        db_table_comment = 'Student type lookup table.'

class SglSmstr(models.Model):
    sgl_smstr_smid = models.CharField(primary_key=True, max_length=4, db_comment='Semester ID.')
    sgl_smstr_hr_name = models.CharField(max_length=6, db_comment='Semester human-readable name.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'sgl_smstr'
        db_table_comment = 'Semester definition table.'

class SglTerms(models.Model):
    sgl_terms_tmid = models.CharField(primary_key=True, max_length=6, db_comment='Term ID. Format: YYYY + semester code (1S = Summer, 2F = Fall, 3W = Winter).')
    sgl_terms_year = models.IntegerField(db_comment='Calendar year of the term.')
    sgl_terms_smid = models.ForeignKey(SglSmstr, on_delete=models.PROTECT, db_column='sgl_terms_smid', related_name='terms', db_comment='Semester ID.')
    sgl_terms_fyid = models.ForeignKey('FglFyear', on_delete=models.PROTECT, db_column='sgl_terms_fyid', related_name='terms', db_comment='Financial aid year code.')
    sgl_terms_start_date = models.DateField(db_comment='Term official start date.')
    sgl_terms_end_date = models.DateField(db_comment='Term official end date.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'sgl_terms'
        db_table_comment = 'Academic term definition table.'

class SgmStubi(models.Model):
    sgm_stubi_rbid = models.ForeignKey(GumIdent, on_delete=models.CASCADE, primary_key=True, db_column='sgm_stubi_rbid', related_name='stubi_records')
    sgm_stubi_update_tmid = models.ForeignKey(SglTerms, on_delete=models.PROTECT, db_column='sgm_stubi_update_tmid', related_name='stubi_updates', db_comment='Term of last update')
    sgm_stubi_lvid = models.ForeignKey(SglLevel, on_delete=models.PROTECT, db_column='sgm_stubi_lvid', related_name='stubi_levels', db_comment='Student level ID')
    sgm_stubi_stid = models.ForeignKey(SglStype, on_delete=models.PROTECT, db_column='sgm_stubi_stid', related_name='stubi_types', db_comment='Student type ID')
    sgm_stubi_active_ind = models.CharField(max_length=1, db_comment='Active indicator (Y/N)')

    # Majors and campus mapping
    sgm_stubi_major1_mcid = models.ForeignKey(ScbMjrcm, on_delete=models.PROTECT, db_column='sgm_stubi_major1_mcid', null=True, blank=True, related_name='stubi_major1', db_comment='Primary major, campus mapping')
    sgm_stubi_major2_mcid = models.ForeignKey(ScbMjrcm, on_delete=models.PROTECT, db_column='sgm_stubi_major2_mcid', null=True, blank=True, related_name='stubi_major2', db_comment='Secondary major, campus mapping')
    sgm_stubi_major3_mcid = models.ForeignKey(ScbMjrcm, on_delete=models.PROTECT, db_column='sgm_stubi_major3_mcid', null=True, blank=True, related_name='stubi_major3', db_comment='Tertiary major, campus mapping')

    # Minors and campus mapping
    sgm_stubi_minor1_mcid = models.ForeignKey(ScbMjrcm, on_delete=models.PROTECT, db_column='sgm_stubi_minor1_mcid', null=True, blank=True, related_name='stubi_minor1', db_comment='Primary minor, campus mapping')
    sgm_stubi_minor2_mcid = models.ForeignKey(ScbMjrcm, on_delete=models.PROTECT, db_column='sgm_stubi_minor2_mcid', null=True, blank=True, related_name='stubi_minor2', db_comment='Secondary minor, campus mapping')
    sgm_stubi_minor3_mcid = models.ForeignKey(ScbMjrcm, on_delete=models.PROTECT, db_column='sgm_stubi_minor3_mcid', null=True, blank=True, related_name='stubi_minor3', db_comment='Tertiary minor, campus mapping')

    # Audit info
    sgm_stubi_created_date = models.DateField(db_comment='Record creation date')
    sgm_stubi_activity_date = models.DateField(null=True, blank=True, db_comment='Last modification date')
    sgm_stubi_modified_by = models.CharField(max_length=40, null=True, blank=True, db_comment='User who last modified record')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'sgm_stubi'

class SrlSubjs(models.Model):
    srl_subjs_sbid = models.CharField(primary_key=True, max_length=4, db_comment='Subject ID')
    srl_subjs_hr_name = models.CharField(max_length=64, db_comment='Subject Human Readable Name')
    srl_subjs_dpid = models.ForeignKey(SdlDepts, on_delete=models.PROTECT, db_column='srl_subjs_dpid', related_name='subjects', db_comment='Department ID')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'srl_subjs'
        db_table_comment = 'Course Subject Report Table'

class SrlCours(models.Model):
    srl_cours_crid = models.CharField(primary_key=True, max_length=6, db_comment='Course ID')
    srl_cours_sbid = models.ForeignKey(SrlSubjs, on_delete=models.PROTECT, db_column='srl_cours_sbid', related_name='courses', db_comment='Subject ID')
    srl_cours_crse_num = models.CharField(max_length=6, db_comment='Course Number')
    srl_cours_hr_name = models.CharField(max_length=64, db_comment='Course Title')
    srl_cours_inactive_ind = models.CharField(max_length=1, db_comment='Inactive indicator')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'srl_cours'
        db_table_comment = 'Course lookup table'
        unique_together = (('srl_cours_sbid', 'srl_cours_crse_num'),)

class SrbSects(models.Model):
    srb_sects_stid = models.CharField(primary_key=True, max_length=12, db_comment='Section-term-sequece ID')
    srb_sects_scid = models.IntegerField(db_comment='Section ID')
    srb_sects_tmid = models.ForeignKey(SglTerms, on_delete=models.PROTECT, db_column='srb_sects_tmid', related_name='sections')
    srb_sects_crid = models.ForeignKey(SrlCours, on_delete=models.PROTECT, db_column='srb_sects_crid', related_name='sections')
    srb_sects_section_seq = models.IntegerField(db_column='srb_sects_section_seq', db_comment='Section Sequence Number')
    srb_sects_prim_inst = models.ForeignKey(GumIdent, on_delete=models.PROTECT, db_column='srb_sects_prim_inst', related_name='primary_sections')
    srb_sects_scnd_inst = models.ForeignKey(GumIdent, on_delete=models.PROTECT, db_column='srb_sects_scnd_inst', null=True, blank=True, related_name='secondary_sections')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'srb_sects'
        db_table_comment = 'Section bridge table'
        unique_together = (('srb_sects_tmid', 'srb_sects_crid', 'srb_sects_section_seq'),)


class SrlEnrst(models.Model):
    srl_enrst_esid = models.CharField(primary_key=True, max_length=2, db_comment='Enrollment Status ID')
    srl_enrst_hr_name = models.CharField(max_length=32, db_comment='Enrollment Status Human Readable Name')
    srl_enrst_roll_ind = models.CharField(max_length=1, db_comment='Indicates if student is enrolled in the course (Y/N).')
    srl_enrst_credit_ind = models.CharField(max_length=1, db_comment='Indicates if student receives credit for the course (Y/N).')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'srl_enrst'
        db_table_comment = 'Enrollment Status Lookup Table'

class SrhEnrol(models.Model):
    srh_enrol_rbid = models.ForeignKey(GumIdent, on_delete=models.PROTECT, db_column='srh_enrol_rbid', related_name='enrollments')
    srh_enrol_stid = models.ForeignKey(SrbSects, on_delete=models.PROTECT, db_column='srh_enrol_stid', related_name='enrollments')
    srh_enrol_esid = models.ForeignKey(SrlEnrst, on_delete=models.PROTECT, db_column='srh_enrol_esid', related_name='enrollments')
    srh_enrol_final_mark = models.FloatField(db_comment='Student Final Mark.')
    srh_enrol_created_date = models.DateField(db_comment='Date record was created.')
    srh_enrol_activity_date = models.DateField(db_comment='Date record was last modified.')
    srh_enrol_modified_by = models.CharField(max_length=40, db_comment='User who last modified record.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'srh_enrol'
        db_table_comment = 'Registration Status History Table'
        unique_together = (('srh_enrol_rbid', 'srh_enrol_stid'),)

class FglFyear(models.Model):
    fgl_fyear_fyid = models.CharField(primary_key=True, max_length=4, db_comment='Financial aid year code.')
    fgl_fyear_desc = models.CharField(max_length=40, db_comment='Financial aid year description.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'fgl_fyear'
        db_table_comment = 'Financial aid year definition table.'
