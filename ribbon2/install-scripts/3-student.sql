-- ============================================
-- Ribbon2 General Schema for Ribbon2 SIS Student
-- Release 1.0 - Initial Schema
-- Date: 2026-04-20
-- PostgreSQL 16+
-- Apply: psql -U ribbon2 -d ribbon2 -f 3-student.sql
-- ============================================

BEGIN;

-- ============================================
-- Create Schema Student
-- ============================================

CREATE SCHEMA student;

-- ============================================
-- Create Trigger Functions
-- ============================================

CREATE FUNCTION student.fn_sal_avtyp_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.sal_avtyp_created_date := CURRENT_DATE;
    NEW.sal_avtyp_activity_date := CURRENT_DATE;
    NEW.sal_avtyp_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_sal_avtyp_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.sal_avtyp_activity_date := CURRENT_DATE;
    NEW.sal_avtyp_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_sar_advrl_arid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.sar_advrl_arid := NEW.sar_advrl_avid || NEW.sar_advrl_begin_letter || NEW.sar_advrl_end_letter;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_sar_advrl_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.sar_advrl_created_date := CURRENT_DATE;
    NEW.sar_advrl_activity_date := CURRENT_DATE;
    NEW.sar_advrl_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_sar_advrl_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.sar_advrl_activity_date := CURRENT_DATE;
    NEW.sar_advrl_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_sar_ovrar_oaid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.sar_ovrar_oaid := NEW.sar_ovrar_arid || NEW.sar_ovrar_stdn_rbid;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_sar_ovrar_validate_lastname() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_first_letter CHAR(1);
    v_last_name VARCHAR(32);
    v_count INTEGER;
BEGIN
    SELECT
        UPPER(SUBSTRING(gum_ident_last_name, 1, 1)),
        gum_ident_last_name
    INTO
        v_first_letter,
        v_last_name
    FROM
        gum_ident
    WHERE
        gum_ident_rbid = new.sar_ovrar_stdn_rbid;

    IF v_last_name IS NULL THEN
        RAISE EXCEPTION 'No identity record found for RBID %', NEW.sar_ovrar_stdn_rbid;
    END IF;

    SELECT COUNT(*)
    INTO
        v_count
    FROM
        sar_advrl
    WHERE
        v_first_letter BETWEEN sar_advrl_begin_letter AND sar_advrl_end_letter
        AND new.sar_ovrar_arid = sar_advrl_arid;
    IF v_count = 0 THEN
        RAISE EXCEPTION 'Last name "%" does not fall within any valid range. First letter "%" is not between any begin/end values for rule "%".', 
        v_last_name, v_first_letter, NEW.sar_ovrar_arid;
    END IF;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scb_mjrcm_mcid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scb_mjrcm_mcid := new.scb_mjrcm_mrid || scb_mjrcm_cpid;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scb_strqs_sqid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scb_strqs_sqid := NEW.scb_strqs_scid || NEW.scb_strqs_rqid;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scb_strqs_validate_curriculum() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_student_cvid VARCHAR(14);
    v_requirement_cvid VARCHAR(14);
BEGIN
    -- Get the curriculum version from the student-curriculum record
    SELECT scm_stucv_cvid INTO v_student_cvid
    FROM student.scm_stucv
    WHERE scm_stucv_scid = NEW.scb_strqs_scid;

    -- Get the curriculum version from the requirement
    SELECT scr_creqs_cvid INTO v_requirement_cvid
    FROM student.scr_creqs
    WHERE scr_creqs_rqid = NEW.scb_strqs_rqid;

    -- Ensure they match
    IF v_student_cvid != v_requirement_cvid THEN
        RAISE EXCEPTION 'Requirement % belongs to curriculum %, but student is enrolled in curriculum %',
            NEW.scb_strqs_rqid, v_requirement_cvid, v_student_cvid;
    END IF;

    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scl_currv_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scl_currv_created_date := CURRENT_DATE;
    NEW.scl_currv_activity_date := CURRENT_DATE;
    NEW.scl_currv_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scl_currv_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scl_currv_activity_date := CURRENT_DATE;
    NEW.scl_currv_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scl_currv_cvid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
  NEW.scl_currv_cvid := NEW.scl_currv_mrid || NEW.scl_currv_effective_term;
  RETURN NEW;
  END;
  $$;

CREATE FUNCTION student.fn_scl_currv_set_end_terms() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE student.scl_currv t
    SET scl_currv_end_term = NEW.scl_currv_effective_term
    WHERE t.scl_currv_mrid = NEW.scl_currv_mrid
      AND t.scl_currv_effective_term = (
          SELECT MAX(t2.scl_currv_effective_term)
          FROM student.scl_currv t2
          WHERE t2.scl_currv_mrid = NEW.scl_currv_mrid
            AND t2.scl_currv_effective_term < NEW.scl_currv_effective_term
      );

    SELECT t.scl_currv_effective_term
    INTO NEW.scl_currv_end_term
    FROM student.scl_currv t
    WHERE t.scl_currv_mrid = NEW.scl_currv_mrid
      AND t.scl_currv_effective_term > NEW.scl_currv_effective_term
    ORDER BY t.scl_currv_effective_term
    ASC
    LIMIT 1;

    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scm_stucv_scid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scm_stucv_scid := NEW.scm_stucv_rbid || NEW.scm_stucv_cvid;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_creqs_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scr_creqs_created_date := CURRENT_DATE;
    NEW.scr_creqs_activity_date := CURRENT_DATE;
    NEW.scr_creqs_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_creqs_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scr_creqs_activity_date := CURRENT_DATE;
    NEW.scr_creqs_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_creqs_rqid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
  NEW.scr_creqs_rqid := NEW.scr_creqs_cvid || NEW.scr_creqs_crid;
  RETURN NEW;
    END;
  $$;

CREATE FUNCTION student.fn_scr_ovcls_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scr_ovcls_created_date := CURRENT_DATE;
    NEW.scr_ovcls_activity_date := CURRENT_DATE;
    NEW.scr_ovcls_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_ovcls_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scr_ovcls_activity_date := CURRENT_DATE;
    NEW.scr_ovcls_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_ovcls_ocid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scr_ovcls_ocid := NEW.scr_ovcls_scid || NEW.scr_ovcls_rqid;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_ovcls_validate_curriculum() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_student_cvid VARCHAR(14);
    v_requirement_cvid VARCHAR(14);
BEGIN
    BEGIN
        SELECT scm_stucv_cvid INTO v_student_cvid
        FROM student.scm_stucv
        WHERE scm_stucv_scid = NEW.scr_ovcls_scid;
    EXCEPTION WHEN OTHERS THEN
      v_student_cvid := NULL;
    END;

    BEGIN
        SELECT scr_creqs_cvid INTO v_requirement_cvid
        FROM student.scr_creqs
        WHERE scr_creqs_rqid = NEW.scr_ovcls_rqid;
    EXCEPTION WHEN OTHERS THEN
      v_student_cvid := NULL;
    END;

    IF v_student_cvid IS NULL OR v_requirement_cvid IS NULL THEN
        RAISE EXCEPTION 'Student or curriculum requirement not found';
    END IF;

        IF v_student_cvid != v_requirement_cvid THEN
        RAISE EXCEPTION 'Requirement % belongs to curriculum %, but student is enrolled in curriculum %',
            NEW.scr_ovcls_rqid, v_requirement_cvid, v_student_cvid;
    END IF;

    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_ovmrk_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scr_ovmrk_created_date := CURRENT_DATE;
    NEW.scr_ovmrk_activity_date := CURRENT_DATE;
    NEW.scr_ovmrk_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_ovmrk_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scr_ovmrk_activity_date := CURRENT_DATE;
    NEW.scr_ovmrk_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_ovmrk_omid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scr_ovmrk_omid := NEW.scr_ovmrk_scid || NEW.scr_ovmrk_rqid;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_ovmrk_validate_curriculum() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_student_cvid VARCHAR(14);
    v_requirement_cvid VARCHAR(14);
BEGIN
    BEGIN
        SELECT scm_stucv_cvid INTO v_student_cvid
        FROM student.scm_stucv
        WHERE scm_stucv_scid = NEW.scr_ovmrk_scid;
    EXCEPTION WHEN OTHERS THEN
      v_student_cvid := NULL;
    END;

    BEGIN
        SELECT scr_creqs_cvid INTO v_requirement_cvid
        FROM student.scr_creqs
        WHERE scr_creqs_rqid = NEW.scr_ovmrk_rqid;
    EXCEPTION WHEN OTHERS THEN
      v_student_cvid := NULL;
    END;

    IF v_student_cvid IS NULL OR v_requirement_cvid IS NULL THEN
        RAISE EXCEPTION 'Student or curriculum requirement not found';
    END IF;

        IF v_student_cvid != v_requirement_cvid THEN
        RAISE EXCEPTION 'Requirement % belongs to curriculum %, but student is enrolled in curriculum %',
            NEW.scr_ovmrk_rqid, v_requirement_cvid, v_student_cvid;
    END IF;

    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_preqs_pqid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        NEW.scr_preqs_pqid := NEW.scr_preqs_crid || NEW.scr_preqs_req_crid ;
        RETURN NEW;
    END;
    $$;

CREATE FUNCTION student.fn_scr_rqgrp_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
BEGIN
    NEW.scr_rqgrp_created_date := CURRENT_DATE;
    NEW.scr_rqgrp_activity_date := CURRENT_DATE;
    NEW.scr_rqgrp_modified_by := CURRENT_USER;

    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_rqgrp_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.scr_rqgrp_activity_date := CURRENT_DATE;
    NEW.scr_rqgrp_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_scr_rqgrp_rgid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
BEGIN
    NEW.scr_rqgrp_rgid := new.scr_rqgrp_cvid || NEW.scr_rqgrp_rtid;

    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_sgl_terms_tmid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF abs(NEW.sgl_terms_year) NOT BETWEEN 1000 AND 9999 THEN
        RAISE EXCEPTION 'Year must be 4 digits. Got: %', NEW.sgl_terms_year;
    END IF;
    NEW.sgl_terms_tmid := NEW.sgl_terms_year::varchar || CASE 
                                                             WHEN NEW.sgl_terms_smid = 'SMMR' THEN
                                                                 '1S'
                                                             WHEN NEW.sgl_terms_smid = 'ATMN' THEN
                                                                 '2F'
                                                             WHEN NEW.sgl_terms_smid = 'SPNG' THEN
                                                                 '3W'
                                                         END;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_sgm_stubi_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.sgm_stubi_created_date := CURRENT_DATE;
    NEW.sgm_stubi_activity_date := CURRENT_DATE;
    NEW.sgm_stubi_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_sgm_stubi_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.sgm_stubi_activity_date := CURRENT_DATE;
    NEW.sgm_stubi_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_sgm_stubi_tsid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        NEW.sgm_stubi_tsid := NEW.sgm_stubi_rbid || NEW.sgm_stubi_tmid ;
        RETURN NEW;
    END;
    $$;

CREATE FUNCTION student.fn_sgm_stubi_verify_tmid() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_tmid CHAR(6);
	v_rbid varchar(9);
BEGIN
    SELECT srh_sterm_tmid, srh_sterm_rbid
    INTO v_tmid, v_rbid
    FROM student.srh_sterm
    WHERE srh_sterm_tsid = NEW.sgm_stubi_tsid;
    NEW.sgm_stubi_tmid := v_tmid;
	NEW.sgm_stubi_rbid := v_rbid;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_srb_sects_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  DECLARE
    next_seq        INTEGER;
    term_suffix text;
  BEGIN

    PERFORM pg_advisory_xact_lock(
        hashtext(NEW.srb_sects_tmid || '|' || NEW.srb_sects_crid)
      );
    SELECT coalesce( max(srb_sects_section_seq), 0 ) + 1
    INTO   next_seq
    FROM   student.srb_sects
    WHERE  srb_sects_tmid = NEW.srb_sects_tmid
    AND    srb_sects_crid = NEW.srb_sects_crid;

    NEW.srb_sects_section_seq := next_seq;

    NEW.srb_sects_stid := NEW.srb_sects_crid || NEW.srb_sects_tmid || next_seq;
    RETURN NEW;
  END;
  $$;

