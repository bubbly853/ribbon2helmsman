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
        app_label = 'sis'
        db_table = 'finance.fgl_fyear'
        db_table_comment = 'Financial aid year definition table.'


class GglCount(models.Model):
    ggl_count_coid = models.CharField(primary_key=True, max_length=2, db_comment='Country ID, Alpha-2 code.')
    ggl_count_hr_name = models.CharField(max_length=64, db_comment='Country human-readable name.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'general.ggl_count'
        db_table_comment = 'Country definition table.'


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
        app_label = 'sis'
        db_table = 'general.gum_ident'
        db_table_comment = 'Person identity base record table.'


class SclCipcd(models.Model):
    scl_cipcd_ciid = models.CharField(primary_key=True, max_length=7, db_comment='CIP code ID in NCES format (2, 4, or 6 digit structure).')
    scl_cipcd_hr_name = models.CharField(max_length=50, db_comment='CIP code human-readable name.')
    scl_cipcd_cal_sp04_code = models.CharField(max_length=5, blank=True, null=True, db_comment='SP04 reporting code for the CIP classification.')
    scl_cipcd_publish_date = models.DateField(blank=True, null=True, db_comment='Date the CIP code was published.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'student.scl_cipcd'
        db_table_comment = 'CIP code definition table.'


class SclDegrs(models.Model):
    scl_degrs_dgid = models.CharField(primary_key=True, max_length=6, db_comment='Degree ID.')
    scl_degrs_hr_name = models.CharField(max_length=32, db_comment='Degree human-readable name.')
    scl_degrs_dlid = models.ForeignKey('SclDlevl', models.DO_NOTHING, db_column='scl_degrs_dlid', db_comment='Degree level ID.')
    scl_degrs_finaid_ind = models.CharField(max_length=1, blank=True, null=True, db_comment='Degree financial aid indicator.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'student.scl_degrs'
        db_table_comment = 'Degree lookup table.'


class SclDlevl(models.Model):
    scl_dlevl_dlid = models.CharField(primary_key=True, max_length=4, db_comment='Degree level ID.')
    scl_dlevl_hr_name = models.CharField(max_length=32, db_comment='Degree level human-readable name.')
    scl_dlevl_nslds_equiv = models.CharField(max_length=1, blank=True, null=True, db_comment='Degree level National Student Loan Data System category code.')
    scl_dlevl_eqf_equiv = models.CharField(max_length=1, blank=True, null=True, db_comment='European Qualifications Framework equivalency.')
    scl_dlevl_lvid = models.ForeignKey('SglLevel', models.DO_NOTHING, db_column='scl_dlevl_lvid', db_comment='Student level ID.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'student.scl_dlevl'
        db_table_comment = 'Degree level lookup table.'


class SclMajor(models.Model):
    scl_major_mrid = models.CharField(primary_key=True, max_length=8, db_comment='Major ID.')
    scl_major_hr_name = models.CharField(max_length=32, db_comment='Major title.')
    scl_major_short_name = models.CharField(max_length=12, db_comment='Major short name.')
    scl_major_cgid = models.ForeignKey('SdlColeg', models.DO_NOTHING, db_column='scl_major_cgid', db_comment='Major college ID.')
    scl_major_dgid = models.ForeignKey(SclDegrs, models.DO_NOTHING, db_column='scl_major_dgid', db_comment='Major degree ID.')
    scl_major_ciid = models.ForeignKey(SclCipcd, models.DO_NOTHING, db_column='scl_major_ciid', blank=True, null=True, db_comment='Major CIP Code.')
    scl_major_major_ind = models.CharField(max_length=1, db_comment='Valid major indicator.')
    scl_major_minor_ind = models.CharField(max_length=1, db_comment='Valid minor indicator.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'student.scl_major'
        db_table_comment = 'Major report table.'


class SdlColeg(models.Model):
    sdl_coleg_cgid = models.CharField(primary_key=True, max_length=4, db_comment='College ID.')
    sdl_coleg_hr_name = models.CharField(max_length=32, db_comment='College human-readable name.')
    sdl_coleg_short_name = models.CharField(max_length=12, db_comment='College short name.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'student.sdl_coleg'
        db_table_comment = 'College/school definition table.'


class SdlDepts(models.Model):
    sdl_depts_dpid = models.CharField(primary_key=True, max_length=4, db_comment='Department ID.')
    sdl_depts_cgid = models.ForeignKey(SdlColeg, models.DO_NOTHING, db_column='sdl_depts_cgid', db_comment='College ID. References SDL_COLEG.SDL_COLEG_CGID.')
    sdl_depts_hr_name = models.CharField(max_length=32, db_comment='Department human-readable name.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'student.sdl_depts'
        db_table_comment = 'Academic department lookup table.'


class SglLevel(models.Model):
    sgl_level_lvid = models.CharField(primary_key=True, max_length=2, db_comment='Level ID.')
    sgl_level_hr_name = models.CharField(max_length=32, db_comment='Level human-readable name.')
    sgl_level_degree_ind = models.CharField(max_length=1, db_comment='Degree-seeking indicator.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'student.sgl_level'
        db_table_comment = 'Student level lookup table.'


class SglSmstr(models.Model):
    sgl_smstr_smid = models.CharField(primary_key=True, max_length=4, db_comment='Semester ID.')
    sgl_smstr_hr_name = models.CharField(max_length=6, db_comment='Semester human-readable name.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'student.sgl_smstr'
        db_table_comment = 'Semester definition table.'


class SglStype(models.Model):
    sgl_stype_stid = models.CharField(primary_key=True, max_length=2, db_comment='Student type ID.')
    sgl_stype_hr_name = models.CharField(max_length=32, db_comment='Student type human-readable name.')
    sgl_stype_next_stid = models.ForeignKey('self', models.DO_NOTHING, db_column='sgl_stype_next_stid', blank=True, null=True, db_comment='Next student type ID for progression mappings.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'student.sgl_stype'
        db_table_comment = 'Student type lookup table.'


class SglTerms(models.Model):
    sgl_terms_tmid = models.CharField(primary_key=True, max_length=6, db_comment='Term ID. Format: YYYY + semester code (1S = Summer, 2F = Fall, 3W = Winter).')
    sgl_terms_year = models.IntegerField(db_comment='Calendar year of the term.')
    sgl_terms_smid = models.ForeignKey(SglSmstr, models.DO_NOTHING, db_column='sgl_terms_smid', db_comment='Semester ID. References SGL_SMSTR.SGL_SMSTR_SMID.')
    sgl_terms_fyid = models.CharField(max_length=4, db_comment='Financial aid year code.')
    sgl_terms_start_date = models.DateField(db_comment='Term official start date.')
    sgl_terms_end_date = models.DateField(db_comment='Term official end date.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'sgl_terms'
        db_table_comment = 'Academic term definition table.'


class SgmStubi(models.Model):
    sgm_stubi_rbid = models.ForeignKey(
        GumIdent,
        on_delete=models.CASCADE,
        db_column='sgm_stubi_rbid',
        primary_key=True,
        related_name='stubi_records'
    )
    sgm_stubi_update_tmid = models.ForeignKey(SglTerms, models.DO_NOTHING, db_column='sgm_stubi_update_tmid', db_comment='Term ID of most recent update.')
    sgm_stubi_lvid = models.ForeignKey(SglLevel, models.DO_NOTHING, db_column='sgm_stubi_lvid', db_comment='Student level ID.')
    sgm_stubi_stid = models.ForeignKey(SglStype, models.DO_NOTHING, db_column='sgm_stubi_stid', db_comment='Student type ID.')
    sgm_stubi_active_ind = models.CharField(max_length=1)
    sgm_stubi_major1_mrid = models.ForeignKey(SclMajor, models.DO_NOTHING, db_column='sgm_stubi_major1_mrid', blank=True, null=True, db_comment='First major ID.')
    sgm_stubi_minor1_mrid = models.ForeignKey(SclMajor, models.DO_NOTHING, db_column='sgm_stubi_minor1_mrid', related_name='sgmstubi_sgm_stubi_minor1_mrid_set', blank=True, null=True, db_comment='First minor ID.')
    sgm_stubi_major2_mrid = models.ForeignKey(SclMajor, models.DO_NOTHING, db_column='sgm_stubi_major2_mrid', related_name='sgmstubi_sgm_stubi_major2_mrid_set', blank=True, null=True, db_comment='Second major ID.')
    sgm_stubi_minor2_mrid = models.ForeignKey(SclMajor, models.DO_NOTHING, db_column='sgm_stubi_minor2_mrid', related_name='sgmstubi_sgm_stubi_minor2_mrid_set', blank=True, null=True, db_comment='Second minor ID.')
    sgm_stubi_created_date = models.DateField(db_comment='Record creation date.')
    sgm_stubi_activity_date = models.DateField(blank=True, null=True, db_comment='Record last modification date.')
    sgm_stubi_modified_by = models.CharField(max_length=40, blank=True, null=True, db_comment='User who last modified the record.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'sgm_stubi'
        db_table_comment = 'Student base information table.'


class SrbSects(models.Model):
    srb_sects_scid = models.IntegerField(primary_key=True)  # The composite primary key (srb_sects_scid, srb_sects_tmid) found, that is not supported. The first column is selected.
    srb_sects_tmid = models.ForeignKey(SglTerms, models.DO_NOTHING, db_column='srb_sects_tmid', db_comment='Term ID')
    srb_sects_crid = models.ForeignKey('SrlCours', models.DO_NOTHING, db_column='srb_sects_crid', blank=True, null=True, db_comment='Course ID')
    srb_sects_section_seq = models.IntegerField(blank=True, null=True, db_comment='Section Sequence Number')
    srb_sects_prim_inst = models.CharField(max_length=9, blank=True, null=True, db_comment='Primary Instructor')
    srb_sects_scnd_inst = models.CharField(max_length=9, blank=True, null=True, db_comment='Secondary Instructor')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'srb_sects'
        unique_together = (('srb_sects_scid', 'srb_sects_tmid'), ('srb_sects_tmid', 'srb_sects_crid', 'srb_sects_section_seq'),)
        db_table_comment = 'Section bridge table'


class SrhEnrol(models.Model):
    srh_enrol_rbid = models.CharField(primary_key=True, max_length=9, db_comment='Ribbon ID')  # The composite primary key (srh_enrol_rbid, srh_enrol_scid, srh_enrol_tmid) found, that is not supported. The first column is selected.
    srh_enrol_scid = models.ForeignKey(SrbSects, models.DO_NOTHING, db_column='srh_enrol_scid', db_comment='Course section ID')
    srh_enrol_tmid = models.ForeignKey(SglTerms, models.DO_NOTHING, db_column='srh_enrol_tmid', db_comment='Term ID')
    srh_enrol_esid = models.ForeignKey('SrlEnrst', models.DO_NOTHING, db_column='srh_enrol_esid', db_comment='Enrollment status ID')
    srh_enrol_created_date = models.DateField(db_comment='Date record was created.')
    srh_enrol_activity_date = models.DateField(db_comment='Date record was last modified.')
    srh_enrol_modified_by = models.CharField(max_length=40, db_comment='User who last modified record.')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'srh_enrol'
        unique_together = (('srh_enrol_rbid', 'srh_enrol_scid', 'srh_enrol_tmid'),)
        db_table_comment = 'Registration Status History Table'


class SrlCours(models.Model):
    srl_cours_crid = models.CharField(primary_key=True, max_length=6, db_comment='Course ID')
    srl_cours_sbid = models.ForeignKey('SrlSubjs', models.DO_NOTHING, db_column='srl_cours_sbid', db_comment='Subject ID')
    srl_cours_crse_num = models.CharField(max_length=6, db_comment='Course Number')
    srl_cours_hr_name = models.CharField(max_length=64, db_comment='Course Title')
    srl_cours_inactive_ind = models.CharField(max_length=1)

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'srl_cours'
        unique_together = (('srl_cours_sbid', 'srl_cours_crse_num'),)
        db_table_comment = 'Course lookup table'


class SrlEnrst(models.Model):
    srl_enrst_esid = models.CharField(primary_key=True, max_length=2, db_comment='Enrollment Status ID')
    srl_enrst_hr_name = models.CharField(max_length=32, db_comment='Enrollment Status Human Readable Name')
    srl_enrst_roll_ind = models.CharField(max_length=1, db_comment='Indicates if student is enrolled in the course (Y/N).')
    srl_enrst_credit_ind = models.CharField(max_length=1, db_comment='Indicates if student receives credit for the course (Y/N).')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'srl_enrst'
        db_table_comment = 'Enrollment Status Lookup Table with Predefined Values. \n     Combines roll and credit flags to indicate enrollment semantics:\n     - Y,Y = Normal registration (Registered, Web Registered, Admin Registered, Vendor Registered)\n     - N,N = Withdrawal (Withdraw, Web Withdraw, Admin Withdraw, Vendor Withdraw)\n     - N,Y = Special cases (Credited Withdraw, Transfer Course, Honorary Course)\n     - Y,N = Audit'


class SrlSubjs(models.Model):
    srl_subjs_sbid = models.CharField(primary_key=True, max_length=4, db_comment='Subject ID')
    srl_subjs_hr_name = models.CharField(max_length=64, blank=True, null=True, db_comment='Subject Human Readable Name')
    srl_subjs_dpid = models.ForeignKey(SdlDepts, models.DO_NOTHING, db_column='srl_subjs_dpid', blank=True, null=True, db_comment='Department ID - References DCR_DEPTS.DCR_DEPTS_DPID')

    class Meta:
        managed = False
        app_label = 'sis'
        db_table = 'srl_subjs'
        db_table_comment = 'Course Subject Report Table'
