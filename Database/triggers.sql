-- Trigger to log deleted patients
CREATE OR REPLACE TRIGGER trg_patient_delete
AFTER DELETE ON patients
FOR EACH ROW
BEGIN
    INSERT INTO patient_audit (patient_id, action, action_time)
    VALUES (:OLD.patient_id, 'DELETED', SYSDATE);
END;
/

-- Trigger to auto-set appointment status on insert
CREATE OR REPLACE TRIGGER trg_appointment_status
BEFORE INSERT ON appointments
FOR EACH ROW
BEGIN
    :NEW.status := 'Scheduled';
END;
/