/* 
	NOTE: CREATE DATABASE USING pgAdmin or psql before running this script
	
	****  If you have used a different name for the database than edscribed in 
		  the default .ini you must change all references in this script 
		  (use find/replace to make changes)

	Database: virtual_clinic
	The following steps are required to setup the database before running this script:
	1. create a database called virtual_clinic using pgAdmin or psql
	   NOTE: this must be done before running this script
	   
	This script contains the following:
	2. create a role called vc_user
	3. create tables
		- doctors
		- time_slot
		- diary
		- service
		- patients
		- appointments
		- document_type
		- patient_documents

	4. create constraints for all tables
*/


CREATE ROLE vc_user WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEROLE
  NOREPLICATION
  PASSWORD 'password123';

GRANT CONNECT ON DATABASE virtual_clinic TO vc_user;

GRANT ALL ON DATABASE virtual_clinic TO postgres;

GRANT TEMPORARY, CONNECT ON DATABASE virtual_clinic TO PUBLIC;

-- Table: public.doctors

-- DROP TABLE public.doctors;

CREATE TABLE public.doctors
(
    doctor_id serial NOT NULL,
    first_name character varying(50),
    middle_name character varying(50),
    last_name character varying(50),
    CONSTRAINT doctors_pkey PRIMARY KEY (doctor_id)
);

ALTER TABLE public.doctors
    OWNER to postgres;

GRANT ALL ON TABLE public.doctors TO postgres;

GRANT ALL ON TABLE public.doctors TO vc_user;


-- Table: public.time_slot

-- DROP TABLE public.time_slot;

CREATE TABLE public.time_slot
(
    time_slot_id integer NOT NULL,
    time_slot character varying(50),
    time_from character varying(10),
    time_to character varying(10),
    time_from_24 character varying(10),
    time_to_24 character varying(10),
    CONSTRAINT time_slot_pkey PRIMARY KEY (time_slot_id)
);

ALTER TABLE public.time_slot
    OWNER to postgres;

GRANT ALL ON TABLE public.time_slot TO postgres;

GRANT ALL ON TABLE public.time_slot TO vc_user;



-- Table: public.diary

-- DROP TABLE public.diary;

CREATE TABLE public.diary
(
    diary_id serial NOT NULL,
    doctor_id integer NOT NULL,
    diary_date date NOT NULL,
    time_slot_id integer NOT NULL,
    available character(1) NOT NULL,
    notes character varying(255),
    CONSTRAINT diary_pkey PRIMARY KEY (diary_id),
    CONSTRAINT fk_diary_doctors FOREIGN KEY (doctor_id)
        REFERENCES public.doctors (doctor_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_diary_time_slot FOREIGN KEY (time_slot_id)
        REFERENCES public.time_slot (time_slot_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

ALTER TABLE public.diary
    OWNER to postgres;

GRANT ALL ON TABLE public.diary TO postgres;

GRANT ALL ON TABLE public.diary TO vc_user;


-- Table: public.service

-- DROP TABLE public.service;

CREATE TABLE public.service
(
    service_id integer NOT NULL,
    service character varying(25),
    price numeric(6,2),
    sort_order integer,
    CONSTRAINT service_pkey PRIMARY KEY (service_id)
);

ALTER TABLE public.service
    OWNER to postgres;

GRANT ALL ON TABLE public.service TO postgres;

GRANT ALL ON TABLE public.service TO vc_user;


-- Table: public.patients

-- DROP TABLE public.patients;

CREATE TABLE public.patients
(
    patient_id serial NOT NULL,
    first_name character varying(50),
    last_name character varying(50),
    middle_name character varying(50),
    dob date,
    sex character(1),
    email character varying(150),
    phone character varying(12),
    medicare_no character varying(10),
    medicare_pos smallint,
    CONSTRAINT patients_pkey PRIMARY KEY (patient_id)
);

ALTER TABLE public.patients
    OWNER to postgres;

GRANT ALL ON TABLE public.patients TO postgres;

GRANT ALL ON TABLE public.patients TO vc_user;


-- Table: public.appointments

-- DROP TABLE public.appointments;

CREATE TABLE public.appointments
(
    patient_id integer NOT NULL,
    diary_id integer NOT NULL,
    service_id integer,
    videoconference_url character varying(255),
    amount_paid numeric(6,2),
    paid_date date,
    receipt character varying(50),
    notes character varying(255),
    start_url character varying(700),
    join_url character varying(700),
    CONSTRAINT appointments_pkey PRIMARY KEY (patient_id, diary_id),
    CONSTRAINT fk_appointment_diary FOREIGN KEY (diary_id)
        REFERENCES public.diary (diary_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_appointment_patient FOREIGN KEY (patient_id)
        REFERENCES public.patients (patient_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_appointment_service FOREIGN KEY (service_id)
        REFERENCES public.service (service_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

ALTER TABLE public.appointments
    OWNER to postgres;

GRANT ALL ON TABLE public.appointments TO postgres;

GRANT ALL ON TABLE public.appointments TO vc_user;


-- Table: public.document_type

-- DROP TABLE public.document_type;

CREATE TABLE public.document_type
(
    document_type_id integer NOT NULL,
    document_type character varying(50),
    sort_order integer,
    CONSTRAINT document_type_pkey PRIMARY KEY (document_type_id)
);

ALTER TABLE public.document_type
    OWNER to postgres;

GRANT ALL ON TABLE public.document_type TO postgres;

GRANT ALL ON TABLE public.document_type TO vc_user;




-- Table: public.patient_documents

-- DROP TABLE public.patient_documents;

CREATE TABLE public.patient_documents
(
    document_id serial NOT NULL,
    description character varying(255),
    file_name character varying(255),
    document_type_id integer,
    patient_id integer,
    CONSTRAINT patient_documents_pkey PRIMARY KEY (document_id),
    CONSTRAINT fk_patient_documents_documents FOREIGN KEY (document_type_id)
        REFERENCES public.document_type (document_type_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_patient_documents_patients FOREIGN KEY (patient_id)
        REFERENCES public.patients (patient_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

ALTER TABLE public.patient_documents
    OWNER to postgres;

GRANT ALL ON TABLE public.patient_documents TO postgres;

GRANT ALL ON TABLE public.patient_documents TO vc_user;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public to vc_user;
