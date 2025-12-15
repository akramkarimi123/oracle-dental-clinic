# dentist_ui.py
from PyQt5.QtWidgets import *
from database import Database

class DentistUI(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.db.connect()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        btn_add = QPushButton("Add Dentist")
        btn_del = QPushButton("Delete Selected")
        btn_ref = QPushButton("Refresh")

        btn_add.clicked.connect(self.add_dentist)
        btn_del.clicked.connect(self.delete_dentist)
        btn_ref.clicked.connect(self.load_dentists)

        layout.addWidget(btn_add)
        layout.addWidget(btn_del)
        layout.addWidget(btn_ref)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Specialization", "Phone"])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_dentists()

    def load_dentists(self):
        query = "SELECT dentist_id, name, specialization, phone FROM dentists ORDER BY dentist_id"
        rows = self.db.fetch_all(query)
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def add_dentist(self):
        name, ok1 = QInputDialog.getText(self, "Input", "Dentist Name:")
        if not ok1 or not name: return
        spec, ok2 = QInputDialog.getText(self, "Input", "Specialization:")
        if not ok2: return
        phone, ok3 = QInputDialog.getText(self, "Input", "Phone:")
        if not ok3: return

        query = """
        INSERT INTO dentists (dentist_id, name, specialization, phone)
        VALUES (dentist_seq.NEXTVAL, :name, :spec, :phone)
        """
        self.db.execute_query(query, {"name": name, "spec": spec, "phone": phone})
        self.db.commit()
        self.load_dentists()

    def delete_dentist(self):
        row = self.table.currentRow()
        if row == -1:
            return
        did = int(self.table.item(row, 0).text())
        self.db.execute_query("DELETE FROM dentists WHERE dentist_id = :id", {"id": did})
        self.db.commit()
        self.load_dentists()