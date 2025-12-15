# billing_ui.py
from PyQt5.QtWidgets import *
from database import Database

class BillingUI(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.db.connect()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        btn_add = QPushButton("Add Billing")
        btn_del = QPushButton("Delete Selected")
        btn_ref = QPushButton("Refresh")
        btn_search = QPushButton("Search by Billing ID")

        btn_add.clicked.connect(self.add_billing)
        btn_del.clicked.connect(self.delete_billing)
        btn_ref.clicked.connect(self.load_billing)
        btn_search.clicked.connect(self.search_billing)

        layout.addWidget(btn_add)
        layout.addWidget(btn_del)
        layout.addWidget(btn_ref)
        layout.addWidget(btn_search)

        # Updated table with meaningful columns (not just IDs)
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "Billing ID", "Appt ID", "Patient", "Dentist", "Treatment", "Amount", "Status"
        ])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_billing()

    def load_billing(self, billing_id=None):
        if billing_id is None:
            # Use the pre-joined view
            query = """
            SELECT billing_id, appointment_id, patient_name, dentist_name, 
                   treatment_name, amount, payment_status
            FROM billing_details_v
            ORDER BY billing_id
            """
            rows = self.db.fetch_all(query)
        else:
            query = """
            SELECT billing_id, appointment_id, patient_name, dentist_name, 
                   treatment_name, amount, payment_status
            FROM billing_details_v
            WHERE billing_id = :id
            """
            rows = self.db.fetch_all(query, {"id": billing_id})
        
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val) if val is not None else ""))

    def add_billing(self):
        aid, ok1 = QInputDialog.getInt(self, "Input", "Appointment ID:", 1, 1, 1000)
        if not ok1: return
        amount, ok2 = QInputDialog.getDouble(self, "Input", "Amount:", 0, 0, 10000, 2)
        if not ok2: return
        status, ok3 = QInputDialog.getText(self, "Input", "Payment Status:", text="Paid")
        if not ok3: return

        query = """
        INSERT INTO billing (billing_id, appointment_id, amount, payment_status)
        VALUES (billing_seq.NEXTVAL, :aid, :amount, :status)
        """
        cursor = self.db.execute_query(query, {"aid": aid, "amount": amount, "status": status})
        if cursor:
            self.db.commit()
            self.load_billing()

    def delete_billing(self):
        row = self.table.currentRow()
        if row == -1:
            return
        bid = int(self.table.item(row, 0).text())
        cursor = self.db.execute_query("DELETE FROM billing WHERE billing_id = :id", {"id": bid})
        if cursor:
            self.db.commit()
            self.load_billing()

    def search_billing(self):
        bid, ok = QInputDialog.getInt(self, "Search", "Enter Billing ID:", 1, 1, 1000)
        if not ok:
            return
        self.load_billing(billing_id=bid)