# appointment_ui.py
from PyQt5.QtWidgets import *
from database import Database

class AppointmentUI(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.db.connect()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        btn_add = QPushButton("Book Appointment")
        btn_del = QPushButton("Delete Selected")
        btn_ref = QPushButton("Refresh")

        btn_add.clicked.connect(self.add_appointment)
        btn_del.clicked.connect(self.delete_appointment)
        btn_ref.clicked.connect(self.load_appointments)

        layout.addWidget(btn_add)
        layout.addWidget(btn_del)
        layout.addWidget(btn_ref)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Patient", "Dentist", "Treatment", "Date"])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_appointments()

    def load_appointments(self):
        query = """
        SELECT a.appointment_id, p.name, d.name, t.name, a.appointment_date
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN dentists d ON a.dentist_id = d.dentist_id
        JOIN treatments t ON a.treatment_id = t.treatment_id
        ORDER BY a.appointment_id
        """
        rows = self.db.fetch_all(query)
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def add_appointment(self):
        pid, ok1 = QInputDialog.getInt(self, "Input", "Patient ID:", 1, 1, 1000)
        if not ok1: return
        did, ok2 = QInputDialog.getInt(self, "Input", "Dentist ID:", 1, 1, 1000)
        if not ok2: return
        tid, ok3 = QInputDialog.getInt(self, "Input", "Treatment ID:", 1, 1, 1000)
        if not ok3: return
        date_str, ok4 = QInputDialog.getText(self, "Input", "Appointment Date (YYYY-MM-DD):", text="2025-12-20")
        if not ok4 or not date_str: return

        query = """
        INSERT INTO appointments (appointment_id, patient_id, dentist_id, treatment_id, appointment_date)
        VALUES (appointment_seq.NEXTVAL, :pid, :did, :tid, TO_DATE(:date_str, 'YYYY-MM-DD'))
        """
        self.db.execute_query(query, {"pid": pid, "did": did, "tid": tid, "date_str": date_str})
        self.db.commit()
        self.load_appointments()

    def delete_appointment(self):
        row = self.table.currentRow()
        if row == -1:
            return
        aid = int(self.table.item(row, 0).text())
        self.db.execute_query("DELETE FROM appointments WHERE appointment_id = :id", {"id": aid})
        self.db.commit()
        self.load_appointments()