CREATE FUNCTION student.fn_srb_sects_stid_autogen_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        NEW.srb_sects_stid := NEW.srb_sects_crid || NEW.srb_sects_tmid || NEW.srb_sects_section_seq;
        RETURN NEW;
    END;
  $$;

CREATE FUNCTION student.fn_srh_enrol_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.srh_enrol_created_date := CURRENT_DATE;
    NEW.srh_enrol_activity_date := CURRENT_DATE;
    NEW.srh_enrol_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_srh_enrol_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.srh_enrol_activity_date := CURRENT_DATE;
    NEW.srh_enrol_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_srh_enrol_erid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.srh_enrol_erid := NEW.srh_enrol_rbid || NEW.srh_enrol_stid;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_srh_sterm_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.srh_sterm_created_date := CURRENT_DATE;
    NEW.srh_sterm_activity_date := CURRENT_DATE;
    NEW.srh_sterm_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_srh_sterm_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.srh_sterm_activity_date := CURRENT_DATE;
    NEW.srh_sterm_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_srh_sterm_create_sgm_stubi() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NOT EXISTS ( SELECT 1 FROM student.sgm_stubi WHERE sgm_stubi_rbid = NEW.srh_sterm_rbid ) THEN
    INSERT INTO student.sgm_stubi (
        sgm_stubi_tsid,
		sgm_stubi_rbid,
        sgm_stubi_tmid,
        sgm_stubi_lvid,
        sgm_stubi_stid,
        sgm_stubi_active_ind
    ) VALUES (
        NEW.srh_sterm_tsid,
		NEW.srh_sterm_rbid,
        NEW.srh_sterm_tmid,
        'UN',
        'UN',
        'Y'
    );
    END IF;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_srh_sterm_tsid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.srh_sterm_tsid := NEW.srh_sterm_rbid || NEW.srh_sterm_tmid;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_srl_cours_crid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        NEW.srl_cours_crid := NEW.srl_cours_sbid || NEW.srl_cours_crse_num ;
        RETURN NEW;
    END;
    $$;

CREATE FUNCTION student.fn_sth_crtrn_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.sth_crtrn_created_date := CURRENT_DATE;
    NEW.sth_crtrn_activity_date := CURRENT_DATE;
    NEW.sth_crtrn_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_sth_crtrn_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.sth_crtrn_activity_date := CURRENT_DATE;
    NEW.sth_crtrn_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION student.fn_sth_crtrn_erid_autogen() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.sth_crtrn_erid := NEW.sth_crtrn_rbid || NEW.sth_crtrn_stid;
    RETURN NEW;
END;
$$;

