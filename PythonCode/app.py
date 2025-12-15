# app.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from patient_ui import PatientUI
from appointment_ui import AppointmentUI
from treatment_ui import TreatmentUI
from billing_ui import BillingUI
from dentist_ui import DentistUI  # 👈 Added

class DentalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dental Clinic Management System")
        self.resize(900, 600)

        tabs = QTabWidget()
        tabs.addTab(PatientUI(), "Patients")
        tabs.addTab(DentistUI(), "Dentists")          # 👈 Added
        tabs.addTab(AppointmentUI(), "Appointments")
        tabs.addTab(TreatmentUI(), "Treatments")
        tabs.addTab(BillingUI(), "Billing")

        self.setCentralWidget(tabs)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DentalApp()
    window.show()
    sys.exit(app.exec_())