-- ============================================
-- Ribbon2 General Schema for Ribbon2 SIS Users and Roles
-- Release 1.0 - Initial Schema
-- Date: 2026-04-20
-- PostgreSQL 16+
-- Apply: psql -U ribbon2 -d ribbon2 -f 4-ireland_inserts.sql
-- ============================================

BEGIN;

-- ============================================
-- Insert Into Table grl_rcens
-- ============================================

INSERT INTO general.grl_rcens (grl_rcens_rcid, grl_rcens_hr_name, grl_rcens_govt_1, grl_rcens_govt_2, grl_rcens_govt_3) VALUES ('WIRS', 'White Irish', 'WHITE', NULL, NULL);
INSERT INTO general.grl_rcens (grl_rcens_rcid, grl_rcens_hr_name, grl_rcens_govt_1, grl_rcens_govt_2, grl_rcens_govt_3) VALUES ('WTRV', 'Irish Traveller', 'WHITE', NULL, NULL);
INSERT INTO general.grl_rcens (grl_rcens_rcid, grl_rcens_hr_name, grl_rcens_govt_1, grl_rcens_govt_2, grl_rcens_govt_3) VALUES ('WRMA', 'White Roma', 'WHITE', NULL, NULL);
INSERT INTO general.grl_rcens (grl_rcens_rcid, grl_rcens_hr_name, grl_rcens_govt_1, grl_rcens_govt_2, grl_rcens_govt_3) VALUES ('WOTH', 'Other White', 'WHITE', NULL, NULL);
INSERT INTO general.grl_rcens (grl_rcens_rcid, grl_rcens_hr_name, grl_rcens_govt_1, grl_rcens_govt_2, grl_rcens_govt_3) VALUES ('ACHN', 'Chinese', 'ASIAN', NULL, NULL);
INSERT INTO general.grl_rcens (grl_rcens_rcid, grl_rcens_hr_name, grl_rcens_govt_1, grl_rcens_govt_2, grl_rcens_govt_3) VALUES ('AIPB', 'Indian/Pakistani/Bangladeshi', 'ASIAN', NULL, NULL);
INSERT INTO general.grl_rcens (grl_rcens_rcid, grl_rcens_hr_name, grl_rcens_govt_1, grl_rcens_govt_2, grl_rcens_govt_3) VALUES ('AARB', 'Arab', 'ASIAN', NULL, NULL);
INSERT INTO general.grl_rcens (grl_rcens_rcid, grl_rcens_hr_name, grl_rcens_govt_1, grl_rcens_govt_2, grl_rcens_govt_3) VALUES ('AOTH', 'Other Asian', 'ASIAN', NULL, NULL);
INSERT INTO general.grl_rcens (grl_rcens_rcid, grl_rcens_hr_name, grl_rcens_govt_1, grl_rcens_govt_2, grl_rcens_govt_3) VALUES ('BIAF', 'Black Irish or African', 'BLACK', NULL, NULL);
INSERT INTO general.grl_rcens (grl_rcens_rcid, grl_rcens_hr_name, grl_rcens_govt_1, grl_rcens_govt_2, grl_rcens_govt_3) VALUES ('BOTH', 'Other Black', 'BLACK', NULL, NULL);
INSERT INTO general.grl_rcens (grl_rcens_rcid, grl_rcens_hr_name, grl_rcens_govt_1, grl_rcens_govt_2, grl_rcens_govt_3) VALUES ('OOIM', 'Other Including Mixed', 'OTHER', NULL, NULL);
INSERT INTO general.grl_rcens (grl_rcens_rcid, grl_rcens_hr_name, grl_rcens_govt_1, grl_rcens_govt_2, grl_rcens_govt_3) VALUES ('ONST', 'Not Stated', 'OTHER', NULL, NULL);

-- ============================================
-- Insert Into Table grl_rcens
-- ============================================

INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('IRIS', 'Irish', 'WIRS');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('TRAV', 'Irish Traveller', 'WTRV');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('WRMA', 'White Roma', 'WRMA');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('SLAV', 'Slavic', 'WOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('GERM', 'German', 'WOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('BRIT', 'British', 'WOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('FRNC', 'French', 'WOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('SPLA', 'Spanish/Latino', 'WOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('ITAL', 'Italian', 'WOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('HFES', 'Hungarian/Finish/Estonian', 'WOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('OEUR', 'Other Europe', 'WOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('AMRC', 'White American', 'WOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('AUST', 'White Australian', 'WOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('WOTH', 'Other White', 'WOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('CHAN', 'Han Chinese', 'ACHN');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('CHUI', 'Hui Chinese', 'ACHN');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('TBTN', 'Tibetan', 'ACHN');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('BRMS', 'Burmese', 'ACHN');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('INDN', 'Indian', 'AIPB');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('PKST', 'Pakistani', 'AIPB');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('BNGL', 'Bangladeshi', 'AIPB');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('ROMA', 'Indic Roma', 'AIPB');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('AGLF', 'Gulf Arab', 'AARB');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('ANIL', 'Nile Basin Arab', 'AARB');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('ALEV', 'Levantine Arab', 'AARB');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('AMAG', 'Maghrebi Arab', 'AARB');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('AYEM', 'Yemeni Arab', 'AARB');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('AIRQ', 'Iraqi Arab', 'AARB');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('AOTH', 'Other Arab', 'AARB');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('VIET', 'Vietnamese', 'AOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('THAI', 'Thai', 'AOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('MLYS', 'Malaysian', 'AOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('INDS', 'Indonesian', 'AOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('PHLP', 'Filipino', 'AOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('OSEA', 'Other South East Asian', 'AOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('JAPN', 'Japanese', 'AOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('PACF', 'Pacific Islander', 'AOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('KORN', 'Korean', 'AOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('MNGL', 'Mongolian', 'AOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('BIRS', 'Black Irish', 'BIAF');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('SUBS', 'Sub Saharan African', 'BIAF');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('OBAF', 'Other Black African', 'BIAF');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('ACRB', 'Afro-Caribbean', 'BIAF');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('AUSA', 'Australian Aboriginal', 'BOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('BOTH', 'Other Black', 'BOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('USCN', 'Native American or Aboriginal Canadian', 'OOIM');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('SCAN', 'Native South or Central American', 'OOIM');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('CARB', 'Caribbean', 'OOIM');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('NOST', 'Not Stated', 'ONST');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('OASN', 'Other Asian', 'AOTH');
INSERT INTO general.grl_rdetl (grl_rdetl_rdid, grl_rdetl_hr_name, grl_rdetl_rcid) VALUES ('AOSI', 'Aos Sí', 'WIRS');

-- ============================================
-- Insert Into Table ggl_citzn
-- ============================================

INSERT INTO general.ggl_citzn (ggl_citzn_czid, ggl_citzn_hr_name, ggl_citzn_study_visa_ind, ggl_citzn_employ_visa_ind) VALUES ('CZNA', 'Native Citizen', 'N', 'N');
INSERT INTO general.ggl_citzn (ggl_citzn_czid, ggl_citzn_hr_name, ggl_citzn_study_visa_ind, ggl_citzn_employ_visa_ind) VALUES ('CZNR', 'Naturalised Citizen', 'N', 'N');
INSERT INTO general.ggl_citzn (ggl_citzn_czid, ggl_citzn_hr_name, ggl_citzn_study_visa_ind, ggl_citzn_employ_visa_ind) VALUES ('UKCZ', 'UK Citizen', 'N', 'N');
INSERT INTO general.ggl_citzn (ggl_citzn_czid, ggl_citzn_hr_name, ggl_citzn_study_visa_ind, ggl_citzn_employ_visa_ind) VALUES ('EUEA', 'European Economic Area NON-EU', 'N', 'N');
INSERT INTO general.ggl_citzn (ggl_citzn_czid, ggl_citzn_hr_name, ggl_citzn_study_visa_ind, ggl_citzn_employ_visa_ind) VALUES ('EUNI', 'European Union', 'N', 'N');
INSERT INTO general.ggl_citzn (ggl_citzn_czid, ggl_citzn_hr_name, ggl_citzn_study_visa_ind, ggl_citzn_employ_visa_ind) VALUES ('SCHN', 'Schengen NON-EU', 'N', 'N');
INSERT INTO general.ggl_citzn (ggl_citzn_czid, ggl_citzn_hr_name, ggl_citzn_study_visa_ind, ggl_citzn_employ_visa_ind) VALUES ('NCTZ', 'Non Citizen NON-EU-EEA-SCHENGEN-UK', 'Y', 'Y');
INSERT INTO general.ggl_citzn (ggl_citzn_czid, ggl_citzn_hr_name, ggl_citzn_study_visa_ind, ggl_citzn_employ_visa_ind) VALUES ('LTRS', 'Long Term Resident', 'Y', 'Y');

-- ============================================
-- Insert Into Table scl_crtyp
-- ============================================

INSERT INTO student.scl_crtyp (scl_crtyp_ctid, scl_crtyp_hr_name, scl_crtyp_major_ind) VALUES ('MAJR', 'Major', 'Y');
INSERT INTO student.scl_crtyp (scl_crtyp_ctid, scl_crtyp_hr_name, scl_crtyp_major_ind) VALUES ('MINR', 'Minor', 'N');
INSERT INTO student.scl_crtyp (scl_crtyp_ctid, scl_crtyp_hr_name, scl_crtyp_major_ind) VALUES ('HCRT', 'Higher Certificate', 'N');

-- ============================================
-- Insert Into Table sgl_level
-- ============================================

INSERT INTO student.sgl_level (sgl_level_lvid, sgl_level_hr_name, sgl_level_degree_ind) VALUES ('L7', 'Ordinary Bachelor Degree', 'Y');
INSERT INTO student.sgl_level (sgl_level_lvid, sgl_level_hr_name, sgl_level_degree_ind) VALUES ('L8', 'Honours Bachelor Degree', 'Y');
INSERT INTO student.sgl_level (sgl_level_lvid, sgl_level_hr_name, sgl_level_degree_ind) VALUES ('L9', 'Master’s Degree', 'Y');
INSERT INTO student.sgl_level (sgl_level_lvid, sgl_level_hr_name, sgl_level_degree_ind) VALUES ('10', 'Doctoral Degree', 'Y');
INSERT INTO student.sgl_level (sgl_level_lvid, sgl_level_hr_name, sgl_level_degree_ind) VALUES ('L6', 'Higher Certificate', 'Y');
INSERT INTO student.sgl_level (sgl_level_lvid, sgl_level_hr_name, sgl_level_degree_ind) VALUES ('UN', 'Undeclared', 'N');


-- ============================================
-- Insert Into Table scl_dlevl
-- ============================================

INSERT INTO student.scl_dlevl (scl_dlevl_dlid, scl_dlevl_hr_name, scl_dlevl_nslds_equiv, scl_dlevl_eqf_equiv, scl_dlevl_lvid) VALUES ('6', 'Higher Certificate', NULL, '5', 'L6');
INSERT INTO student.scl_dlevl (scl_dlevl_dlid, scl_dlevl_hr_name, scl_dlevl_nslds_equiv, scl_dlevl_eqf_equiv, scl_dlevl_lvid) VALUES ('7', 'Ordinary Bachelor', '05', '6', 'L7');
INSERT INTO student.scl_dlevl (scl_dlevl_dlid, scl_dlevl_hr_name, scl_dlevl_nslds_equiv, scl_dlevl_eqf_equiv, scl_dlevl_lvid) VALUES ('8', 'Honours Bachelor', '05', '6', 'L8');
INSERT INTO student.scl_dlevl (scl_dlevl_dlid, scl_dlevl_hr_name, scl_dlevl_nslds_equiv, scl_dlevl_eqf_equiv, scl_dlevl_lvid) VALUES ('9', 'Master''s Degree', '07', '7', 'L9');
INSERT INTO student.scl_dlevl (scl_dlevl_dlid, scl_dlevl_hr_name, scl_dlevl_nslds_equiv, scl_dlevl_eqf_equiv, scl_dlevl_lvid) VALUES ('10R', 'Doctoral Degree - Research', '17', '8', '10');
INSERT INTO student.scl_dlevl (scl_dlevl_dlid, scl_dlevl_hr_name, scl_dlevl_nslds_equiv, scl_dlevl_eqf_equiv, scl_dlevl_lvid) VALUES ('10P', 'Doctoral Degree - Professional', '18', '8', '10');

-- ============================================
-- Insert Into Table scl_degrs
-- ============================================

INSERT INTO student.scl_degrs (scl_degrs_dgid, scl_degrs_hr_name, scl_degrs_dlid, scl_degrs_finaid_ind) VALUES ('OBA', 'Ordinary Bachelor of Art', '7', 'Y');
INSERT INTO student.scl_degrs (scl_degrs_dgid, scl_degrs_hr_name, scl_degrs_dlid, scl_degrs_finaid_ind) VALUES ('HBA', 'Honours Bachelor of Art', '8', 'Y');
INSERT INTO student.scl_degrs (scl_degrs_dgid, scl_degrs_hr_name, scl_degrs_dlid, scl_degrs_finaid_ind) VALUES ('OBSC', 'Ordinary Bachelor of Science', '7', 'Y');
INSERT INTO student.scl_degrs (scl_degrs_dgid, scl_degrs_hr_name, scl_degrs_dlid, scl_degrs_finaid_ind) VALUES ('HBSC', 'Honours Bachelor of Science', '8', 'Y');
INSERT INTO student.scl_degrs (scl_degrs_dgid, scl_degrs_hr_name, scl_degrs_dlid, scl_degrs_finaid_ind) VALUES ('OBMUS', 'Ordinary Bachelor of Music', '7', 'Y');
INSERT INTO student.scl_degrs (scl_degrs_dgid, scl_degrs_hr_name, scl_degrs_dlid, scl_degrs_finaid_ind) VALUES ('HBMUS', 'Honours Bachelor of Music', '8', 'Y');
INSERT INTO student.scl_degrs (scl_degrs_dgid, scl_degrs_hr_name, scl_degrs_dlid, scl_degrs_finaid_ind) VALUES ('MA', 'Master of Art', '9', 'Y');
INSERT INTO student.scl_degrs (scl_degrs_dgid, scl_degrs_hr_name, scl_degrs_dlid, scl_degrs_finaid_ind) VALUES ('MSC', 'Master of Science', '9', 'Y');
INSERT INTO student.scl_degrs (scl_degrs_dgid, scl_degrs_hr_name, scl_degrs_dlid, scl_degrs_finaid_ind) VALUES ('MMUS', 'Master of Music', '9', 'Y');
INSERT INTO student.scl_degrs (scl_degrs_dgid, scl_degrs_hr_name, scl_degrs_dlid, scl_degrs_finaid_ind) VALUES ('PHD', 'Doctor of Philosophy', '10R', 'Y');

-- ============================================
-- Insert Into Table scl_iscdf
-- ============================================

INSERT INTO student.scl_iscdf (scl_iscdf_ifid, scl_iscdf_hr_name) VALUES ('0231', 'Language acquisition');
INSERT INTO student.scl_iscdf (scl_iscdf_ifid, scl_iscdf_hr_name) VALUES ('0232', 'Literature and linguistics');
INSERT INTO student.scl_iscdf (scl_iscdf_ifid, scl_iscdf_hr_name) VALUES ('0511', 'Biology');
INSERT INTO student.scl_iscdf (scl_iscdf_ifid, scl_iscdf_hr_name) VALUES ('0521', 'Environmental sciences');
INSERT INTO student.scl_iscdf (scl_iscdf_ifid, scl_iscdf_hr_name) VALUES ('0613', 'Software and app dev and analysis');

COMMIT;