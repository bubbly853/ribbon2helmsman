-- ============================================
-- Helmsman Schema for Ribbon2 SIS
-- Release 1.0 - Initial Schema
-- Date: 2026-04-20
-- PostgreSQL 16+
-- Apply: psql -U ribbon2 -d ribbon2 -f 6-helmsman.sql
-- ============================================
BEGIN;

-- ============================================
-- Create database schema - login as ribbon2 on ribbon2
-- ============================================
CREATE SCHEMA helmsman AUTHORIZATION "ribbon2";
ALTER SCHEMA helmsman OWNER TO "ribbon2";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA helmsman TO "ribbon2";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA helmsman TO
"ribbon2";

-- ============================================
-- DDL for view hsv_stdnt
-- ============================================

CREATE VIEW helmsman.hsv_stdnt AS
    SELECT
        s1.sgm_stubi_rbid         hsv_stdnt_rbid,
        s1.sgm_stubi_tsid         hsv_stdnt_tsid,
        gum_adinf_pref_first_name hsv_stdnt_pref_first_name,
        gum_ident_first_name      hsv_stdnt_first_name,
        gum_ident_middle_name     hsv_stdnt_middle_name,
        gum_ident_last_name       hsv_stdnt_last_name,
        gum_ident_birthday        hsv_stdnt_birthday,
        s1.sgm_stubi_lvid         hsv_stdnt_lvid,
        sgl_level_hr_name         hsv_stdnt_level,
        s1.sgm_stubi_stid         hsv_stdnt_stid,
        sgl_stype_hr_name         hsv_stdnt_student_type,
        sgm_stubi_active_ind      hsv_stdnt_active_ind
    FROM
             general.gum_ident
        JOIN student.sgm_stubi s1 ON s1.sgm_stubi_rbid = gum_ident_rbid
        JOIN student.sgl_level ON sgl_level_lvid = s1.sgm_stubi_lvid
        JOIN student.sgl_stype ON sgl_stype_stid = s1.sgm_stubi_stid
        JOIN general.gum_adinf ON gum_adinf_rbid = gum_ident_rbid
    WHERE
        sgm_stubi_tmid = (
            SELECT
                MAX(s2.sgm_stubi_tmid)
            FROM
                student.sgm_stubi s2
            WHERE
                s2.sgm_stubi_rbid = s1.sgm_stubi_rbid
        )
    ORDER BY
        1;

-- ============================================
-- DDL for view hgv_prson
-- ============================================

CREATE VIEW helmsman.hgv_prson AS
    SELECT
        gum_ident_rbid            hgv_prson_rbid,
        gum_adinf_pref_first_name hgv_prson_pref_first_name,
        gum_ident_first_name      hgv_prson_first_name,
        gum_ident_middle_name     hgv_prson_middle_name,
        gum_ident_last_name       hgv_prson_last_name,
        gum_ident_birthday        hgv_prson_birthday,
        gum_ident_idnum           hgv_prson_idnum,
        ggl_count_hr_name         hgv_prson_id_country
    FROM
             general.gum_ident
        JOIN general.gum_adinf ON gum_ident_rbid = gum_adinf_rbid
        JOIN general.ggl_count ON ggl_count_coid = gum_ident_id_coid
    ORDER BY
        1;
        
-- ============================================
-- DDL for view hsv_ltsts
-- ============================================

CREATE VIEW helmsman.hsv_ltsts AS
    SELECT
        sgm_stubi_rbid                        hsv_ltsts_rbid,
        sgm_stubi_rbid || MAX(sgm_stubi_tmid) AS hsv_ltsts_latest_tsid
    FROM
        student.sgm_stubi
    GROUP BY
        sgm_stubi_rbid;
        
-- ============================================
-- DDL for view hsv_actcr
-- ============================================

