-- View: Patient Appointments Summary
CREATE OR REPLACE VIEW patient_appointments_v AS
SELECT
    p.name AS patient_name,
    d.name AS dentist_name,
    t.name AS treatment_name,
    a.appointment_date,
    a.status
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN dentists d ON a.dentist_id = d.dentist_id
JOIN treatments t ON a.treatment_id = t.treatment_id;

-- View: Monthly Revenue by Dentist
CREATE OR REPLACE VIEW monthly_revenue_by_dentist_v AS
SELECT
    d.name AS dentist_name,
    EXTRACT(MONTH FROM b.billed_at) AS month_num,
    SUM(b.amount) AS total_revenue
FROM billing b
JOIN appointments a ON b.appointment_id = a.appointment_id
JOIN dentists d ON a.dentist_id = d.dentist_id
WHERE b.payment_status = 'Paid'
GROUP BY d.name, EXTRACT(MONTH FROM b.billed_at);