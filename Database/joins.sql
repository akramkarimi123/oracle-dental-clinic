
-- File: Database/joins.sql
-- Complex queries using JOINs for UI display

-- View: Full billing details with names and cost
CREATE OR REPLACE VIEW billing_details_v AS
SELECT
    b.billing_id,
    b.appointment_id,
    b.amount,
    b.payment_status,
    b.billed_at,
    p.name AS patient_name,
    d.name AS dentist_name,
    t.name AS treatment_name,
    t.cost AS treatment_cost
FROM billing b
JOIN appointments a ON b.appointment_id = a.appointment_id
JOIN patients p ON a.patient_id = p.patient_id
JOIN dentists d ON a.dentist_id = d.dentist_id
JOIN treatments t ON a.treatment_id = t.treatment_id;