CREATE VIEW helmsman.hsv_actcr AS
    SELECT
        srl_cours_crid       hsv_actcr_crid,
        srl_cours_sbid       hsv_actcr_sbid,
        srl_cours_crse_num   hsv_actcr_crse_num,
        srl_subjs_hr_name    hsv_actcr_subject,
        sdl_depts_hr_name    hsv_actcr_department,
        srl_cours_hr_name    hsv_actcr_name,
        srl_cours_active_ind hsv_actcr_active_ind
    FROM
             student.srl_cours
        JOIN student.srl_subjs ON srl_subjs_sbid = srl_cours_sbid
        JOIN student.sdl_depts ON sdl_depts_dpid = srl_subjs_dpid
    WHERE
        srl_cours_active_ind = 'Y';
        
-- ============================================
-- DDL for view hsv_allcr
-- ============================================

CREATE VIEW helmsman.hsv_allcr AS
    SELECT
        srl_cours_crid       hsv_allcr_crid,
        srl_cours_sbid       hsv_allcr_sbid,
        srl_cours_crse_num   hsv_allcr_crse_num,
        srl_subjs_hr_name    hsv_allcr_subject,
        sdl_depts_hr_name    hsv_allcr_department,
        srl_cours_hr_name    hsv_allcr_name,
        srl_cours_active_ind hsv_allcr_active_ind
    FROM
             student.srl_cours
        JOIN student.srl_subjs ON srl_subjs_sbid = srl_cours_sbid
        JOIN student.sdl_depts ON sdl_depts_dpid = srl_subjs_dpid;
        
-- ============================================
-- DDL for view hsv_crcrc
-- ============================================

CREATE VIEW helmsman.hsv_crcrc AS
    SELECT
        scl_currv_cvid           hsv_crcrc_cvid,
        scl_currv_mrid           hsv_crcrc_mrid,
        scl_currv_effective_term hsv_crcrc_effective_term,
        scl_major_hr_name        hsv_crcrc_hr_name,
        scl_currv_ctid           hsv_crcrc_ctid,
        scl_crtyp_hr_name        hsv_crcrc_curr_type,
        scl_currv_min_mark_avg   hsv_crcrc_mark_avg,
        scl_currv_min_gpa        hsv_crcrc_min_gpa,
        scl_currv_min_credits    hsv_crcrc_min_credits,
        scl_currv_created_date   hsv_crcrc_created_date,
        scl_currv_activity_date  hsv_crcrc_activity_date,
        scl_currv_modified_by    hsv_crcrc_modified_by
    FROM
             student.scl_currv
        JOIN student.scl_major ON scl_major_mrid = scl_currv_mrid
        JOIN student.scl_crtyp ON scl_crtyp_ctid = scl_currv_ctid
    WHERE
        scl_currv_end_term IS NULL;
        
-- ============================================
-- DDL for view hsv_sects
-- ============================================
CREATE VIEW helmsman.hsv_sects AS
    SELECT
        srb_sects_stid              hsv_sects_stid,
        srb_sects_tmid              hsv_sects_tmid,
        srb_sects_crid              hsv_sects_crid,
        srb_sects_section_seq       hsv_sects_seq,
        srl_cours_hr_name           hsv_sects_name,
        prim.gum_ident_first_name
        || ' '
           || prim.gum_ident_last_name hsv_sects_prim_inst,
        scnd.gum_ident_first_name
        || ' '
           || scnd.gum_ident_last_name hsv_sects_scnd_inst
    FROM
             student.srb_sects
        JOIN student.srl_cours ON srl_cours_crid = srb_sects_crid
        JOIN general.gum_ident prim ON prim.gum_ident_rbid = srb_sects_prim_inst
        LEFT JOIN general.gum_ident scnd ON scnd.gum_ident_rbid = srb_sects_scnd_inst;
        
-- ============================================
-- DDL for view hsv_currv
-- ============================================

CREATE VIEW helmsman.hsv_currv AS
    SELECT
        scl_currv_cvid           hsv_currv_cvid,
        scl_major_mrid           hsv_currv_mrid,
        scl_major_hr_name        hsv_currv_major,
        scl_currv_effective_term hsv_currv_tmid,
        sgl_terms_hr_name        hsv_currv_term,
        scl_crtyp_hr_name        hsv_currv_type
    FROM
             student.scl_currv
        JOIN student.scl_major ON scl_major_mrid = scl_currv_mrid
        JOIN student.scl_crtyp ON scl_crtyp_ctid = scl_currv_ctid
        JOIN student.sgl_terms ON sgl_terms_tmid = scl_currv_effective_term;
        

