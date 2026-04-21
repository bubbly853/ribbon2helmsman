-- ============================================
-- Ribbon2 General Schema for Ribbon2 SIS General
-- Release 1.0 - Initial Schema
-- Date: 2026-04-20
-- PostgreSQL 16+
-- Apply: psql -U ribbon2 -d ribbon2 -f 1-general.sql
-- ============================================

BEGIN;

-- ============================================
-- Create Schema General
-- ============================================

CREATE SCHEMA general;

-- ============================================
-- Create Trigger Functions
-- ============================================

CREATE FUNCTION general.fn_gum_adinf_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.gum_adinf_created_date := CURRENT_DATE;
    NEW.gum_adinf_activity_date := CURRENT_DATE;
    NEW.gum_adinf_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION general.fn_gum_adinf_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.gum_adinf_activity_date := CURRENT_DATE;
    NEW.gum_adinf_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION general.fn_gum_ident_audit_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.gum_ident_created_date := CURRENT_DATE;
    NEW.gum_ident_activity_date := CURRENT_DATE;
    NEW.gum_ident_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION general.fn_gum_ident_audit_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.gum_ident_activity_date := CURRENT_DATE;
    NEW.gum_ident_modified_by := CURRENT_USER;
    RETURN NEW;
END;
$$;

CREATE FUNCTION general.fn_gum_ident_generate_rbid() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    max_num INTEGER;
BEGIN
    IF NEW.gum_ident_rbid IS NOT NULL AND NEW.gum_ident_rbid <> '' THEN
        RETURN NEW;
    END IF;
        SELECT COALESCE(MAX(SUBSTRING(gum_ident_rbid FROM 2)::INTEGER), 0) + 1
        INTO max_num
        FROM general.gum_ident;
        NEW.gum_ident_rbid := 'U' || LPAD(max_num::TEXT, 8, '0');
    RETURN NEW;
END;
$$;

CREATE FUNCTION general.fn_gum_ident_generate_username() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    base_username text;
    candidate text;
    i int := 0;
BEGIN
    IF NEW.gum_adinf_username IS NOT NULL THEN
        RETURN NEW;
    END IF;
    SELECT lower(unaccent(substring(gum_ident_last_name FROM 1 FOR 12) ||
                 substring(gum_ident_first_name FROM 1 FOR 1)))
    INTO base_username
    FROM general.gum_ident
    WHERE gum_ident_rbid = NEW.gum_adinf_rbid;
    base_username := regexp_replace(base_username, '[^a-z0-9]', '.', 'g');

    LOOP
        IF i = 0 THEN
            candidate := base_username;
        ELSE
            candidate := left(base_username || i::text, 16);
        END IF;

        BEGIN
            NEW.gum_adinf_username := candidate;
            RETURN NEW;
        EXCEPTION
            WHEN unique_violation THEN
                i := i + 1;
                IF i > 999 THEN
                    RAISE EXCEPTION 'Could not generate unique username for RBID %: reached 999 suffixes for base "%". Manual intervention required.', NEW.gum_adinf_rbid, base_username;
                END IF;
                CONTINUE; 
        END;
    END LOOP;
END;
$$;

-- ============================================
-- Create Table ggl_citzn
-- ============================================

