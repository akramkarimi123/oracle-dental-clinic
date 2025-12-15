-- Indexes for frequent queries
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_billing_paid
ON billing (
    CASE
        WHEN payment_status = 'Paid' THEN payment_status
        ELSE NULL
    END
);