CREATE PROCEDURE student.pr_sgm_stubi_update_styp(IN p_new_tmid character varying, IN p_rbid character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_last_tmid CHAR(6);
    v_prev_stid VARCHAR(2);
    v_next_stid VARCHAR(2);
    v_next_lvid VARCHAR(2);
    v_next_active_ind CHAR(1);
BEGIN
    IF EXISTS (SELECT 1
               FROM student.sgm_stubi
               WHERE sgm_stubi_tmid = p_new_tmid
                     AND sgm_stubi_rbid = p_rbid) THEN
        RAISE EXCEPTION 'Base record already exits for term % and student %', p_new_tmid, p_rbid;
    END IF;

    IF NOT EXISTS (SELECT 1
               FROM student.srh_sterm
               WHERE srh_sterm_tmid = p_new_tmid
                     AND srh_sterm_rbid = p_rbid) THEN
        RAISE EXCEPTION 'Term record does not exits for term % and student %', p_new_tmid, p_rbid;
    END IF;

    SELECT sgl_terms_tmid
    INTO v_last_tmid
    FROM student.sgl_terms
    WHERE sgl_terms_start_date < (SELECT sgl_terms_start_date 
                                  FROM student.sgl_terms 
                                  WHERE sgl_terms_tmid = p_new_tmid)
    ORDER BY sgl_terms_tmid ASC
    LIMIT 1;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No previous term found for term %  and student %', p_new_tmid, p_rbid;
    END IF;

    SELECT sgm_stubi_stid, sgm_stubi_lvid, sgm_stubi_active_ind
    INTO v_prev_stid, v_next_lvid, v_next_active_ind
    FROM student.sgm_stubi
    WHERE sgm_stubi_rbid = p_rbid
          AND sgm_stubi_tmid = v_last_tmid;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No previous base record found for term %  and student %', v_last_tmid, p_rbid;
    END IF;   

    SELECT sgl_stype_next_stid
    INTO v_next_stid
    FROM student.sgl_stype
    WHERE sgl_stype_stid = v_prev_stid;
    IF NOT FOUND THEN
        v_next_stid := v_prev_stid;
    END IF; 
    IF v_next_stid != v_prev_stid THEN
        INSERT INTO student.sgm_stubi (
            sgm_stubi_tsid,
            sgm_stubi_rbid,
            sgm_stubi_tmid,
            sgm_stubi_lvid,
            sgm_stubi_stid,
            sgm_stubi_active_ind
        ) VALUES (
            p_rbid || p_new_tmid,
            p_rbid,
            p_new_tmid,
            v_next_lvid,
            v_next_stid,
            v_next_active_ind
        );
    END IF;
END;
$$;

-- ============================================
-- Create Table sdl_depts
-- ============================================

CREATE TABLE student.sdl_depts (
    sdl_depts_dpid character varying(4) NOT NULL,
    sdl_depts_cgid character varying(4) NOT NULL,
    sdl_depts_hr_name character varying(64) NOT NULL
);

COMMENT ON TABLE student.sdl_depts IS 'Academic department lookup table.';
COMMENT ON COLUMN student.sdl_depts.sdl_depts_dpid IS 'Department ID.';
COMMENT ON COLUMN student.sdl_depts.sdl_depts_cgid IS 'College ID.';
COMMENT ON COLUMN student.sdl_depts.sdl_depts_hr_name IS 'Department human-readable name.';

-- ============================================
-- Create Table srl_cours
-- ============================================

CREATE TABLE student.srl_cours (
    srl_cours_crid character varying(10) NOT NULL,
    srl_cours_sbid character varying(4) NOT NULL,
    srl_cours_crse_num character varying(6) NOT NULL,
    srl_cours_hr_name character varying(64) NOT NULL,
    srl_cours_active_ind character(1) NOT NULL,
    srl_cours_credit_hours integer,
    CONSTRAINT ck_srl_cours_inactive_ind CHECK ((srl_cours_active_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);

COMMENT ON TABLE student.srl_cours IS 'Course Lookup Table';
COMMENT ON COLUMN student.srl_cours.srl_cours_crid IS 'Course ID';
COMMENT ON COLUMN student.srl_cours.srl_cours_sbid IS 'Subject ID';
COMMENT ON COLUMN student.srl_cours.srl_cours_crse_num IS 'Course Number';
COMMENT ON COLUMN student.srl_cours.srl_cours_hr_name IS 'Course Title';
COMMENT ON COLUMN student.srl_cours.srl_cours_active_ind IS 'Active Indicator';
COMMENT ON COLUMN student.srl_cours.srl_cours_hr_name IS 'Credit Hours';


-- ============================================
-- Create Table srl_subjs
-- ============================================

CREATE TABLE student.srl_subjs (
    srl_subjs_sbid character varying(4) NOT NULL,
    srl_subjs_hr_name character varying(64),
    srl_subjs_dpid character varying(4)
);

COMMENT ON TABLE student.srl_subjs IS 'Course Subject Lookup Table';
COMMENT ON COLUMN student.srl_subjs.srl_subjs_sbid IS 'Subject ID';
COMMENT ON COLUMN student.srl_subjs.srl_subjs_hr_name IS 'Subject Human Readable Name';
COMMENT ON COLUMN student.srl_subjs.srl_subjs_dpid IS 'Department ID - References DCR_DEPTS.DCR_DEPTS_DPID';

-- ============================================
-- Create Table scm_stucv
-- ============================================

CREATE TABLE student.scm_stucv (
    scm_stucv_scid character varying(23) NOT NULL,
    scm_stucv_rbid character(9) NOT NULL,
    scm_stucv_cvid character varying(14) NOT NULL,
    scm_stucv_admit_term character(6) NOT NULL,
    scm_stucv_active_ind character(1) NOT NULL,
    scm_stucv_cpid character varying(2) NOT NULL,
    CONSTRAINT ck_scm_stucv_active_ind CHECK ((scm_stucv_active_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);

COMMENT ON TABLE student.scm_stucv IS 'Student-Curriculum Master Table';
COMMENT ON COLUMN student.scm_stucv.scm_stucv_scid IS 'Student-Curriculum ID';
COMMENT ON COLUMN student.scm_stucv.scm_stucv_rbid IS 'Student Ribbon ID';
COMMENT ON COLUMN student.scm_stucv.scm_stucv_cvid IS 'Curriculum Version ID';
COMMENT ON COLUMN student.scm_stucv.scm_stucv_admit_term IS 'Term Student was Admitted to Curriculum Program';
COMMENT ON COLUMN student.scm_stucv.scm_stucv_active_ind IS 'Active Indicator';
COMMENT ON COLUMN student.scm_stucv.scm_stucv_cpid IS 'Campus ID';

-- ============================================
-- Create Table scr_creqs
-- ============================================

CREATE TABLE student.scr_creqs (
    scr_creqs_rqid character varying(24) NOT NULL,
    scr_creqs_cvid character varying(14) NOT NULL,
    scr_creqs_crid character varying(10) NOT NULL,
    scr_creqs_rtid character varying(4) NOT NULL,
    scr_creqs_min_credits integer,
    scr_creqs_min_mkid character(1),
    scr_creqs_min_mark_avg numeric(5,2),
    scr_creqs_created_date date NOT NULL,
    scr_creqs_activity_date date,
    scr_creqs_modified_by character varying(40)
);

COMMENT ON TABLE student.scr_creqs IS 'Course requirements - individual courses required for curriculum. Links to groups for elective blocks.';
COMMENT ON COLUMN student.scr_creqs.scr_creqs_rqid IS 'Requirement ID (auto-generated).';
COMMENT ON COLUMN student.scr_creqs.scr_creqs_cvid IS 'Curriculum version ID.';
COMMENT ON COLUMN student.scr_creqs.scr_creqs_crid IS 'Course ID.';
COMMENT ON COLUMN student.scr_creqs.scr_creqs_rtid IS 'Requirement type ID (CORE, ELCA, ELCB, etc.).';
COMMENT ON COLUMN student.scr_creqs.scr_creqs_min_credits IS 'Minimum credits required (typically matches course credits).';
COMMENT ON COLUMN student.scr_creqs.scr_creqs_min_mkid IS 'Minimum grade letter required.';
COMMENT ON COLUMN student.scr_creqs.scr_creqs_min_mark_avg IS 'Minimum numeric grade required.';
COMMENT ON COLUMN student.scr_creqs.scr_creqs_created_date IS 'Date record was created.';
COMMENT ON COLUMN student.scr_creqs.scr_creqs_activity_date IS 'Date record was last modified.';
COMMENT ON COLUMN student.scr_creqs.scr_creqs_modified_by IS 'User who last modified record.';

-- ============================================
-- Create Table sgl_terms
-- ============================================

CREATE TABLE student.sgl_terms (
    sgl_terms_tmid character(6) NOT NULL,
    sgl_terms_year integer NOT NULL,
    sgl_terms_smid character(4) NOT NULL,
    sgl_terms_hr_name character varying(32) NOT NULL,
    sgl_terms_fyid character(4) NOT NULL,
    sgl_terms_start_date date NOT NULL,
    sgl_terms_end_date date NOT NULL
);

COMMENT ON TABLE student.sgl_terms IS 'Academic term lookup table';
COMMENT ON COLUMN student.sgl_terms.sgl_terms_tmid IS 'Term ID. Format: YYYY + semester code (1S = Summer, 2F = Fall, 3W = Winter)';
COMMENT ON COLUMN student.sgl_terms.sgl_terms_year IS 'Calendar year of the term';
COMMENT ON COLUMN student.sgl_terms.sgl_terms_smid IS 'Semester ID';
COMMENT ON COLUMN student.sgl_terms.sgl_terms_hr_name IS 'Term human-readable name';
COMMENT ON COLUMN student.sgl_terms.sgl_terms_fyid IS 'Financial aid year code';
COMMENT ON COLUMN student.sgl_terms.sgl_terms_start_date IS 'Term official start date';
COMMENT ON COLUMN student.sgl_terms.sgl_terms_end_date IS 'Term official end date';

-- ============================================
-- Create Table srb_sects
-- ============================================

CREATE TABLE student.srb_sects (
    srb_sects_stid character varying(18) NOT NULL,
    srb_sects_tmid character varying(6) NOT NULL,
    srb_sects_crid character varying(10) NOT NULL,
    srb_sects_section_seq integer NOT NULL,
    srb_sects_prim_inst character(9) NOT NULL,
    srb_sects_scnd_inst character(9)
);

COMMENT ON TABLE student.srb_sects IS 'Section bridge table';
COMMENT ON COLUMN student.srb_sects.srb_sects_stid IS 'Course, Term, Sequence ID';
COMMENT ON COLUMN student.srb_sects.srb_sects_tmid IS 'Term ID';
COMMENT ON COLUMN student.srb_sects.srb_sects_crid IS 'Course ID';
COMMENT ON COLUMN student.srb_sects.srb_sects_section_seq IS 'Section Sequence Number';
COMMENT ON COLUMN student.srb_sects.srb_sects_prim_inst IS 'Primary Instructor';
COMMENT ON COLUMN student.srb_sects.srb_sects_scnd_inst IS 'Secondary Instructor';

-- ============================================
-- Create Table srh_enrol
-- ============================================

CREATE TABLE student.srh_enrol (
    srh_enrol_erid character varying(27) NOT NULL,
    srh_enrol_rbid character(9) NOT NULL,
    srh_enrol_stid character varying(18) NOT NULL,
    srh_enrol_esid character(2) NOT NULL,
    srh_enrol_created_date date NOT NULL,
    srh_enrol_activity_date date NOT NULL,
    srh_enrol_modified_by character varying(40) NOT NULL
);

COMMENT ON TABLE student.srh_enrol IS 'Registration Status History Table';
COMMENT ON COLUMN student.srh_enrol.srh_enrol_erid IS 'Enrollment ID (auto-generated)';
COMMENT ON COLUMN student.srh_enrol.srh_enrol_rbid IS 'Ribbon ID';
COMMENT ON COLUMN student.srh_enrol.srh_enrol_stid IS 'Course section-term-sequence ID';
COMMENT ON COLUMN student.srh_enrol.srh_enrol_esid IS 'Enrollment status ID';
COMMENT ON COLUMN student.srh_enrol.srh_enrol_created_date IS 'Date record was created.';
COMMENT ON COLUMN student.srh_enrol.srh_enrol_activity_date IS 'Date record was last modified.';
COMMENT ON COLUMN student.srh_enrol.srh_enrol_modified_by IS 'User who last modified record.';

-- ============================================
-- Create Table srl_rqtyp
-- ============================================

CREATE TABLE student.srl_rqtyp (
    srl_rqtyp_rtid character varying(4) NOT NULL,
    srl_rqtyp_hr_name character varying(32) NOT NULL,
    srl_rqtyp_group_ind character(1),
    CONSTRAINT ck_srl_rqtyp_group_ind CHECK ((srl_rqtyp_group_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);

COMMENT ON TABLE student.srl_rqtyp IS 'Requirement type lookup table (e.g., CORE, ELCA, ELCB for elective blocks).';
COMMENT ON COLUMN student.srl_rqtyp.srl_rqtyp_rtid IS 'Requirement type ID.';
COMMENT ON COLUMN student.srl_rqtyp.srl_rqtyp_hr_name IS 'Requirement type human-readable name.';
COMMENT ON COLUMN student.srl_rqtyp.srl_rqtyp_group_ind IS 'Indicates if this type represents a group/block of courses (Y/N).';

-- ============================================
-- Create Table sth_crtrn
-- ============================================

CREATE TABLE student.sth_crtrn (
    sth_crtrn_erid character varying(27) NOT NULL,
    sth_crtrn_rbid character(9) NOT NULL,
    sth_crtrn_stid character varying(18) NOT NULL,
    sth_crtrn_final_mark_avg numeric(5,2),
    sth_crtrn_final_mkid character(1),
    sth_crtrn_created_date date NOT NULL,
    sth_crtrn_activity_date date NOT NULL,
    sth_crtrn_modified_by character varying(40) NOT NULL
);

COMMENT ON TABLE student.sth_crtrn IS 'Transcript History Table';
COMMENT ON COLUMN student.sth_crtrn.sth_crtrn_erid IS 'Enrollment ID.';
COMMENT ON COLUMN student.sth_crtrn.sth_crtrn_rbid IS 'Student Ribbon ID.';
COMMENT ON COLUMN student.sth_crtrn.sth_crtrn_stid IS 'Section ID.';
COMMENT ON COLUMN student.sth_crtrn.sth_crtrn_final_mark_avg IS 'Final Average Marl Percentage.';
COMMENT ON COLUMN student.sth_crtrn.sth_crtrn_final_mkid IS 'Final Mark Letter Grade - For GPA in USA.';

-- ============================================
-- Create Table scl_crtyp
-- ============================================

CREATE TABLE student.scl_crtyp (
    scl_crtyp_ctid character(4) NOT NULL,
    scl_crtyp_hr_name character varying(32),
    scl_crtyp_major_ind character(1),
    CONSTRAINT ck_scl_crtyp_major_ind CHECK ((scl_crtyp_major_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);

COMMENT ON TABLE student.scl_crtyp IS 'Curriculum type lookup table (e.g., Major, Minor, Certificate).';
COMMENT ON COLUMN student.scl_crtyp.scl_crtyp_ctid IS 'Curriculum type ID.';
COMMENT ON COLUMN student.scl_crtyp.scl_crtyp_hr_name IS 'Curriculum type human-readable name.';
COMMENT ON COLUMN student.scl_crtyp.scl_crtyp_major_ind IS 'Indicates if this type can be a major (Y/N).';

-- ============================================
-- Create Table scl_currv
-- ============================================

CREATE TABLE student.scl_currv (
    scl_currv_cvid character varying(14) NOT NULL,
    scl_currv_mrid character varying(8) NOT NULL,
    scl_currv_ctid character(4) NOT NULL,
    scl_currv_effective_term character(6) NOT NULL,
    scl_currv_end_term character(6),
    scl_currv_min_mark_avg numeric(6,2),
    scl_currv_min_gpa numeric(3,2),
    scl_currv_min_credits integer NOT NULL,
    scl_currv_created_date date NOT NULL,
    scl_currv_activity_date date,
    scl_currv_modified_by character varying(40)
);

COMMENT ON TABLE student.scl_currv IS 'Curriculum version table - tracks changes to major/degree requirements over time.';
COMMENT ON COLUMN student.scl_currv.scl_currv_cvid IS 'Curriculum version ID (auto-generated from major + term).';
COMMENT ON COLUMN student.scl_currv.scl_currv_mrid IS 'Major ID (foreign key to scl_major).';
COMMENT ON COLUMN student.scl_currv.scl_currv_effective_term IS 'Term when this curriculum version becomes effective.';
COMMENT ON COLUMN student.scl_currv.scl_currv_end_term IS 'Term when this curriculum version is no longer active (NULL if current).';
COMMENT ON COLUMN student.scl_currv.scl_currv_min_mark_avg IS 'Minimum GPA required for graduation under this curriculum.';
COMMENT ON COLUMN student.scl_currv.scl_currv_min_gpa IS 'Minimum cumulative GPA required.';
COMMENT ON COLUMN student.scl_currv.scl_currv_min_credits IS 'Minimum total credits required for graduation.';

-- ============================================
-- Create Table scl_major
-- ============================================

CREATE TABLE student.scl_major (
    scl_major_mrid character varying(8) NOT NULL,
    scl_major_hr_name character varying(64) NOT NULL,
    scl_major_short_name character varying(32) NOT NULL,
    scl_major_cgid character varying(4) NOT NULL,
    scl_major_dgid character varying(6) NOT NULL,
    scl_major_ciid character varying(7),
    scl_major_major_ind character(1) NOT NULL,
    scl_major_minor_ind character(1) NOT NULL,
    scl_major_ifid character varying(4),
    CONSTRAINT ck_scl_major_major_ind CHECK ((scl_major_major_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))),
    CONSTRAINT ck_scl_major_minor_ind CHECK ((scl_major_minor_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);

COMMENT ON TABLE student.scl_major IS 'Major report table.';
COMMENT ON COLUMN student.scl_major.scl_major_mrid IS 'Major ID.';
COMMENT ON COLUMN student.scl_major.scl_major_hr_name IS 'Major title.';
COMMENT ON COLUMN student.scl_major.scl_major_short_name IS 'Major short name.';
COMMENT ON COLUMN student.scl_major.scl_major_cgid IS 'Major college ID.';
COMMENT ON COLUMN student.scl_major.scl_major_dgid IS 'Major degree ID.';
COMMENT ON COLUMN student.scl_major.scl_major_ciid IS 'Major CIP Code.';
COMMENT ON COLUMN student.scl_major.scl_major_major_ind IS 'Indicates if this program can be declared as a major (Y/N).';
COMMENT ON COLUMN student.scl_major.scl_major_minor_ind IS 'Indicates if this program can be declared as a minor (Y/N).';

-- ============================================
-- Create Table sgm_stubi
-- ============================================

CREATE TABLE student.sgm_stubi (
    sgm_stubi_tsid character varying(15) NOT NULL,
    sgm_stubi_rbid character varying(9) NOT NULL,
    sgm_stubi_tmid character varying(6) NOT NULL,
    sgm_stubi_lvid character(2) NOT NULL,
    sgm_stubi_stid character varying(2) NOT NULL,
    sgm_stubi_active_ind character(1) NOT NULL,
    sgm_stubi_created_date date NOT NULL,
    sgm_stubi_activity_date date,
    sgm_stubi_modified_by character varying(40),
    CONSTRAINT ck_sgm_stubi_active_ind CHECK ((sgm_stubi_active_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);

COMMENT ON TABLE student.sgm_stubi IS 'Student base information table.';
COMMENT ON COLUMN student.sgm_stubi.sgm_stubi_tsid IS 'Student/Term ID of the update.';
COMMENT ON COLUMN student.sgm_stubi.sgm_stubi_lvid IS 'Student level ID.';
COMMENT ON COLUMN student.sgm_stubi.sgm_stubi_stid IS 'Student type ID.';
COMMENT ON COLUMN student.sgm_stubi.sgm_stubi_created_date IS 'Record creation date.';
COMMENT ON COLUMN student.sgm_stubi.sgm_stubi_activity_date IS 'Record last modification date.';
COMMENT ON COLUMN student.sgm_stubi.sgm_stubi_modified_by IS 'User who last modified the record.';

-- ============================================
-- Create Table sgl_level
-- ============================================

CREATE TABLE student.sgl_level (
    sgl_level_lvid character(2) NOT NULL,
    sgl_level_hr_name character varying(32) NOT NULL,
    sgl_level_degree_ind character(1) NOT NULL,
    CONSTRAINT ck_sgl_level_degree_ind CHECK ((sgl_level_degree_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);

COMMENT ON TABLE student.sgl_level IS 'Student level lookup table.';
COMMENT ON COLUMN student.sgl_level.sgl_level_lvid IS 'Level ID.';
COMMENT ON COLUMN student.sgl_level.sgl_level_hr_name IS 'Level human-readable name.';
COMMENT ON COLUMN student.sgl_level.sgl_level_degree_ind IS 'Degree-seeking indicator.';

-- ============================================
-- Create Table sgl_stype
-- ============================================

CREATE TABLE student.sgl_stype (
    sgl_stype_stid character varying(2) NOT NULL,
    sgl_stype_hr_name character varying(32) NOT NULL,
    sgl_stype_next_stid character varying(2)
);

COMMENT ON TABLE student.sgl_stype IS 'Student type lookup table.';
COMMENT ON COLUMN student.sgl_stype.sgl_stype_stid IS 'Student type ID.';
COMMENT ON COLUMN student.sgl_stype.sgl_stype_hr_name IS 'Student type human-readable name.';
COMMENT ON COLUMN student.sgl_stype.sgl_stype_next_stid IS 'Next student type ID for progression mappings.';

-- ============================================
-- Create Table sal_avtyp
-- ============================================

CREATE TABLE student.sal_avtyp (
    sal_avtyp_avid character varying(4) NOT NULL,
    sal_avtyp_hr_name character varying(32),
    sal_avtyp_created_date date NOT NULL,
    sal_avtyp_activity_date date NOT NULL,
    sal_avtyp_modified_by character varying(40) NOT NULL
);

COMMENT ON TABLE student.sal_avtyp IS 'Advisor Type Lookup Table.';
COMMENT ON COLUMN student.sal_avtyp.sal_avtyp_avid IS 'Advisor type ID.';
COMMENT ON COLUMN student.sal_avtyp.sal_avtyp_hr_name IS 'Advisor type human-readable name.';

-- ============================================
-- Create Table sar_advrl
-- ============================================

CREATE TABLE student.sar_advrl (
    sar_advrl_arid character varying(6) NOT NULL,
    sar_advrl_avid character varying(4) NOT NULL,
    sar_advrl_begin_letter character(1) NOT NULL,
    sar_advrl_end_letter character(1) NOT NULL,
    sar_advrl_advr_rbid character(9) NOT NULL,
    sar_advrl_created_date date NOT NULL,
    sar_advrl_activity_date date NOT NULL,
    sar_advrl_modified_by character varying(40) NOT NULL
);

COMMENT ON TABLE student.sar_advrl IS 'Advisor Rule Table.';
COMMENT ON COLUMN student.sar_advrl.sal_avtyp_avid IS 'Advisor rule ID.';
COMMENT ON COLUMN student.sar_advrl.sal_avtyp_avid IS 'Advisor type ID.';
COMMENT ON COLUMN student.sar_advrl.sar_advrl_begin_letter IS 'Student Last Name Begin Letter.';
COMMENT ON COLUMN student.sar_advrl.sar_advrl_end_letter IS 'Student Last Name End Letter.';
COMMENT ON COLUMN student.sar_advrl.sar_advrl_advr_rbid IS 'Advisor Ribbon ID.';

-- ============================================
-- Create Table sar_ovrar
-- ============================================

CREATE TABLE student.sar_ovrar (
    sar_ovrar_oaid character varying(15) NOT NULL,
    sar_ovrar_arid character varying(6) NOT NULL,
    sar_ovrar_stdn_rbid character(9) NOT NULL,
    sar_ovrar_advr_rbid character(9) NOT NULL,
    sar_ovrar_reason text NOT NULL,
    sar_ovrar_approved_by character(9) NOT NULL,
    sar_ovrar_created_date date NOT NULL,
    sar_ovrar_activity_date date NOT NULL,
    sar_ovrar_modified_by character varying(40) NOT NULL
);

COMMENT ON TABLE student.sar_ovrar IS 'Advisor Override Repeating Table.';
COMMENT ON COLUMN student.sar_ovrar.sar_ovrar_arid IS 'Advisor rule ID.';
COMMENT ON COLUMN student.sar_ovrar.sar_ovrar_stdn_rbid IS 'Student Ribbon ID.';
COMMENT ON COLUMN student.sar_ovrar.sar_ovrar_advr_rbid IS 'Approver Ribbon ID.';
COMMENT ON COLUMN student.sar_ovrar.sar_ovrar_reason IS 'Advisor rule ID.';
COMMENT ON COLUMN student.sar_ovrar.sar_ovrar_approved_by IS 'Approver Ribbon ID.';

-- ============================================
-- Create Table scl_cipcd
-- ============================================

CREATE TABLE student.scl_cipcd (
    scl_cipcd_ciid character varying(7) NOT NULL,
    scl_cipcd_hr_name character varying(50) NOT NULL,
    scl_cipcd_cal_sp04_code character(5),
    scl_cipcd_publish_date date,
    CONSTRAINT ck_scl_cipcd_ciid CHECK (((scl_cipcd_ciid)::text ~ '^[0-9]{2}([.][0-9]{2}|[.][0-9]{4})?$'::text))
);

COMMENT ON TABLE student.scl_cipcd IS 'CIP code definition table.';
COMMENT ON COLUMN student.scl_cipcd.scl_cipcd_ciid IS 'CIP code ID in NCES format (2, 4, or 6 digit structure).';
COMMENT ON COLUMN student.scl_cipcd.scl_cipcd_hr_name IS 'CIP code human-readable name.';
COMMENT ON COLUMN student.scl_cipcd.scl_cipcd_cal_sp04_code IS 'SP04 reporting code for the CIP classification.';
COMMENT ON COLUMN student.scl_cipcd.scl_cipcd_publish_date IS 'Date the CIP code was published.';

-- ============================================
-- Create Table scl_degrs
-- ============================================

CREATE TABLE student.scl_degrs (
    scl_degrs_dgid character varying(6) NOT NULL,
    scl_degrs_hr_name character varying(64) NOT NULL,
    scl_degrs_dlid character varying(4) NOT NULL,
    scl_degrs_finaid_ind character(1)
);

COMMENT ON TABLE student.scl_degrs IS 'Degree lookup table.';
COMMENT ON COLUMN student.scl_degrs.scl_degrs_dgid IS 'Degree ID.';
COMMENT ON COLUMN student.scl_degrs.scl_degrs_hr_name IS 'Degree human-readable name.';
COMMENT ON COLUMN student.scl_degrs.scl_degrs_dlid IS 'Degree level ID.';
COMMENT ON COLUMN student.scl_degrs.scl_degrs_finaid_ind IS 'Degree financial aid indicator.';

-- ============================================
-- Create Table scl_dlevl
-- ============================================

CREATE TABLE student.scl_dlevl (
    scl_dlevl_dlid character varying(4) NOT NULL,
    scl_dlevl_hr_name character varying(32) NOT NULL,
    scl_dlevl_nslds_equiv character(2),
    scl_dlevl_eqf_equiv character(1),
    scl_dlevl_lvid character(2) NOT NULL
);

COMMENT ON TABLE student.scl_dlevl IS 'Degree level lookup table.';
COMMENT ON COLUMN student.scl_dlevl.scl_dlevl_dlid IS 'Degree level ID.';
COMMENT ON COLUMN student.scl_dlevl.scl_dlevl_hr_name IS 'Degree level human-readable name.';
COMMENT ON COLUMN student.scl_dlevl.scl_dlevl_nslds_equiv IS 'Degree level National Student Loan Data System category code.';
COMMENT ON COLUMN student.scl_dlevl.scl_dlevl_eqf_equiv IS 'European Qualifications Framework equivalency.';
COMMENT ON COLUMN student.scl_dlevl.scl_dlevl_lvid IS 'Student level ID.';

-- ============================================
-- Create Table scl_iscdf
-- ============================================

CREATE TABLE student.scl_iscdf (
    scl_iscdf_ifid character varying(4) NOT NULL,
    scl_iscdf_hr_name character varying(50) NOT NULL,
    CONSTRAINT ck_scl_iscdf_ifid CHECK (((scl_iscdf_ifid)::text ~ '^[0-9]{2,4}$'::text))
);

COMMENT ON TABLE student.scl_iscdf IS 'ISCED F lookup table.';
COMMENT ON COLUMN student.scl_iscdf.scl_iscdf_ifid IS 'ISCED F ID.';
COMMENT ON COLUMN student.scl_iscdf.scl_iscdf_hr_name IS 'ISCED F human-readable name.';

-- ============================================
-- Create Table scr_ovcls
-- ============================================

CREATE TABLE student.scr_ovcls (
    scr_ovcls_ocid character varying(41) NOT NULL,
    scr_ovcls_scid character varying(17) NOT NULL,
    scr_ovcls_rqid character varying(24) NOT NULL,
    scr_ovcls_crid character varying(10) NOT NULL,
    scr_ovcls_reason text NOT NULL,
    scr_ovcls_approved_by character(9) NOT NULL,
    scr_ovcls_created_date date NOT NULL,
    scr_ovcls_activity_date date,
    scr_ovcls_modified_by character varying(40)
);

COMMENT ON TABLE student.scr_ovcls IS 'Curriuculum Course Override table.';
COMMENT ON COLUMN student.scr_ovcls.scr_ovcls_ocid IS 'Ovveride Course ID.';
COMMENT ON COLUMN student.scr_ovcls.scr_ovcls_scid IS 'Student Curriculum ID.';
COMMENT ON COLUMN student.scr_ovcls.scr_ovcls_rqid IS 'Requirement ID.';
COMMENT ON COLUMN student.scr_ovcls.scr_ovcls_crid IS 'Course ID.';
COMMENT ON COLUMN student.scr_ovcls.scr_ovcls_reason IS 'Override Reason ID.';
COMMENT ON COLUMN student.scr_ovcls.scr_ovcls_approved_by IS 'Approver Ribbon ID.';

-- ============================================
-- Create Table scr_ovmrk
-- ============================================

CREATE TABLE student.scr_ovmrk (
    scr_ovmrk_omid character varying(41) NOT NULL,
    scr_ovmrk_scid character varying(17) NOT NULL,
    scr_ovmrk_rqid character varying(24) NOT NULL,
    scr_ovmrk_mkid character(1) NOT NULL,
    scr_ovmrk_mark_avg numeric(5,2),
    scr_ovmrk_reason text NOT NULL,
    scr_ovmrk_approved_by character(9) NOT NULL,
    scr_ovmrk_created_date date NOT NULL,
    scr_ovmrk_activity_date date,
    scr_ovmrk_modified_by character varying(40)
);

COMMENT ON TABLE student.scr_ovmrk IS 'Curriuculum Marks Override table.';
COMMENT ON COLUMN student.scr_ovmrk.scr_ovmrk_omid IS 'Ovveride Course ID.';
COMMENT ON COLUMN student.scr_ovmrk.scr_ovmrk_scid IS 'Student Curriculum ID.';
COMMENT ON COLUMN student.scr_ovmrk.scr_ovmrk_rqid IS 'Requirement ID.';
COMMENT ON COLUMN student.scr_ovmrk.scr_ovmrk_mkid IS 'Letter Mark ID.';
COMMENT ON COLUMN student.scr_ovmrk.scr_ovmrk_mark_avg IS 'Mark Average.';
COMMENT ON COLUMN student.scr_ovmrk.scr_ovmrk_reason IS 'Override Reason ID.';
COMMENT ON COLUMN student.scr_ovmrk.scr_ovmrk_approved_by IS 'Approver Ribbon ID.';


-- ============================================
-- Create Table scr_preqs
-- ============================================

CREATE TABLE student.scr_preqs (
    scr_preqs_pqid character varying(12) NOT NULL,
    scr_preqs_crid character varying(6) NOT NULL,
    scr_preqs_req_crid character varying(6) NOT NULL,
    scr_preqs_min_grade character(1)
);

COMMENT ON TABLE student.scr_preqs IS 'Course prerequisite mapping table.';
COMMENT ON COLUMN student.scr_preqs.scr_preqs_pqid IS 'Prerequisite ID (auto-generated from course IDs).';
COMMENT ON COLUMN student.scr_preqs.scr_preqs_crid IS 'Course ID that has the prerequisite requirement.';
COMMENT ON COLUMN student.scr_preqs.scr_preqs_req_crid IS 'Required prerequisite course ID.';
COMMENT ON COLUMN student.scr_preqs.scr_preqs_min_grade IS 'Minimum grade required in prerequisite course.';

-- ============================================
-- Create Table scr_rqgrp
-- ============================================

CREATE TABLE student.scr_rqgrp (
    scr_rqgrp_rgid character varying(18) NOT NULL,
    scr_rqgrp_cvid character varying(14) NOT NULL,
    scr_rqgrp_rtid character varying(4) NOT NULL,
    scr_rqgrp_hr_name character varying(64) NOT NULL,
    scr_rqgrp_min_courses integer,
    scr_rqgrp_min_credits integer,
    scr_rqgrp_min_mark_avg numeric(5,2),
    scr_rqgrp_created_date date NOT NULL,
    scr_rqgrp_activity_date date,
    scr_rqgrp_modified_by character varying(40)
);

COMMENT ON TABLE student.scr_rqgrp IS 'Requirement groups/blocks - defines elective blocks and course groups for curriculum. E.g., "6 credits from Block A courses".';
COMMENT ON COLUMN student.scr_rqgrp.scr_rqgrp_rgid IS 'Requirement group ID (auto-generated).';
COMMENT ON COLUMN student.scr_rqgrp.scr_rqgrp_cvid IS 'Curriculum version ID.';
COMMENT ON COLUMN student.scr_rqgrp.scr_rqgrp_rtid IS 'Requirement type ID (typically ELCA, ELCB, ELCC, etc.).';
COMMENT ON COLUMN student.scr_rqgrp.scr_rqgrp_hr_name IS 'Group human-readable name (e.g., "Upper Division Technical Electives").';
COMMENT ON COLUMN student.scr_rqgrp.scr_rqgrp_min_courses IS 'Minimum number of courses required from this group.';
COMMENT ON COLUMN student.scr_rqgrp.scr_rqgrp_min_credits IS 'Minimum credit hours required from this group.';
COMMENT ON COLUMN student.scr_rqgrp.scr_rqgrp_min_mark_avg IS 'Minimum average mark required for courses in this group.';

-- ============================================
-- Create Table sdl_camps
-- ============================================

CREATE TABLE student.sdl_camps (
    sdl_camps_cpid character varying(2) NOT NULL,
    sdl_camps_hr_name character varying(32) NOT NULL
);

COMMENT ON TABLE student.sdl_camps IS 'Campus definition table.';
COMMENT ON COLUMN student.sdl_camps.sdl_camps_cpid IS 'Campus ID.';
COMMENT ON COLUMN student.sdl_camps.sdl_camps_hr_name IS 'Campus human-readable name.';

-- ============================================
-- Create Table sdl_coleg
-- ============================================

CREATE TABLE student.sdl_coleg (
    sdl_coleg_cgid character varying(4) NOT NULL,
    sdl_coleg_hr_name character varying(64) NOT NULL,
    sdl_coleg_short_name character varying(32) NOT NULL
);

COMMENT ON TABLE student.sdl_coleg IS 'College/school definition table.';
COMMENT ON COLUMN student.sdl_coleg.sdl_coleg_cgid IS 'Campus ID.';
COMMENT ON COLUMN student.sdl_coleg.sdl_coleg_hr_name IS 'Campus human-readable name.';
COMMENT ON COLUMN student.sdl_coleg.sdl_coleg_short_name IS 'College short name.';

-- ============================================
-- Create Table sgl_smstr
-- ============================================

CREATE TABLE student.sgl_smstr (
    sgl_smstr_smid character(4) NOT NULL,
    sgl_smstr_hr_name character varying(6) NOT NULL
);

COMMENT ON TABLE student.sgl_smstr IS 'Semester definition table.';
COMMENT ON COLUMN student.sgl_smstr.sgl_smstr_smid IS 'Semester ID.';
COMMENT ON COLUMN student.sgl_smstr.sgl_smstr_hr_name IS 'Semester human-readable name.';

-- ============================================
-- Create Table srh_sterm
-- ============================================

CREATE TABLE student.srh_sterm (
    srh_sterm_tsid character(15) NOT NULL,
    srh_sterm_rbid character(9) NOT NULL,
    srh_sterm_tmid character(6) NOT NULL,
    srh_sterm_rgid character varying(4) NOT NULL,
    srh_sterm_created_date date NOT NULL,
    srh_sterm_activity_date date,
    srh_sterm_modified_by character varying(40)
);

COMMENT ON TABLE student.srh_sterm IS 'Student base information table.';
COMMENT ON COLUMN student.srh_sterm.srh_sterm_tsid IS 'Student/Term ID (auto-generated)';
COMMENT ON COLUMN student.srh_sterm.srh_sterm_rbid IS 'Ribbon ID';
COMMENT ON COLUMN student.srh_sterm.srh_sterm_tmid IS 'Term ID';
COMMENT ON COLUMN student.srh_sterm.srh_sterm_rgid IS 'Registration Type ID';
COMMENT ON COLUMN student.srh_sterm.srh_sterm_activity_date IS 'Record last modification date.';
COMMENT ON COLUMN student.srh_sterm.srh_sterm_modified_by IS 'User who last modified the record.';

-- ============================================
-- Create Table srl_enrst
-- ============================================

CREATE TABLE student.srl_enrst (
    srl_enrst_esid character(2) NOT NULL,
    srl_enrst_hr_name character varying(32) NOT NULL,
    srl_enrst_roll_ind character(1) NOT NULL,
    srl_enrst_credit_ind character(1) NOT NULL,
    CONSTRAINT ck_srl_enrst_credit_ind CHECK ((srl_enrst_credit_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))),
    CONSTRAINT ck_srl_enrst_roll_ind CHECK ((srl_enrst_roll_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);

COMMENT ON TABLE student.srl_enrst IS 'Enrollment Status Lookup Table with Predefined Values. 
     Combines roll and credit flags to indicate enrollment semantics:
     - Y,Y = Normal registration (Registered, Web Registered, Admin Registered, Vendor Registered)
     - N,N = Withdrawal (Withdraw, Web Withdraw, Admin Withdraw, Vendor Withdraw)
     - N,Y = Special cases (Credited Withdraw, Transfer Course, Honorary Course)
     - Y,N = Audit';
COMMENT ON COLUMN student.srl_enrst.srl_enrst_esid IS 'Enrollment Status ID';
COMMENT ON COLUMN student.srl_enrst.srl_enrst_hr_name IS 'Enrollment Status Human Readable Name';
COMMENT ON COLUMN student.srl_enrst.srl_enrst_roll_ind IS 'Indicates if student is enrolled in the course (Y/N).';
COMMENT ON COLUMN student.srl_enrst.srl_enrst_credit_ind IS 'Indicates if student receives credit for the course (Y/N).';

-- ============================================
-- Create Table srl_rgtyp
-- ============================================

CREATE TABLE student.srl_rgtyp (
    srl_rgtyp_rgid character varying(4) NOT NULL,
    srl_rgtyp_hr_name character varying(32),
    srl_rgtyp_enrol_ind character(1),
    srl_rgtyp_count_ind character(1),
    srl_rgtyp_audit_ind character(1),
    CONSTRAINT ck_srl_rgtyp_audit_ind CHECK ((srl_rgtyp_enrol_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))),
    CONSTRAINT ck_srl_rgtyp_count_ind CHECK ((srl_rgtyp_enrol_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))),
    CONSTRAINT ck_srl_rgtyp_enrol_ind CHECK ((srl_rgtyp_enrol_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);

COMMENT ON TABLE student.srl_rgtyp IS 'Registration type lookup table.';
COMMENT ON COLUMN student.srl_rgtyp.srl_rgtyp_rgid IS 'Registration ID';
COMMENT ON COLUMN student.srl_rgtyp.srl_rgtyp_enrol_ind IS 'Enrolled indicatior';
COMMENT ON COLUMN student.srl_rgtyp.srl_rgtyp_count_ind IS 'Counts for Credit indicatior';
COMMENT ON COLUMN student.srl_rgtyp.srl_rgtyp_audit_ind IS 'Audit indicatior';

-- ============================================
-- Create Table stl_marks
-- ============================================

CREATE TABLE student.stl_marks (
    stl_marks_mkid character(1) NOT NULL,
    stl_marks_credit_hr_gp integer
);

COMMENT ON TABLE student.stl_marks IS 'Grade marks/letters lookup table with quality points for GPA calculation.';
COMMENT ON COLUMN student.stl_marks.stl_marks_mkid IS 'Mark/Grade letter (A, B, C, D, F, etc.).';
COMMENT ON COLUMN student.stl_marks.stl_marks_credit_hr_gp IS 'Grade points per credit hour for GPA calculation (4.0 scale).';

-- ============================================
-- Create PK and Unique Constraints
-- ============================================

ALTER TABLE ONLY student.srl_rgtyp
    ADD CONSTRAINT pk_rgtyp PRIMARY KEY (srl_rgtyp_rgid);

ALTER TABLE ONLY student.sal_avtyp
    ADD CONSTRAINT pk_sal_avtyp PRIMARY KEY (sal_avtyp_avid);

ALTER TABLE ONLY student.sar_advrl
    ADD CONSTRAINT pk_sar_advrl PRIMARY KEY (sar_advrl_arid);

ALTER TABLE ONLY student.sar_ovrar
    ADD CONSTRAINT pk_sar_ovrar PRIMARY KEY (sar_ovrar_oaid);

ALTER TABLE ONLY student.scl_cipcd
    ADD CONSTRAINT pk_scl_cipcd PRIMARY KEY (scl_cipcd_ciid);

ALTER TABLE ONLY student.scl_crtyp
    ADD CONSTRAINT pk_scl_crtyp PRIMARY KEY (scl_crtyp_ctid);

ALTER TABLE ONLY student.scl_currv
    ADD CONSTRAINT pk_scl_currv PRIMARY KEY (scl_currv_cvid);

ALTER TABLE ONLY student.scl_degrs
    ADD CONSTRAINT pk_scl_degrs PRIMARY KEY (scl_degrs_dgid);

ALTER TABLE ONLY student.scl_dlevl
    ADD CONSTRAINT pk_scl_dlevl PRIMARY KEY (scl_dlevl_dlid);

ALTER TABLE ONLY student.scl_iscdf
    ADD CONSTRAINT pk_scl_iscdf PRIMARY KEY (scl_iscdf_ifid);

ALTER TABLE ONLY student.scl_major
    ADD CONSTRAINT pk_scl_major PRIMARY KEY (scl_major_mrid);

ALTER TABLE ONLY student.scm_stucv
    ADD CONSTRAINT pk_scm_stucv PRIMARY KEY (scm_stucv_scid);

ALTER TABLE ONLY student.scr_creqs
    ADD CONSTRAINT pk_scr_creqs PRIMARY KEY (scr_creqs_rqid);

ALTER TABLE ONLY student.scr_ovcls
    ADD CONSTRAINT pk_scr_ovcls PRIMARY KEY (scr_ovcls_ocid);

ALTER TABLE ONLY student.scr_ovmrk
    ADD CONSTRAINT pk_scr_ovmrk_omid PRIMARY KEY (scr_ovmrk_omid);

ALTER TABLE ONLY student.scr_preqs
    ADD CONSTRAINT pk_scr_preqs PRIMARY KEY (scr_preqs_pqid);

ALTER TABLE ONLY student.scr_rqgrp
    ADD CONSTRAINT pk_scr_rqgrp PRIMARY KEY (scr_rqgrp_rgid);

ALTER TABLE ONLY student.sdl_camps
    ADD CONSTRAINT pk_sdl_camps PRIMARY KEY (sdl_camps_cpid);

ALTER TABLE ONLY student.sdl_coleg
    ADD CONSTRAINT pk_sdl_coleg PRIMARY KEY (sdl_coleg_cgid);

ALTER TABLE ONLY student.sdl_depts
    ADD CONSTRAINT pk_sdl_depts PRIMARY KEY (sdl_depts_dpid);

ALTER TABLE ONLY student.sgl_level
    ADD CONSTRAINT pk_sgl_level PRIMARY KEY (sgl_level_lvid);

ALTER TABLE ONLY student.sgl_smstr
    ADD CONSTRAINT pk_sgl_smstr PRIMARY KEY (sgl_smstr_smid);

ALTER TABLE ONLY student.sgl_stype
    ADD CONSTRAINT pk_sgl_stype PRIMARY KEY (sgl_stype_stid);

ALTER TABLE ONLY student.sgl_terms
    ADD CONSTRAINT pk_sgl_terms PRIMARY KEY (sgl_terms_tmid);

ALTER TABLE ONLY student.sgm_stubi
    ADD CONSTRAINT pk_sgm_stubi PRIMARY KEY (sgm_stubi_tsid);

ALTER TABLE ONLY student.srb_sects
    ADD CONSTRAINT pk_srb_sects PRIMARY KEY (srb_sects_stid);

ALTER TABLE ONLY student.srh_enrol
    ADD CONSTRAINT pk_srh_enrol PRIMARY KEY (srh_enrol_erid);

ALTER TABLE ONLY student.srh_sterm
    ADD CONSTRAINT pk_srh_sterm PRIMARY KEY (srh_sterm_tsid);

ALTER TABLE ONLY student.srl_cours
    ADD CONSTRAINT pk_srl_cours PRIMARY KEY (srl_cours_crid);

ALTER TABLE ONLY student.srl_enrst
    ADD CONSTRAINT pk_srl_enrst PRIMARY KEY (srl_enrst_esid);

ALTER TABLE ONLY student.srl_rqtyp
    ADD CONSTRAINT pk_srl_rqtyp PRIMARY KEY (srl_rqtyp_rtid);

ALTER TABLE ONLY student.srl_subjs
    ADD CONSTRAINT pk_srl_subjs PRIMARY KEY (srl_subjs_sbid);

ALTER TABLE ONLY student.sth_crtrn
    ADD CONSTRAINT pk_sth_crtrn PRIMARY KEY (sth_crtrn_erid);

ALTER TABLE ONLY student.stl_marks
    ADD CONSTRAINT pk_stl_marks PRIMARY KEY (stl_marks_mkid);

ALTER TABLE ONLY student.sar_advrl
    ADD CONSTRAINT uk_sar_advrl_avid_begin_letter_end_letter UNIQUE (sar_advrl_avid, sar_advrl_begin_letter, sar_advrl_end_letter);

ALTER TABLE ONLY student.sar_ovrar
    ADD CONSTRAINT uk_sar_ovrar_arid_stdn_rbid UNIQUE (sar_ovrar_arid, sar_ovrar_stdn_rbid);

ALTER TABLE ONLY student.scl_currv
    ADD CONSTRAINT uk_scl_currv_mrid_effective_term UNIQUE (scl_currv_mrid, scl_currv_effective_term);

ALTER TABLE ONLY student.scm_stucv
    ADD CONSTRAINT uk_scm_stucv_rbid_cvid UNIQUE (scm_stucv_rbid, scm_stucv_cvid);

ALTER TABLE ONLY student.scr_creqs
    ADD CONSTRAINT uk_scr_creqs_cvid_crid UNIQUE (scr_creqs_cvid, scr_creqs_crid);

ALTER TABLE ONLY student.scr_ovcls
    ADD CONSTRAINT uk_scr_ovcls_scid_rqid UNIQUE (scr_ovcls_scid, scr_ovcls_rqid);

ALTER TABLE ONLY student.scr_ovmrk
    ADD CONSTRAINT uk_scr_ovmrk_scid_rqid UNIQUE (scr_ovmrk_scid, scr_ovmrk_rqid);

ALTER TABLE ONLY student.scr_rqgrp
    ADD CONSTRAINT uk_scr_rqgrp_cvid_seq UNIQUE (scr_rqgrp_cvid, scr_rqgrp_rtid);

ALTER TABLE ONLY student.sgl_terms
    ADD CONSTRAINT uk_sgl_terms_year_sgl_terms_smid UNIQUE (sgl_terms_year, sgl_terms_smid);

ALTER TABLE ONLY student.sgm_stubi
    ADD CONSTRAINT uk_sgm_stubi_rbid_tmid UNIQUE (sgm_stubi_rbid, sgm_stubi_tmid);

ALTER TABLE ONLY student.srb_sects
    ADD CONSTRAINT uk_srb_sects_tmid_crid_seq UNIQUE (srb_sects_tmid, srb_sects_crid, srb_sects_section_seq);

ALTER TABLE ONLY student.srh_enrol
    ADD CONSTRAINT uk_srh_enrol_rbid_stid UNIQUE (srh_enrol_rbid, srh_enrol_stid);

ALTER TABLE ONLY student.srh_sterm
    ADD CONSTRAINT uk_srh_sterm_rbid_tmid UNIQUE (srh_sterm_rbid, srh_sterm_tmid);

ALTER TABLE ONLY student.srl_cours
    ADD CONSTRAINT uk_srl_cours UNIQUE (srl_cours_sbid, srl_cours_crse_num);

ALTER TABLE ONLY student.sth_crtrn
    ADD CONSTRAINT uk_sth_crtrn_rbid_stid UNIQUE (sth_crtrn_rbid, sth_crtrn_stid);

-- ============================================
-- Create Triggers
-- ============================================

CREATE TRIGGER tr_sal_avtyp_audit_insert BEFORE INSERT ON student.sal_avtyp FOR EACH ROW EXECUTE FUNCTION student.fn_sal_avtyp_audit_insert();
CREATE TRIGGER tr_sal_avtyp_audit_update BEFORE UPDATE ON student.sal_avtyp FOR EACH ROW EXECUTE FUNCTION student.fn_sal_avtyp_audit_update();
CREATE TRIGGER tr_sar_advrl_arid_autogen BEFORE INSERT OR UPDATE ON student.sar_advrl FOR EACH ROW EXECUTE FUNCTION student.fn_sar_advrl_arid_autogen();
CREATE TRIGGER tr_sar_advrl_audit_insert BEFORE INSERT ON student.sar_advrl FOR EACH ROW EXECUTE FUNCTION student.fn_sar_advrl_audit_insert();
CREATE TRIGGER tr_sar_advrl_audit_update BEFORE UPDATE ON student.sar_advrl FOR EACH ROW EXECUTE FUNCTION student.fn_sar_advrl_audit_update();
CREATE TRIGGER tr_sar_ovrar_audit_insert BEFORE INSERT OR UPDATE ON student.sar_ovrar FOR EACH ROW EXECUTE FUNCTION student.fn_sar_ovrar_validate_lastname();
CREATE TRIGGER tr_sar_ovrar_oaid_autogen BEFORE INSERT OR UPDATE ON student.sar_advrl FOR EACH ROW EXECUTE FUNCTION student.fn_sar_ovrar_oaid_autogen();
CREATE TRIGGER tr_scl_currv_audit_insert BEFORE INSERT ON student.scl_currv FOR EACH ROW EXECUTE FUNCTION student.fn_scl_currv_audit_insert();
CREATE TRIGGER tr_scl_currv_audit_update BEFORE UPDATE ON student.scl_currv FOR EACH ROW EXECUTE FUNCTION student.fn_scl_currv_audit_update();
CREATE TRIGGER tr_scl_currv_cvid_autogen BEFORE INSERT OR UPDATE ON student.scl_currv FOR EACH ROW EXECUTE FUNCTION student.fn_scl_currv_cvid_autogen();
CREATE TRIGGER tr_scl_currv_set_end_terms BEFORE INSERT ON student.scl_currv FOR EACH ROW EXECUTE FUNCTION student.fn_scl_currv_set_end_terms();
CREATE TRIGGER tr_scm_stucv_scid_autogen BEFORE INSERT OR UPDATE ON student.scm_stucv FOR EACH ROW EXECUTE FUNCTION student.fn_scm_stucv_scid_autogen();
CREATE TRIGGER tr_scr_creqs_audit_insert BEFORE INSERT ON student.scr_creqs FOR EACH ROW EXECUTE FUNCTION student.fn_scr_creqs_audit_insert();
CREATE TRIGGER tr_scr_creqs_audit_update BEFORE UPDATE ON student.scr_creqs FOR EACH ROW EXECUTE FUNCTION student.fn_scr_creqs_audit_update();
CREATE TRIGGER tr_scr_creqs_rqid_autogen BEFORE INSERT OR UPDATE ON student.scr_creqs FOR EACH ROW EXECUTE FUNCTION student.fn_scr_creqs_rqid_autogen();
CREATE TRIGGER tr_scr_ovcls_ocid_autogen BEFORE INSERT OR UPDATE ON student.scr_ovcls FOR EACH ROW EXECUTE FUNCTION student.fn_scr_ovcls_ocid_autogen();
CREATE TRIGGER tr_scr_ovcls_validate_curriculum BEFORE INSERT OR UPDATE ON student.scr_ovcls FOR EACH ROW EXECUTE FUNCTION student.fn_scr_ovcls_validate_curriculum();
CREATE TRIGGER tr_scr_ovmrk_audit_insert BEFORE INSERT ON student.scr_ovmrk FOR EACH ROW EXECUTE FUNCTION student.fn_scr_ovmrk_audit_insert();
CREATE TRIGGER tr_scr_ovmrk_audit_update BEFORE UPDATE ON student.scr_ovmrk FOR EACH ROW EXECUTE FUNCTION student.fn_scr_ovmrk_audit_update();
CREATE TRIGGER tr_scr_ovmrk_omid_autogen BEFORE INSERT OR UPDATE ON student.scr_ovmrk FOR EACH ROW EXECUTE FUNCTION student.fn_scr_ovmrk_omid_autogen();
CREATE TRIGGER tr_scr_ovmrk_validate_curriculum BEFORE INSERT OR UPDATE ON student.scr_ovmrk FOR EACH ROW EXECUTE FUNCTION student.fn_scr_ovmrk_validate_curriculum();
CREATE TRIGGER tr_scr_preqs_pqid_autogen BEFORE INSERT OR UPDATE ON student.scr_preqs FOR EACH ROW EXECUTE FUNCTION student.fn_scr_preqs_pqid_autogen();
CREATE TRIGGER tr_scr_rqgrp_audit_insert BEFORE INSERT ON student.scr_rqgrp FOR EACH ROW EXECUTE FUNCTION student.fn_scr_rqgrp_audit_insert();
CREATE TRIGGER tr_scr_rqgrp_audit_update BEFORE UPDATE ON student.scr_rqgrp FOR EACH ROW EXECUTE FUNCTION student.fn_scr_rqgrp_audit_update();
CREATE TRIGGER tr_scr_scr_rqgrp_rgid_autogen BEFORE INSERT OR UPDATE ON student.scr_rqgrp FOR EACH ROW EXECUTE FUNCTION student.fn_scr_rqgrp_rgid_autogen();
CREATE TRIGGER tr_sgl_terms_tmid_autogen BEFORE INSERT OR UPDATE ON student.sgl_terms FOR EACH ROW EXECUTE FUNCTION student.fn_sgl_terms_tmid_autogen();
CREATE TRIGGER tr_sgm_stubi_audit_insert BEFORE INSERT ON student.sgm_stubi FOR EACH ROW EXECUTE FUNCTION student.fn_sgm_stubi_audit_insert();
CREATE TRIGGER tr_sgm_stubi_audit_update BEFORE UPDATE ON student.sgm_stubi FOR EACH ROW EXECUTE FUNCTION student.fn_sgm_stubi_audit_update();
CREATE TRIGGER tr_srb_sects_autogen BEFORE INSERT ON student.srb_sects FOR EACH ROW EXECUTE FUNCTION student.fn_srb_sects_autogen();
CREATE TRIGGER tr_srb_sects_stid_autogen_update BEFORE UPDATE ON student.srb_sects FOR EACH ROW EXECUTE FUNCTION student.fn_srb_sects_stid_autogen_update();
CREATE TRIGGER tr_srh_enrol_audit_insert BEFORE INSERT ON student.srh_enrol FOR EACH ROW EXECUTE FUNCTION student.fn_srh_enrol_audit_insert();
CREATE TRIGGER tr_srh_enrol_audit_update BEFORE UPDATE ON student.srh_enrol FOR EACH ROW EXECUTE FUNCTION student.fn_srh_enrol_audit_update();
CREATE TRIGGER tr_srh_enrol_erid_autogen BEFORE INSERT OR UPDATE ON student.srh_enrol FOR EACH ROW EXECUTE FUNCTION student.fn_srh_enrol_erid_autogen();
CREATE TRIGGER tr_srh_sterm_audit_insert BEFORE INSERT ON student.srh_sterm FOR EACH ROW EXECUTE FUNCTION student.fn_srh_sterm_audit_insert();
CREATE TRIGGER tr_srh_sterm_audit_update BEFORE UPDATE ON student.srh_sterm FOR EACH ROW EXECUTE FUNCTION student.fn_srh_sterm_audit_update();
CREATE TRIGGER tr_srh_sterm_create_sgm_stubi AFTER INSERT ON student.srh_sterm FOR EACH ROW EXECUTE FUNCTION student.fn_srh_sterm_create_sgm_stubi();
CREATE TRIGGER tr_srh_sterm_tsid_autogen BEFORE INSERT OR UPDATE ON student.srh_sterm FOR EACH ROW EXECUTE FUNCTION student.fn_srh_sterm_tsid_autogen();
CREATE TRIGGER tr_srl_cours_crid_autogen BEFORE INSERT OR UPDATE ON student.srl_cours FOR EACH ROW EXECUTE FUNCTION student.fn_srl_cours_crid_autogen();
CREATE TRIGGER tr_sth_crtrn_audit_insert BEFORE INSERT ON student.sth_crtrn FOR EACH ROW EXECUTE FUNCTION student.fn_sth_crtrn_audit_insert();
CREATE TRIGGER tr_sth_crtrn_audit_update BEFORE UPDATE ON student.sth_crtrn FOR EACH ROW EXECUTE FUNCTION student.fn_sth_crtrn_audit_update();
CREATE TRIGGER tr_sth_crtrn_erid_autogen BEFORE INSERT OR UPDATE ON student.sth_crtrn FOR EACH ROW EXECUTE FUNCTION student.fn_sth_crtrn_erid_autogen();

-- ============================================
-- Create Foreign Key constraints
-- ============================================

ALTER TABLE ONLY student.sar_advrl
    ADD CONSTRAINT fk_sar_advrl_advr_rbid FOREIGN KEY (sar_advrl_advr_rbid) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY student.sar_advrl
    ADD CONSTRAINT fk_sar_advrl_avid FOREIGN KEY (sar_advrl_avid) REFERENCES student.sal_avtyp(sal_avtyp_avid);

ALTER TABLE ONLY student.sar_ovrar
    ADD CONSTRAINT fk_sar_ovrar_advr_rbid FOREIGN KEY (sar_ovrar_advr_rbid) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY student.sar_ovrar
    ADD CONSTRAINT fk_sar_ovrar_stdn_rbid FOREIGN KEY (sar_ovrar_stdn_rbid) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY student.scl_currv
    ADD CONSTRAINT fk_scl_currv_ctid FOREIGN KEY (scl_currv_ctid) REFERENCES student.scl_crtyp(scl_crtyp_ctid);

ALTER TABLE ONLY student.scl_currv
    ADD CONSTRAINT fk_scl_currv_mrid FOREIGN KEY (scl_currv_mrid) REFERENCES student.scl_major(scl_major_mrid);

ALTER TABLE ONLY student.scl_degrs
    ADD CONSTRAINT fk_scl_degrs_dlid FOREIGN KEY (scl_degrs_dlid) REFERENCES student.scl_dlevl(scl_dlevl_dlid);

ALTER TABLE ONLY student.scl_dlevl
    ADD CONSTRAINT fk_scl_dlevl_lvid FOREIGN KEY (scl_dlevl_lvid) REFERENCES student.sgl_level(sgl_level_lvid);

ALTER TABLE ONLY student.scl_major
    ADD CONSTRAINT fk_scl_major_cgid FOREIGN KEY (scl_major_cgid) REFERENCES student.sdl_coleg(sdl_coleg_cgid);

ALTER TABLE ONLY student.scl_major
    ADD CONSTRAINT fk_scl_major_ciid FOREIGN KEY (scl_major_ciid) REFERENCES student.scl_cipcd(scl_cipcd_ciid);

ALTER TABLE ONLY student.scl_major
    ADD CONSTRAINT fk_scl_major_dgid FOREIGN KEY (scl_major_dgid) REFERENCES student.scl_degrs(scl_degrs_dgid);

ALTER TABLE ONLY student.scl_major
    ADD CONSTRAINT fk_scl_major_ifid FOREIGN KEY (scl_major_ifid) REFERENCES student.scl_iscdf(scl_iscdf_ifid);

ALTER TABLE ONLY student.scm_stucv
    ADD CONSTRAINT fk_scm_stucv_cpid FOREIGN KEY (scm_stucv_cpid) REFERENCES student.sdl_camps(sdl_camps_cpid);

ALTER TABLE ONLY student.scm_stucv
    ADD CONSTRAINT fk_scm_stucv_cvid FOREIGN KEY (scm_stucv_cvid) REFERENCES student.scl_currv(scl_currv_cvid);

ALTER TABLE ONLY student.scm_stucv
    ADD CONSTRAINT fk_scm_stucv_rbid FOREIGN KEY (scm_stucv_rbid) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY student.scr_creqs
    ADD CONSTRAINT fk_scr_creqs_crid FOREIGN KEY (scr_creqs_crid) REFERENCES student.srl_cours(srl_cours_crid);

ALTER TABLE ONLY student.scr_creqs
    ADD CONSTRAINT fk_scr_creqs_cvid FOREIGN KEY (scr_creqs_cvid) REFERENCES student.scl_currv(scl_currv_cvid);

ALTER TABLE ONLY student.scr_creqs
    ADD CONSTRAINT fk_scr_creqs_min_mkid FOREIGN KEY (scr_creqs_min_mkid) REFERENCES student.stl_marks(stl_marks_mkid);

ALTER TABLE ONLY student.scr_creqs
    ADD CONSTRAINT fk_scr_creqs_rtid FOREIGN KEY (scr_creqs_rtid) REFERENCES student.srl_rqtyp(srl_rqtyp_rtid);

ALTER TABLE ONLY student.scr_ovcls
    ADD CONSTRAINT fk_scr_ovcls_approved_by FOREIGN KEY (scr_ovcls_approved_by) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY student.scr_ovcls
    ADD CONSTRAINT fk_scr_ovcls_crid FOREIGN KEY (scr_ovcls_crid) REFERENCES student.srl_cours(srl_cours_crid);

ALTER TABLE ONLY student.scr_ovcls
    ADD CONSTRAINT fk_scr_ovcls_rqid FOREIGN KEY (scr_ovcls_rqid) REFERENCES student.scr_creqs(scr_creqs_rqid);

ALTER TABLE ONLY student.scr_ovcls
    ADD CONSTRAINT fk_scr_ovcls_scid FOREIGN KEY (scr_ovcls_scid) REFERENCES student.scm_stucv(scm_stucv_scid);

ALTER TABLE ONLY student.sar_ovrar
    ADD CONSTRAINT fk_sar_ovrar_approved_by FOREIGN KEY (sar_ovrar_approved_by) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY student.scr_ovmrk
    ADD CONSTRAINT fk_scr_ovmrk_approved_by FOREIGN KEY (scr_ovmrk_approved_by) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY student.scr_ovmrk
    ADD CONSTRAINT fk_scr_ovmrk_mkid FOREIGN KEY (scr_ovmrk_mkid) REFERENCES student.stl_marks(stl_marks_mkid);

ALTER TABLE ONLY student.scr_ovmrk
    ADD CONSTRAINT fk_scr_ovmrk_rqid FOREIGN KEY (scr_ovmrk_rqid) REFERENCES student.scr_creqs(scr_creqs_rqid);

ALTER TABLE ONLY student.scr_ovmrk
    ADD CONSTRAINT fk_scr_ovmrk_scid FOREIGN KEY (scr_ovmrk_scid) REFERENCES student.scm_stucv(scm_stucv_scid);

ALTER TABLE ONLY student.scr_preqs
    ADD CONSTRAINT fk_scr_preqs_crid FOREIGN KEY (scr_preqs_crid) REFERENCES student.srl_cours(srl_cours_crid);

ALTER TABLE ONLY student.scr_preqs
    ADD CONSTRAINT fk_scr_preqs_req_crid FOREIGN KEY (scr_preqs_req_crid) REFERENCES student.srl_cours(srl_cours_crid);

ALTER TABLE ONLY student.scr_rqgrp
    ADD CONSTRAINT fk_scr_rqgrp_cvid FOREIGN KEY (scr_rqgrp_cvid) REFERENCES student.scl_currv(scl_currv_cvid);

ALTER TABLE ONLY student.scr_rqgrp
    ADD CONSTRAINT fk_scr_rqgrp_rtid FOREIGN KEY (scr_rqgrp_rtid) REFERENCES student.srl_rqtyp(srl_rqtyp_rtid);

ALTER TABLE ONLY student.sdl_depts
    ADD CONSTRAINT fk_sdl_depts_cgid FOREIGN KEY (sdl_depts_cgid) REFERENCES student.sdl_coleg(sdl_coleg_cgid);

ALTER TABLE ONLY student.sgl_stype
    ADD CONSTRAINT fk_sgl_stype_stid FOREIGN KEY (sgl_stype_next_stid) REFERENCES student.sgl_stype(sgl_stype_stid) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY student.sgl_terms
    ADD CONSTRAINT fk_sgl_terms_fyid FOREIGN KEY (sgl_terms_fyid) REFERENCES finance.fgl_fyear(fgl_fyear_fyid);

ALTER TABLE ONLY student.sgl_terms
    ADD CONSTRAINT fk_sgl_terms_smid FOREIGN KEY (sgl_terms_smid) REFERENCES student.sgl_smstr(sgl_smstr_smid);

ALTER TABLE ONLY student.sgm_stubi
    ADD CONSTRAINT fk_sgm_stubi_lvid FOREIGN KEY (sgm_stubi_lvid) REFERENCES student.sgl_level(sgl_level_lvid);

ALTER TABLE ONLY student.sgm_stubi
    ADD CONSTRAINT fk_sgm_stubi_rbid FOREIGN KEY (sgm_stubi_rbid) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY student.sgm_stubi
    ADD CONSTRAINT fk_sgm_stubi_stid FOREIGN KEY (sgm_stubi_stid) REFERENCES student.sgl_stype(sgl_stype_stid);

ALTER TABLE ONLY student.sgm_stubi
    ADD CONSTRAINT fk_sgm_stubi_tmid FOREIGN KEY (sgm_stubi_tmid) REFERENCES student.sgl_terms(sgl_terms_tmid);

ALTER TABLE ONLY student.sgm_stubi
    ADD CONSTRAINT fk_sgm_stubi_tsid FOREIGN KEY (sgm_stubi_tsid) REFERENCES student.srh_sterm(srh_sterm_tsid);

ALTER TABLE ONLY student.srb_sects
    ADD CONSTRAINT fk_srb_sects_crid FOREIGN KEY (srb_sects_crid) REFERENCES student.srl_cours(srl_cours_crid);

ALTER TABLE ONLY student.srb_sects
    ADD CONSTRAINT fk_srb_sects_prim_inst FOREIGN KEY (srb_sects_prim_inst) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY student.srb_sects
    ADD CONSTRAINT fk_srb_sects_scnd_inst FOREIGN KEY (srb_sects_scnd_inst) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY student.srb_sects
    ADD CONSTRAINT fk_srb_sects_tmid FOREIGN KEY (srb_sects_tmid) REFERENCES student.sgl_terms(sgl_terms_tmid);

ALTER TABLE ONLY student.srh_enrol
    ADD CONSTRAINT fk_srh_enrol_esid FOREIGN KEY (srh_enrol_esid) REFERENCES student.srl_enrst(srl_enrst_esid);

ALTER TABLE ONLY student.srh_enrol
    ADD CONSTRAINT fk_srh_enrol_rbid FOREIGN KEY (srh_enrol_rbid) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY student.srh_enrol
    ADD CONSTRAINT fk_srh_enrol_stid FOREIGN KEY (srh_enrol_stid) REFERENCES student.srb_sects(srb_sects_stid);

ALTER TABLE ONLY student.srh_sterm
    ADD CONSTRAINT fk_srh_sterm_rgid FOREIGN KEY (srh_sterm_rgid) REFERENCES student.srl_rgtyp(srl_rgtyp_rgid);

ALTER TABLE ONLY student.srh_sterm
    ADD CONSTRAINT fk_srh_sterm_rnid FOREIGN KEY (srh_sterm_rbid) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY student.srh_sterm
    ADD CONSTRAINT fk_srh_sterm_tmid FOREIGN KEY (srh_sterm_tmid) REFERENCES student.sgl_terms(sgl_terms_tmid);

ALTER TABLE ONLY student.srl_cours
    ADD CONSTRAINT fk_srl_cours_sbid FOREIGN KEY (srl_cours_sbid) REFERENCES student.srl_subjs(srl_subjs_sbid);

ALTER TABLE ONLY student.srl_subjs
    ADD CONSTRAINT fk_srl_subjs_dpid FOREIGN KEY (srl_subjs_dpid) REFERENCES student.sdl_depts(sdl_depts_dpid);

ALTER TABLE ONLY student.sth_crtrn
    ADD CONSTRAINT fk_sth_crtrn_erid FOREIGN KEY (sth_crtrn_erid) REFERENCES student.srh_enrol(srh_enrol_erid);

ALTER TABLE ONLY student.sth_crtrn
    ADD CONSTRAINT fk_sth_crtrn_final_mkid FOREIGN KEY (sth_crtrn_final_mkid) REFERENCES student.stl_marks(stl_marks_mkid);
    
-- ============================================
-- Insert Into Table srl_rqtyp
-- ============================================

INSERT INTO student.srl_rqtyp (srl_rqtyp_rtid, srl_rqtyp_hr_name, srl_rqtyp_group_ind) VALUES ('CORE', 'Core Class', 'N');
INSERT INTO student.srl_rqtyp (srl_rqtyp_rtid, srl_rqtyp_hr_name, srl_rqtyp_group_ind) VALUES ('ELCA', 'Elective Block A', 'Y');
INSERT INTO student.srl_rqtyp (srl_rqtyp_rtid, srl_rqtyp_hr_name, srl_rqtyp_group_ind) VALUES ('ELCB', 'Elective Block B', 'Y');
INSERT INTO student.srl_rqtyp (srl_rqtyp_rtid, srl_rqtyp_hr_name, srl_rqtyp_group_ind) VALUES ('ELCC', 'Elective Block C', 'Y');

-- ============================================
-- Insert Into Table sgl_stype
-- ============================================

INSERT INTO student.sgl_stype (sgl_stype_stid, sgl_stype_hr_name, sgl_stype_next_stid) VALUES ('CN', 'Continuing', 'CN');
INSERT INTO student.sgl_stype (sgl_stype_stid, sgl_stype_hr_name, sgl_stype_next_stid) VALUES ('FT', 'First Time First Year', 'CN');
INSERT INTO student.sgl_stype (sgl_stype_stid, sgl_stype_hr_name, sgl_stype_next_stid) VALUES ('NT', 'New Transfer', 'CN');
INSERT INTO student.sgl_stype (sgl_stype_stid, sgl_stype_hr_name, sgl_stype_next_stid) VALUES ('RE', 'Returning', 'CN');
INSERT INTO student.sgl_stype (sgl_stype_stid, sgl_stype_hr_name, sgl_stype_next_stid) VALUES ('DR', 'Doctoral', 'DR');
INSERT INTO student.sgl_stype (sgl_stype_stid, sgl_stype_hr_name, sgl_stype_next_stid) VALUES ('UN', 'Undeclared', 'UN');

-- ============================================
-- Insert Into Table sal_avtyp
-- ============================================



-- ============================================
-- Insert Into Table sgl_smstr
-- ============================================

INSERT INTO student.sgl_smstr (sgl_smstr_smid, sgl_smstr_hr_name) VALUES ('SMMR', 'Summer');
INSERT INTO student.sgl_smstr (sgl_smstr_smid, sgl_smstr_hr_name) VALUES ('ATMN', 'Autumn');
INSERT INTO student.sgl_smstr (sgl_smstr_smid, sgl_smstr_hr_name) VALUES ('SPNG', 'Spring');

-- ============================================
-- Insert Into Table srl_enrst
-- ============================================

INSERT INTO student.srl_enrst (srl_enrst_esid, srl_enrst_hr_name, srl_enrst_roll_ind, srl_enrst_credit_ind) VALUES ('RE', 'Registered', 'Y', 'Y');
INSERT INTO student.srl_enrst (srl_enrst_esid, srl_enrst_hr_name, srl_enrst_roll_ind, srl_enrst_credit_ind) VALUES ('RW', 'Web Registered', 'Y', 'Y');
INSERT INTO student.srl_enrst (srl_enrst_esid, srl_enrst_hr_name, srl_enrst_roll_ind, srl_enrst_credit_ind) VALUES ('RA', 'Admin Registered', 'Y', 'Y');
INSERT INTO student.srl_enrst (srl_enrst_esid, srl_enrst_hr_name, srl_enrst_roll_ind, srl_enrst_credit_ind) VALUES ('RV', 'Vendor Registered', 'Y', 'Y');
INSERT INTO student.srl_enrst (srl_enrst_esid, srl_enrst_hr_name, srl_enrst_roll_ind, srl_enrst_credit_ind) VALUES ('WI', 'Withdraw', 'N', 'N');
INSERT INTO student.srl_enrst (srl_enrst_esid, srl_enrst_hr_name, srl_enrst_roll_ind, srl_enrst_credit_ind) VALUES ('WW', 'Web Withdraw', 'N', 'N');
INSERT INTO student.srl_enrst (srl_enrst_esid, srl_enrst_hr_name, srl_enrst_roll_ind, srl_enrst_credit_ind) VALUES ('WA', 'Admin Withdraw', 'N', 'N');
INSERT INTO student.srl_enrst (srl_enrst_esid, srl_enrst_hr_name, srl_enrst_roll_ind, srl_enrst_credit_ind) VALUES ('WV', 'Vendor Withdraw', 'N', 'N');
INSERT INTO student.srl_enrst (srl_enrst_esid, srl_enrst_hr_name, srl_enrst_roll_ind, srl_enrst_credit_ind) VALUES ('WC', 'Credited Withdraw', 'N', 'Y');
INSERT INTO student.srl_enrst (srl_enrst_esid, srl_enrst_hr_name, srl_enrst_roll_ind, srl_enrst_credit_ind) VALUES ('TF', 'Transfer Cousrse', 'N', 'Y');
INSERT INTO student.srl_enrst (srl_enrst_esid, srl_enrst_hr_name, srl_enrst_roll_ind, srl_enrst_credit_ind) VALUES ('HN', 'Honorary Course', 'N', 'Y');
INSERT INTO student.srl_enrst (srl_enrst_esid, srl_enrst_hr_name, srl_enrst_roll_ind, srl_enrst_credit_ind) VALUES ('AU', 'Audit', 'Y', 'N');


-- ============================================
-- Insert Into Table srl_rgtyp
-- ============================================

INSERT INTO student.srl_rgtyp (srl_rgtyp_rgid, srl_rgtyp_hr_name, srl_rgtyp_enrol_ind, srl_rgtyp_count_ind, srl_rgtyp_audit_ind) VALUES ('NS', 'Normal Student', 'Y', 'Y', 'N');
INSERT INTO student.srl_rgtyp (srl_rgtyp_rgid, srl_rgtyp_hr_name, srl_rgtyp_enrol_ind, srl_rgtyp_count_ind, srl_rgtyp_audit_ind) VALUES ('AU', 'Auditor', 'Y', 'N', 'Y');
INSERT INTO student.srl_rgtyp (srl_rgtyp_rgid, srl_rgtyp_hr_name, srl_rgtyp_enrol_ind, srl_rgtyp_count_ind, srl_rgtyp_audit_ind) VALUES ('WB', 'Withdrawal Before Census', 'N', 'N', 'N');
INSERT INTO student.srl_rgtyp (srl_rgtyp_rgid, srl_rgtyp_hr_name, srl_rgtyp_enrol_ind, srl_rgtyp_count_ind, srl_rgtyp_audit_ind) VALUES ('AW', 'Admin Withdrawal', 'N', 'Y', 'N');
INSERT INTO student.srl_rgtyp (srl_rgtyp_rgid, srl_rgtyp_hr_name, srl_rgtyp_enrol_ind, srl_rgtyp_count_ind, srl_rgtyp_audit_ind) VALUES ('WA', 'Withdrawal After Census', 'N', 'Y', 'N');

COMMIT;