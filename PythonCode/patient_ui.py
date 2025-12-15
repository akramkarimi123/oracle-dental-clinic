# patient_ui.py
from PyQt5.QtWidgets import *
from database import Database

class PatientUI(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.db.connect()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        btn_add = QPushButton("Add Patient")
        btn_del = QPushButton("Delete Selected")
        # ❌ Refresh button REMOVED as requested
        btn_search = QPushButton("Search by Name or ID")

        btn_add.clicked.connect(self.add_patient)
        btn_del.clicked.connect(self.delete_patient)
        btn_search.clicked.connect(self.search_patient)

        layout.addWidget(btn_add)
        layout.addWidget(btn_del)
        layout.addWidget(btn_search)  # ← Refresh button gone

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Email", "Address"])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_patients()

    def load_patients(self, query=None, params=None):
        if query is None:
            query = "SELECT patient_id, name, phone, email, address FROM patients ORDER BY patient_id"
            rows = self.db.fetch_all(query)
        else:
            rows = self.db.fetch_all(query, params)
        
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val) if val is not None else ""))

    def add_patient(self):
        name, ok1 = QInputDialog.getText(self, "Input", "Patient Name:")
        if not ok1 or not name.strip():
            return
        phone, ok2 = QInputDialog.getText(self, "Input", "Phone:")
        if not ok2:
            return
        email, ok3 = QInputDialog.getText(self, "Input", "Email:")
        if not ok3:
            return
        address, ok4 = QInputDialog.getText(self, "Input", "Address:")
        if not ok4:
            return

        def to_none_if_empty(s):
            return s if s.strip() != "" else None

        params = {
            "name": name,
            "phone": to_none_if_empty(phone),
            "email": to_none_if_empty(email),
            "address": to_none_if_empty(address)
        }

        query = """
        INSERT INTO patients (patient_id, name, phone, email, address)
        VALUES (patient_seq.NEXTVAL, :name, :phone, :email, :address)
        """
        cursor = self.db.execute_query(query, params)  # ✅ Correct method name
        if cursor:
            self.db.commit()
            self.load_patients()

    def delete_patient(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Warning", "Please select a patient to delete.")
            return
        pid = int(self.table.item(row, 0).text())
        # 🔥 FIXED: was 'execute_job' → now 'execute_query'
        cursor = self.db.execute_query("DELETE FROM patients WHERE patient_id = :id", {"id": pid})
        if cursor:
            self.db.commit()
            self.load_patients()

    def search_patient(self):
        choice, ok = QInputDialog.getItem(
            self, "Search", "Search by:", ["Name", "ID"], 0, False
        )
        if not ok:
            return

        if choice == "ID":
            pid, ok2 = QInputDialog.getInt(self, "Search by ID", "Patient ID:", 1, 1, 10000)
            if not ok2:
                return
            query = "SELECT patient_id, name, phone, email, address FROM patients WHERE patient_id = :id"
            self.load_patients(query, {"id": pid})
        else:  # Name
            name, ok2 = QInputDialog.getText(self, "Search by Name", "Enter full or partial name:")
            if not ok2 or not name.strip():
                return
            query = "SELECT patient_id, name, phone, email, address FROM patients WHERE UPPER(name) LIKE UPPER(:name)"
            self.load_patients(query, {"name": f"%{name.strip()}%"})