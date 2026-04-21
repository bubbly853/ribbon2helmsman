-- ============================================
-- Ribbon2 General Schema for Ribbon2 SIS Finance
-- Release 1.0 - Initial Schema
-- Date: 2026-04-20
-- PostgreSQL 16+
-- Apply: psql -U ribbon2 -d ribbon2 -f 2-finance.sql
-- ============================================

BEGIN;

-- ============================================
-- Create Schema General
-- ============================================

CREATE SCHEMA finance;

-- ============================================
-- Create Table fgl_fyear
-- ============================================

CREATE TABLE finance.fgl_fyear (
    fgl_fyear_fyid character(4) NOT NULL,
    fgl_fyear_desc character varying(40) NOT NULL
);

COMMENT ON TABLE finance.fgl_fyear IS 'Financial aid year definition table.';
COMMENT ON COLUMN finance.fgl_fyear.fgl_fyear_fyid IS 'Financial aid year code.';
COMMENT ON COLUMN finance.fgl_fyear.fgl_fyear_desc IS 'Financial aid year description.';

-- ============================================
-- Create PK and Unique Constraints
-- ============================================

ALTER TABLE ONLY finance.fgl_fyear
    ADD CONSTRAINT pk_fgl_fyear PRIMARY KEY (fgl_fyear_fyid);
    
COMMIT;