
-- Function: Get total billing for a patient
CREATE OR REPLACE FUNCTION get_patient_total_billing(p_patient_id IN NUMBER)
RETURN NUMBER IS
    v_total NUMBER := 0;
BEGIN
    SELECT NVL(SUM(amount), 0)
    INTO v_total
    FROM billing b
    JOIN appointments a ON b.appointment_id = a.appointment_id
    WHERE a.patient_id = p_patient_id;

    RETURN v_total;
END;
/
