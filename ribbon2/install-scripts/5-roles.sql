-- ============================================
-- Ribbon2 SIS Users and Roles
-- Release 1.0 - Initial Schema
-- Date: 2026-04-20
-- PostgreSQL 16+
-- Apply: psql -U ribbon2 -d ribbon2 -f 5-roles.sql
-- ============================================

CREATE ROLE sis_readonly;
GRANT USAGE ON SCHEMA general TO sis_readonly;
GRANT USAGE ON SCHEMA finance TO sis_readonly;
GRANT USAGE ON SCHEMA student TO sis_readonly;
ALTER DEFAULT PRIVILEGES FOR ROLE ribbon2 IN SCHEMA general
    GRANT SELECT ON TABLES TO sis_readonly;
ALTER DEFAULT PRIVILEGES FOR ROLE ribbon2 IN SCHEMA finance
    GRANT SELECT ON TABLES TO sis_readonly;
ALTER DEFAULT PRIVILEGES FOR ROLE ribbon2 IN SCHEMA student
    GRANT SELECT ON TABLES TO sis_readonly;

-- ============================================
-- Create Role sis_registrar
-- ============================================

CREATE ROLE sis_registrar;
GRANT USAGE ON SCHEMA general TO sis_registrar;
GRANT USAGE ON SCHEMA finance TO sis_registrar;
GRANT USAGE ON SCHEMA student TO sis_registrar;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA general TO sis_registrar;
GRANT SELECT, INSERT, UPDATE ON TABLE finance.fgl_fyear TO sis_registrar;
GRANT SELECT ON student.sdl_camps, student.sdl_coleg, student.sdl_depts, 
                student.sgl_smstr, student.sgl_terms, student.sgl_level,
                student.sgl_stype, student.srl_cours, student.srl_subjs, 
                student.srl_enrst, student.srl_rgtyp, student.srl_rqtyp,
                student.scl_cipcd, student.scl_iscdf, student.scl_crtyp, 
                student.scl_degrs, student.scl_dlevl, student.stl_marks,
                student.sal_avtyp, student.sth_crtrn, student.scl_major, 
                student.scl_currv, student.scr_creqs, student.scr_rqgrp, 
                student.scr_preqs, student.srh_sterm, student.scm_stucv, 
                student.srb_sects, student.sgm_stubi, student.srh_enrol,
                sar_advrl, sar_ovrar, scr_ovcls, scr_ovmrk TO sis_registrar;             
GRANT INSERT, UPDATE ON student.scl_major, student.scl_currv, student.scr_creqs, 
                        student.scr_rqgrp, student.scr_preqs, student.srh_sterm, 
                        student.scm_stucv, student.srb_sects, student.sgm_stubi, 
                        student.srh_enrol, student.sar_advrl TO sis_registrar;
GRANT INSERT ON student.sar_ovrar, student.scr_ovcls, student.scr_ovmrk 
                TO sis_registrar;
                
-- ============================================
-- Create Role sis_advisor
-- ============================================

CREATE ROLE sis_advisor;
GRANT USAGE ON SCHEMA general TO sis_advisor;
GRANT USAGE ON SCHEMA finance TO sis_advisor;
GRANT USAGE ON SCHEMA student TO sis_advisor;
GRANT SELECT (gum_ident_rbid, gum_ident_first_name, gum_ident_last_name, gum_ident_birthday) ON general.gum_ident TO sis_advisor;
GRANT SELECT (gum_adinf_rbid, gum_adinf_pref_first_name, gum_adinf_prefix, gum_adinf_suffix, gum_adinf_username, gum_adinf_czid, gum_adinf_citizen_coid) ON general.gum_ident TO sis_advisor;
GRANT SELECT ON TABLE ggl_count TO sis_advisor;
GRANT SELECT ON TABLE ggl_citzn TO sis_advisor;
GRANT SELECT ON TABLE finance.fgl_fyear TO sis_advisor;
GRANT SELECT ON student.sdl_camps, student.sdl_coleg, student.sdl_depts, 
                student.sgl_smstr, student.sgl_terms, student.sgl_level,
                student.sgl_stype, student.srl_cours, student.srl_subjs, 
                student.srl_enrst, student.srl_rgtyp, student.srl_rqtyp,
                student.scl_cipcd, student.scl_iscdf, student.scl_crtyp,
                student.scl_degrs, student.scl_dlevl, student.stl_marks,
                student.sal_avtyp, student.srh_sterm, student.sgm_stubi, 
                student.scr_preqs, student.srb_sects, student.srh_enrol,
                student.sth_crtrn, student.scl_major, student.scl_currv, 
                student.scr_creqs, student.scr_rqgrp, student.scm_stucv,
                student.sar_advrl, student.sar_ovrar, student.scr_ovcls, 
                student.scr_ovmrk TO sis_advisor;