CREATE TABLE general.ggl_citzn (
    ggl_citzn_czid character varying(4) NOT NULL,
    ggl_citzn_hr_name character varying(64) NOT NULL,
    ggl_citzn_study_visa_ind character(1),
    ggl_citzn_employ_visa_ind character(1),
    CONSTRAINT ck_ggl_citzn_employ_visa_ind CHECK ((ggl_citzn_employ_visa_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))),
    CONSTRAINT ck_ggl_citzn_study_visa_ind CHECK ((ggl_citzn_study_visa_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);

COMMENT ON TABLE general.ggl_citzn IS 'Citizenship lookup table.';
COMMENT ON COLUMN general.ggl_citzn.ggl_citzn_czid IS 'Citizenship ID';
COMMENT ON COLUMN general.ggl_citzn.ggl_citzn_hr_name IS 'Citizenship human readable name';
COMMENT ON COLUMN general.ggl_citzn.ggl_citzn_study_visa_ind IS 'Indicates if this citizenship status reqires study/student visa';
COMMENT ON COLUMN general.ggl_citzn.ggl_citzn_employ_visa_ind IS 'Indicates if this citizenship status reqires employment visa';

-- ============================================
-- Create Table ggl_count
-- ============================================

CREATE TABLE general.ggl_count (
    ggl_count_coid character(2) NOT NULL,
    ggl_count_hr_name character varying(64) NOT NULL
);

COMMENT ON TABLE general.ggl_count IS 'Country definition table.';
COMMENT ON COLUMN general.ggl_count.ggl_count_coid IS 'Country ID, Alpha-2 code.';
COMMENT ON COLUMN general.ggl_count.ggl_count_hr_name IS 'Country human-readable name.';

-- ============================================
-- Create Table grl_rcens
-- ============================================

CREATE TABLE general.grl_rcens (
    grl_rcens_rcid character varying(4) NOT NULL,
    grl_rcens_hr_name character varying(64) NOT NULL,
    grl_rcens_govt_1 character varying(23),
    grl_rcens_govt_2 character varying(23),
    grl_rcens_govt_3 character varying(23)
);

COMMENT ON TABLE general.grl_rcens IS 'Census/Goverment Race lookup table';
COMMENT ON COLUMN general.grl_rcens.grl_rcens_rcid IS 'Census Race ID';
COMMENT ON COLUMN general.grl_rcens.grl_rcens_hr_name IS 'Census Race human readable name';
COMMENT ON COLUMN general.grl_rcens.grl_rcens_govt_1 IS 'Census Race additional government/reporting field 1.';
COMMENT ON COLUMN general.grl_rcens.grl_rcens_govt_2 IS 'Census Race additional government/reporting field 2.';
COMMENT ON COLUMN general.grl_rcens.grl_rcens_govt_3 IS 'Census Race additional government/reporting field 3.';

-- ============================================
-- Create Table grl_rdetl
-- ============================================

CREATE TABLE general.grl_rdetl (
    grl_rdetl_rdid character varying(4) NOT NULL,
    grl_rdetl_hr_name character varying(64) NOT NULL,
    grl_rdetl_rcid character varying(4)
);

COMMENT ON TABLE general.grl_rdetl IS 'Race Detail lookup table';
COMMENT ON COLUMN general.grl_rdetl.grl_rdetl_rdid IS 'Race Detail ID';
COMMENT ON COLUMN general.grl_rdetl.grl_rdetl_hr_name IS 'Race Detail human readable name';
COMMENT ON COLUMN general.grl_rdetl.grl_rdetl_rcid IS 'Census Race ID associated with Race Detail Code';

-- ============================================
-- Create Table gum_adinf
-- ============================================

CREATE TABLE general.gum_adinf (
    gum_adinf_rbid character(9) NOT NULL,
    gum_adinf_pref_first_name character varying(32),
    gum_adinf_prefix character varying(16),
    gum_adinf_suffix character varying(16),
    gum_adinf_username character varying(16),
    gum_adinf_rcid character varying(4),
    gum_adinf_hispanic_ind character(1),
    gum_adinf_rdid_1 character varying(4),
    gum_adinf_rdid_2 character varying(4),
    gum_adinf_rdid_3 character varying(4),
    gum_adinf_czid character varying(4),
    gum_adinf_citizen_coid character varying(2),
    gum_adinf_created_date date NOT NULL,
    gum_adinf_activity_date date,
    gum_adinf_modified_by character varying(40),
    CONSTRAINT ck_gum_adinf_hispanic_ind CHECK ((gum_adinf_hispanic_ind = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);

COMMENT ON TABLE general.gum_adinf IS 'Additional user information table - extended demographics and preferences.';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_rbid IS 'Ribbon ID (foreign key to gum_ident).';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_pref_first_name IS 'Preferred first name (may differ from legal name).';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_prefix IS 'Name prefix (e.g., Mr., Mrs., Dr.).';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_suffix IS 'Name suffix (e.g., Jr., Sr., III).';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_username IS 'System username for authentication.';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_rcid IS 'Census race ID (for government reporting).';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_hispanic_ind IS 'Hispanic/Latino ethnicity indicator (Y/N).';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_rdid_1 IS 'Primary race detail ID.';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_rdid_2 IS 'Secondary race detail ID (for multi-racial individuals).';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_rdid_3 IS 'Tertiary race detail ID (for multi-racial individuals).';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_czid IS 'Citizenship status ID.';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_citizen_coid IS 'Country of citizenship (foreign key to ggl_count).';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_created_date IS 'Date record was created.';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_activity_date IS 'Date record was last modified.';
COMMENT ON COLUMN general.gum_adinf.gum_adinf_modified_by IS 'User who last modified record.';

-- ============================================
-- Create Table gum_ident
-- ============================================

CREATE TABLE general.gum_ident (
    gum_ident_rbid character(9) NOT NULL,
    gum_ident_first_name character varying(32) NOT NULL,
    gum_ident_last_name character varying(32) NOT NULL,
    gum_ident_middle_name character varying(32),
    gum_ident_birthday date,
    gum_ident_idnum character varying(32),
    gum_ident_id_coid character(2),
    gum_ident_created_date date NOT NULL,
    gum_ident_activity_date date,
    gum_ident_modified_by character varying(40)
);
COMMENT ON TABLE general.gum_ident IS 'Person identity base record table.';
COMMENT ON COLUMN general.gum_ident.gum_ident_rbid IS 'Ribbon ID.';
COMMENT ON COLUMN general.gum_ident.gum_ident_first_name IS 'User first name.';
COMMENT ON COLUMN general.gum_ident.gum_ident_last_name IS 'User last name.';
COMMENT ON COLUMN general.gum_ident.gum_ident_middle_name IS 'User middle name.';
COMMENT ON COLUMN general.gum_ident.gum_ident_birthday IS 'User birth date.';
COMMENT ON COLUMN general.gum_ident.gum_ident_idnum IS 'User national identification number.';
COMMENT ON COLUMN general.gum_ident.gum_ident_id_coid IS 'User national ID country of origin.';
COMMENT ON COLUMN general.gum_ident.gum_ident_created_date IS 'Date record was created.';
COMMENT ON COLUMN general.gum_ident.gum_ident_activity_date IS 'Date record was last modified.';
COMMENT ON COLUMN general.gum_ident.gum_ident_modified_by IS 'User who last modified record.';

-- ============================================
-- Create PK and Unique Constraints
-- ============================================

ALTER TABLE ONLY general.ggl_citzn
    ADD CONSTRAINT pk_ggl_citzn PRIMARY KEY (ggl_citzn_czid);

ALTER TABLE ONLY general.ggl_count
    ADD CONSTRAINT pk_ggl_count PRIMARY KEY (ggl_count_coid);

ALTER TABLE ONLY general.grl_rcens
    ADD CONSTRAINT pk_grl_rcens PRIMARY KEY (grl_rcens_rcid);

ALTER TABLE ONLY general.grl_rdetl
    ADD CONSTRAINT pk_grl_rdetl PRIMARY KEY (grl_rdetl_rdid);

ALTER TABLE ONLY general.gum_adinf
    ADD CONSTRAINT pk_gum_adinf PRIMARY KEY (gum_adinf_rbid);

ALTER TABLE ONLY general.gum_ident
    ADD CONSTRAINT pk_gum_ident PRIMARY KEY (gum_ident_rbid);

ALTER TABLE ONLY general.gum_adinf
    ADD CONSTRAINT uk_gum_adinf_username UNIQUE (gum_adinf_username);
    
-- ============================================
-- Create Triggers
-- ============================================

CREATE TRIGGER tr_gum_adinf_audit_insert BEFORE INSERT ON general.gum_adinf FOR EACH ROW EXECUTE FUNCTION general.fn_gum_adinf_audit_insert();
CREATE TRIGGER tr_gum_adinf_audit_update BEFORE UPDATE ON general.gum_adinf FOR EACH ROW EXECUTE FUNCTION general.fn_gum_adinf_audit_update();
CREATE TRIGGER tr_gum_ident_audit_insert BEFORE INSERT ON general.gum_ident FOR EACH ROW EXECUTE FUNCTION general.fn_gum_ident_audit_insert();
CREATE TRIGGER tr_gum_ident_audit_update BEFORE UPDATE ON general.gum_ident FOR EACH ROW EXECUTE FUNCTION general.fn_gum_ident_audit_update();
CREATE TRIGGER tr_gum_ident_generate_rbid BEFORE INSERT ON general.gum_ident FOR EACH ROW EXECUTE FUNCTION general.fn_gum_ident_generate_rbid();
CREATE TRIGGER tr_gum_ident_generate_username BEFORE INSERT ON general.gum_adinf FOR EACH ROW EXECUTE FUNCTION general.fn_gum_ident_generate_username();

-- ============================================
-- Create Foreign Key constraints
-- ============================================

ALTER TABLE ONLY general.grl_rdetl
    ADD CONSTRAINT fk_grl_rdetl_rcid FOREIGN KEY (grl_rdetl_rcid) REFERENCES general.grl_rcens(grl_rcens_rcid);

ALTER TABLE ONLY general.gum_adinf
    ADD CONSTRAINT fk_gum_adinf_citizen_coid FOREIGN KEY (gum_adinf_citizen_coid) REFERENCES general.ggl_count(ggl_count_coid);

ALTER TABLE ONLY general.gum_adinf
    ADD CONSTRAINT fk_gum_adinf_czid FOREIGN KEY (gum_adinf_czid) REFERENCES general.ggl_citzn(ggl_citzn_czid);

ALTER TABLE ONLY general.gum_adinf
    ADD CONSTRAINT fk_gum_adinf_rbid FOREIGN KEY (gum_adinf_rbid) REFERENCES general.gum_ident(gum_ident_rbid);

ALTER TABLE ONLY general.gum_adinf
    ADD CONSTRAINT fk_gum_adinf_rcid FOREIGN KEY (gum_adinf_rcid) REFERENCES general.grl_rcens(grl_rcens_rcid);

ALTER TABLE ONLY general.gum_adinf
    ADD CONSTRAINT fk_gum_adinf_rdid_1 FOREIGN KEY (gum_adinf_rdid_1) REFERENCES general.grl_rdetl(grl_rdetl_rdid);

ALTER TABLE ONLY general.gum_adinf
    ADD CONSTRAINT fk_gum_adinf_rdid_2 FOREIGN KEY (gum_adinf_rdid_2) REFERENCES general.grl_rdetl(grl_rdetl_rdid);

ALTER TABLE ONLY general.gum_adinf
    ADD CONSTRAINT fk_gum_adinf_rdid_3 FOREIGN KEY (gum_adinf_rdid_3) REFERENCES general.grl_rdetl(grl_rdetl_rdid);

ALTER TABLE ONLY general.gum_ident
    ADD CONSTRAINT fk_gum_ident_id_coid FOREIGN KEY (gum_ident_id_coid) REFERENCES general.ggl_count(ggl_count_coid);
    
-- ============================================
-- Insert Into Table ggl_count
-- ============================================

INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AD', 'Andorra');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AE', 'United Arab Emirates');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AF', 'Afghanistan');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AG', 'Antigua and Barbuda');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AI', 'Anguilla');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AL', 'Albania');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AM', 'Armenia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AN', 'Netherlands Antilles');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AO', 'Angola');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AQ', 'Antarctica');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AR', 'Argentina');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AS', 'American Samoa');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AT', 'Austria');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AU', 'Australia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AW', 'Aruba');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('AZ', 'Azerbaijan');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BA', 'Bosnia and Herzegovina');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BB', 'Barbados');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BD', 'Bangladesh');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BE', 'Belgium');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BF', 'Burkina Faso');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BG', 'Bulgaria');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BH', 'Bahrain');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BI', 'Burundi');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BJ', 'Benin');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BM', 'Bermuda');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BN', 'Brunei Darussalam');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BO', 'Bolivia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BR', 'Brazil');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BS', 'Bahamas');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BT', 'Bhutan');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BV', 'Bouvet Island');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BW', 'Botswana');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BY', 'Belarus');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('BZ', 'Belize');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CA', 'Canada');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CC', 'Cocos (Keeling) Islands');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CD', 'Congo, the Democratic Republic of the');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CF', 'Central African Republic');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CG', 'Congo');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CH', 'Switzerland');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CI', 'Cote D''Ivoire');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CK', 'Cook Islands');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CL', 'Chile');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CM', 'Cameroon');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CN', 'China');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CO', 'Colombia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CR', 'Costa Rica');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CS', 'Serbia and Montenegro');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CU', 'Cuba');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CV', 'Cape Verde');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CX', 'Christmas Island');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CY', 'Cyprus');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('CZ', 'Czech Republic');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('DE', 'Germany');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('DJ', 'Djibouti');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('DK', 'Denmark');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('DM', 'Dominica');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('DO', 'Dominican Republic');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('DZ', 'Algeria');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('EC', 'Ecuador');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('EE', 'Estonia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('EG', 'Egypt');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('EH', 'Western Sahara');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('ER', 'Eritrea');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('ES', 'Spain');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('ET', 'Ethiopia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('FI', 'Finland');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('FJ', 'Fiji');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('FK', 'Falkland Islands (Malvinas)');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('FM', 'Micronesia, Federated States of');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('FO', 'Faroe Islands');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('FR', 'France');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GA', 'Gabon');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GB', 'United Kingdom');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GD', 'Grenada');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GE', 'Georgia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GF', 'French Guiana');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GH', 'Ghana');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GI', 'Gibraltar');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GL', 'Greenland');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GM', 'Gambia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GN', 'Guinea');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GP', 'Guadeloupe');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GQ', 'Equatorial Guinea');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GR', 'Greece');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GS', 'South Georgia and the South Sandwich Islands');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GT', 'Guatemala');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GU', 'Guam');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GW', 'Guinea-Bissau');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('GY', 'Guyana');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('HK', 'Hong Kong');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('HM', 'Heard Island and Mcdonald Islands');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('HN', 'Honduras');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('HR', 'Croatia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('HT', 'Haiti');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('HU', 'Hungary');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('ID', 'Indonesia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('IE', 'Ireland');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('IL', 'Israel');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('IN', 'India');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('IO', 'British Indian Ocean Territory');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('IQ', 'Iraq');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('IR', 'Iran, Islamic Republic of');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('IS', 'Iceland');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('IT', 'Italy');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('JM', 'Jamaica');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('JO', 'Jordan');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('JP', 'Japan');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('KE', 'Kenya');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('KG', 'Kyrgyzstan');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('KH', 'Cambodia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('KI', 'Kiribati');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('KM', 'Comoros');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('KN', 'Saint Kitts and Nevis');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('KP', 'Korea, Democratic People''s Republic of');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('KR', 'Korea, Republic of');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('KW', 'Kuwait');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('KY', 'Cayman Islands');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('KZ', 'Kazakhstan');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('LA', 'Lao People''s Democratic Republic');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('LB', 'Lebanon');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('LC', 'Saint Lucia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('LI', 'Liechtenstein');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('LK', 'Sri Lanka');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('LR', 'Liberia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('LS', 'Lesotho');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('LT', 'Lithuania');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('LU', 'Luxembourg');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('LV', 'Latvia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('LY', 'Libyan Arab Jamahiriya');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MA', 'Morocco');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MC', 'Monaco');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MD', 'Moldova, Republic of');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MG', 'Madagascar');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MH', 'Marshall Islands');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MK', 'Macedonia, the Former Yugoslav Republic of');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('ML', 'Mali');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MM', 'Myanmar');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MN', 'Mongolia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MO', 'Macao');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MP', 'Northern Mariana Islands');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MQ', 'Martinique');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MR', 'Mauritania');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MS', 'Montserrat');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MT', 'Malta');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MU', 'Mauritius');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MV', 'Maldives');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MW', 'Malawi');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MX', 'Mexico');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MY', 'Malaysia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('MZ', 'Mozambique');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('NA', 'Namibia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('NC', 'New Caledonia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('NE', 'Niger');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('NF', 'Norfolk Island');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('NG', 'Nigeria');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('NI', 'Nicaragua');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('NL', 'Netherlands');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('NO', 'Norway');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('NP', 'Nepal');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('NR', 'Nauru');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('NU', 'Niue');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('NZ', 'New Zealand');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('OM', 'Oman');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PA', 'Panama');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PE', 'Peru');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PF', 'French Polynesia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PG', 'Papua New Guinea');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PH', 'Philippines');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PK', 'Pakistan');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PL', 'Poland');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PM', 'Saint Pierre and Miquelon');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PN', 'Pitcairn');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PR', 'Puerto Rico');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PS', 'Palestinian Territory, Occupied');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PT', 'Portugal');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PW', 'Palau');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('PY', 'Paraguay');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('QA', 'Qatar');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('RE', 'Reunion');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('RO', 'Romania');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('RU', 'Russian Federation');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('RW', 'Rwanda');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SA', 'Saudi Arabia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SB', 'Solomon Islands');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SC', 'Seychelles');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SD', 'Sudan');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SE', 'Sweden');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SG', 'Singapore');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SH', 'Saint Helena');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SI', 'Slovenia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SJ', 'Svalbard and Jan Mayen');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SK', 'Slovakia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SL', 'Sierra Leone');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SM', 'San Marino');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SN', 'Senegal');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SO', 'Somalia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SR', 'Suriname');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('ST', 'Sao Tome and Principe');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SV', 'El Salvador');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SY', 'Syrian Arab Republic');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('SZ', 'Swaziland');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TC', 'Turks and Caicos Islands');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TD', 'Chad');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TF', 'French Southern Territories');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TG', 'Togo');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TH', 'Thailand');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TJ', 'Tajikistan');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TK', 'Tokelau');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TL', 'Timor-Leste');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TM', 'Turkmenistan');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TN', 'Tunisia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TO', 'Tonga');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TR', 'Turkey');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TT', 'Trinidad and Tobago');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TV', 'Tuvalu');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TW', 'Taiwan, Province of China');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('TZ', 'Tanzania, United Republic of');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('UA', 'Ukraine');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('UG', 'Uganda');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('UM', 'United States Minor Outlying Islands');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('US', 'United States');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('UY', 'Uruguay');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('UZ', 'Uzbekistan');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('VA', 'Holy See (Vatican City State)');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('VC', 'Saint Vincent and the Grenadines');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('VE', 'Venezuela');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('VG', 'Virgin Islands, British');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('VI', 'Virgin Islands, U.s.');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('VN', 'Viet Nam');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('VU', 'Vanuatu');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('WF', 'Wallis and Futuna');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('WS', 'Samoa');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('YE', 'Yemen');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('YT', 'Mayotte');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('ZA', 'South Africa');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('ZM', 'Zambia');
INSERT INTO general.ggl_count (ggl_count_coid, ggl_count_hr_name) VALUES ('ZW', 'Zimbabwe');

COMMIT;