-- ============================================
-- DDL for view hsv_audit
-- ============================================

CREATE VIEW helmsman.hsv_audit AS
    WITH wrh_trans AS (
        SELECT
            e.srh_enrol_rbid           AS wrh_trans_rbid,
            c.srl_cours_crid           AS wrh_trans_crid,
            c.srl_cours_sbid           AS wrh_trans_sbid,
            s.srb_sects_stid           AS wrh_trans_stid,
            c.srl_cours_crse_num       AS wrh_trans_crse_num,
            c.srl_cours_hr_name        AS wrh_trans_crse_name,
            s.srb_sects_tmid           AS wrh_trans_tmid,
            t.sth_crtrn_final_mark_avg AS wrh_trans_final_mark,
            t.sth_crtrn_final_mkid     AS wrh_trans_final_mkid
        FROM
                 student.sth_crtrn t
            JOIN student.srh_enrol e ON e.srh_enrol_erid = t.sth_crtrn_erid
            JOIN student.srb_sects s ON s.srb_sects_stid = e.srh_enrol_stid
            JOIN student.srl_cours c ON c.srl_cours_crid = s.srb_sects_crid
        ORDER BY
            e.srh_enrol_rbid,
            s.srb_sects_tmid,
            c.srl_cours_sbid,
            c.srl_cours_crse_num
    ), wrh_prgrs AS (
        SELECT DISTINCT
            srh_enrol_rbid wrh_prgrs_rbid,
            srb_sects_crid wrh_prgrs_crid,
            sgl_terms_tmid wrh_prgrs_tmid
        FROM
                 student.srh_enrol
            JOIN student.srb_sects ON srb_sects_stid = srh_enrol_stid
            JOIN student.sgl_terms ON sgl_terms_tmid = srb_sects_tmid
                                      AND now() BETWEEN sgl_terms_start_date AND sgl_terms_end_date
    )
    SELECT
        scm_stucv_scid || srl_cours_crid AS hsv_audit_pkid,
        scm_stucv_scid                   AS hsv_audit_scid,
        scm_stucv_rbid                   AS hsv_audit_rbid,
        srl_rqtyp_group_ind              AS hsv_audit_group_ind,
        scr_creqs_rtid                   AS hsv_audit_rtid,
        srl_cours_sbid                   AS hsv_audit_sbid,
        srl_cours_crse_num               AS hsv_audit_crse_numb,
        srl_cours_hr_name                AS hsv_audit_crse_name,
        tr1.wrh_trans_stid               AS hsv_audit_stid,
        tr1.wrh_trans_final_mark         AS hsv_audit_final_mark,
        tr1.wrh_trans_final_mkid         AS hsv_audit_final_mkid,
        wrh_prgrs_crid || wrh_prgrs_tmid AS hsv_audit_progress_stid
    FROM
             student.scr_creqs cr1
        JOIN student.srl_cours ON srl_cours_crid = scr_creqs_crid
        JOIN student.scm_stucv ON scm_stucv_cvid = scr_creqs_cvid
        JOIN student.srl_rqtyp ON srl_rqtyp_rtid = scr_creqs_rtid
        LEFT JOIN wrh_trans tr1 ON wrh_trans_crid = srl_cours_crid
                                   AND tr1.wrh_trans_tmid = (
            SELECT
                MAX(tr2.wrh_trans_tmid)
            FROM
                wrh_trans tr2
            WHERE
                    tr2.wrh_trans_crid = tr1.wrh_trans_crid
                AND cr1.scr_creqs_min_mark_avg <= tr2.wrh_trans_final_mark
        )
        LEFT JOIN wrh_prgrs ON wrh_prgrs_crid = srl_cours_crid
                               AND wrh_prgrs_rbid = scm_stucv_rbid;

COMMIT;