GRANT INSERT, UPDATE ON student.scm_stucv, student.sar_advrl TO sis_advisor;
GRANT INSERT ON student.sar_ovrar, student.scr_ovcls, student.scr_ovmrk 
                TO sis_advisor;

-- ============================================
-- Create Role sis_instructor
-- ============================================

CREATE ROLE sis_instructor;
GRANT USAGE ON SCHEMA general TO sis_instructor;
GRANT USAGE ON SCHEMA finance TO sis_instructor;
GRANT USAGE ON SCHEMA student TO sis_instructor;
GRANT SELECT (gum_ident_rbid, gum_ident_first_name, gum_ident_last_name, gum_ident_birthday) ON general.gum_ident TO sis_advisor;
GRANT SELECT (gum_adinf_rbid, gum_adinf_pref_first_name, gum_adinf_prefix, gum_adinf_suffix, gum_adinf_username, gum_adinf_czid, gum_adinf_citizen_coid) ON general.gum_ident TO sis_advisor;
GRANT SELECT ON TABLE ggl_count TO sis_advisor;
GRANT SELECT ON TABLE ggl_citzn TO sis_advisor;
GRANT SELECT ON TABLE finance.fgl_fyear TO sis_instructor;
GRANT SELECT ON student.sdl_camps, student.sdl_coleg, student.sdl_depts, 
                student.sgl_smstr, student.sgl_terms, student.sgl_level,
                student.sgl_stype, student.srl_cours, student.srl_subjs, 
                student.srl_enrst, student.srl_rgtyp, student.srl_rqtyp,
                student.scl_cipcd, student.scl_iscdf, student.scl_crtyp, 
                student.scl_degrs, student.scl_dlevl, student.stl_marks,
                student.sal_avtyp, student.srh_sterm, student.sgm_stubi, 
                student.scm_stucv, student.srb_sects, student.srh_enrol,
                student.scl_major, student.scl_currv, student.scr_creqs, 
                student.scr_rqgrp, student.scr_preqs, student.sth_crtrn 
                TO sis_instructor;              
GRANT INSERT, UPDATE ON student.sth_crtrn TO sis_advisor;

-- ============================================
-- Create Role sis_admin
-- ============================================

CREATE ROLE sis_admin;
GRANT USAGE ON SCHEMA general TO sis_admin;
GRANT USAGE ON SCHEMA finance TO sis_admin;
GRANT USAGE ON SCHEMA student TO sis_admin;
ALTER DEFAULT PRIVILEGES FOR ROLE ribbon2 IN SCHEMA general
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO sis_admin;
ALTER DEFAULT PRIVILEGES FOR ROLE ribbon2 IN SCHEMA finance
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO sis_admin;
ALTER DEFAULT PRIVILEGES FOR ROLE ribbon2 IN SCHEMA student
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO sis_admin;

-- ============================================
-- Create Role sis_application
-- Apply to petruskan Account only
-- ============================================

CREATE ROLE sis_application;
GRANT USAGE ON SCHEMA general TO sis_application;
GRANT USAGE ON SCHEMA finance TO sis_application;
GRANT USAGE ON SCHEMA student TO sis_application;
ALTER DEFAULT PRIVILEGES FOR ROLE ribbon2 IN SCHEMA general
    GRANT ALL PRIVILEGES ON TABLES TO sis_application;
ALTER DEFAULT PRIVILEGES FOR ROLE ribbon2 IN SCHEMA finance
    GRANT ALL PRIVILEGES ON TABLES TO sis_application;
ALTER DEFAULT PRIVILEGES FOR ROLE ribbon2 IN SCHEMA student
    GRANT ALL PRIVILEGES ON TABLES TO sis_application;
    
CREATE USER petruskan WITH PASSWORD 'Ch4ng3_m3_pl34s3';
GRANT sis_application to petruskan;
