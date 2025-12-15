-- File: procedures.sql
-- Dental Clinic Management System - Stored Procedures

-- 1. Add a new patient
CREATE OR REPLACE PROCEDURE add_patient(
    p_name      IN VARCHAR2,
    p_phone     IN VARCHAR2,
    p_email     IN VARCHAR2,
    p_address   IN VARCHAR2,
    p_patient_id OUT NUMBER
) AS
BEGIN
    INSERT INTO patients (patient_id, name, phone, email, address)
    VALUES (patient_seq.NEXTVAL, p_name, p_phone, p_email, p_address)
    RETURNING patient_id INTO p_patient_id;
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- 2. Add a new dentist
CREATE OR REPLACE PROCEDURE add_dentist(
    p_name            IN VARCHAR2,
    p_specialization  IN VARCHAR2,
    p_phone           IN VARCHAR2,
    p_email           IN VARCHAR2,
    p_dentist_id OUT NUMBER
) AS
BEGIN
    INSERT INTO dentists (dentist_id, name, specialization, phone, email)
    VALUES (dentist_seq.NEXTVAL, p_name, p_specialization, p_phone, p_email)
    RETURNING dentist_id INTO p_dentist_id;
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- 3. Book a new appointment
CREATE OR REPLACE PROCEDURE book_appointment(
    p_patient_id     IN NUMBER,
    p_dentist_id     IN NUMBER,
    p_treatment_id   IN NUMBER,
    p_appointment_date IN DATE,
    p_appointment_id OUT NUMBER
) AS
    v_count NUMBER;
BEGIN
    -- Optional: Validate that patient/dentist/treatment exist
    SELECT COUNT(*) INTO v_count FROM patients WHERE patient_id = p_patient_id;
    IF v_count = 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Patient ID not found');
    END IF;

    SELECT COUNT(*) INTO v_count FROM dentists WHERE dentist_id = p_dentist_id;
    IF v_count = 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'Dentist ID not found');
    END IF;

    SELECT COUNT(*) INTO v_count FROM treatments WHERE treatment_id = p_treatment_id;
    IF v_count = 0 THEN
        RAISE_APPLICATION_ERROR(-20003, 'Treatment ID not found');
    END IF;

    INSERT INTO appointments (appointment_id, patient_id, dentist_id, treatment_id, appointment_date)
    VALUES (appointment_seq.NEXTVAL, p_patient_id, p_dentist_id, p_treatment_id, p_appointment_date)
    RETURNING appointment_id INTO p_appointment_id;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/

-- 4. Create a billing record
CREATE OR REPLACE PROCEDURE create_billing(
    p_appointment_id   IN NUMBER,
    p_amount           IN NUMBER,
    p_payment_status   IN VARCHAR2,
    p_billing_id       OUT NUMBER
) AS
    v_count NUMBER;
BEGIN
    -- Validate appointment exists
    SELECT COUNT(*) INTO v_count FROM appointments WHERE appointment_id = p_appointment_id;
    IF v_count = 0 THEN
        RAISE_APPLICATION_ERROR(-20004, 'Appointment ID not found');
    END IF;

    INSERT INTO billing (billing_id, appointment_id, amount, payment_status)
    VALUES (billing_seq.NEXTVAL, p_appointment_id, p_amount, p_payment_status)
    RETURNING billing_id INTO p_billing_id;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;
/