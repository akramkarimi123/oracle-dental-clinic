# treatment_ui.py
from PyQt5.QtWidgets import *
from database import Database

class TreatmentUI(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.db.connect()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        btn_add = QPushButton("Add Treatment")
        btn_del = QPushButton("Delete Selected")
        btn_ref = QPushButton("Refresh")

        btn_add.clicked.connect(self.add_treatment)
        btn_del.clicked.connect(self.delete_treatment)
        btn_ref.clicked.connect(self.load_treatments)

        layout.addWidget(btn_add)
        layout.addWidget(btn_del)
        layout.addWidget(btn_ref)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Cost"])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_treatments()

    def load_treatments(self):
        rows = self.db.fetch_all("SELECT treatment_id, name, cost FROM treatments ORDER BY treatment_id")
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def add_treatment(self):
        name, ok1 = QInputDialog.getText(self, "Input", "Treatment Name:")
        if not ok1 or not name: return
        cost, ok2 = QInputDialog.getDouble(self, "Input", "Cost:", 0, 0, 10000, 2)
        if not ok2: return

        query = """
        INSERT INTO treatments (treatment_id, name, cost)
        VALUES (treatment_seq.NEXTVAL, :name, :cost)
        """
        self.db.execute_query(query, {"name": name, "cost": cost})
        self.db.commit()
        self.load_treatments()

    def delete_treatment(self):
        row = self.table.currentRow()
        if row == -1:
            return
        tid = int(self.table.item(row, 0).text())
        self.db.execute_query("DELETE FROM treatments WHERE treatment_id = :id", {"id": tid})
        self.db.commit()
        self.load_treatments()