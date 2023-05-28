from math import log
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QRadioButton, QMessageBox, QAction
from PyQt5.QtGui import QIcon, QDoubleValidator, QFont
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices


class StudyMateApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StudyMate")
        self.setWindowIcon(QIcon('rasm.png'))
        
        # Create main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Create main label
        self.main_label = QLabel("Calculates the simple and compound interest.\nEnter exactly three inputs (no more or less)")
        self.main_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.main_label.setStyleSheet("color: #333333")
        self.layout.addWidget(self.main_label)
        
        # Create radio buttons for interest type selection
        self.interest_type_label = QLabel("Select interest type:")
        self.interest_type_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.layout.addWidget(self.interest_type_label)
        
        self.simple_interest_radio = QRadioButton("Simple Interest")
        self.simple_interest_radio.setChecked(True)
        self.simple_interest_radio.setFont(QFont("Arial", 10))
        self.simple_interest_radio.setStyleSheet("color: #333333")
        self.layout.addWidget(self.simple_interest_radio)
        
        self.compound_interest_radio = QRadioButton("Compound Interest")
        self.compound_interest_radio.setFont(QFont("Arial", 10))
        self.compound_interest_radio.setStyleSheet("color: #333333")
        self.layout.addWidget(self.compound_interest_radio)
        
        # Create input labels and text fields
        self.input_labels = []
        self.input_fields = []
        
        input_names = ["Investment:", "Percentage(%):", "How many years:", "Money after time period:"]
        
        for name in input_names:
            label = QLabel(name)
            label.setFont(QFont("Arial", 10))
            label.setStyleSheet("color: #333333")
            self.input_labels.append(label)
            self.layout.addWidget(label)
            
            field = QLineEdit()
            field.setFont(QFont("Arial", 10))
            field.setStyleSheet("color: #333333; background-color: #F2F2F2; border: 1px solid #999999; border-radius: 5px;")
            validator = QDoubleValidator()  # Allow float input
            validator.setNotation(QDoubleValidator.StandardNotation)  # Enable scientific notation
            field.setValidator(validator)
            self.input_fields.append(field)
            self.layout.addWidget(field)

        # Create result label
        self.result_label = QLabel("Missing value: ")
        self.result_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.result_label.setStyleSheet("color: #333333")
        self.layout.addWidget(self.result_label)


        # Create buttons
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFont(QFont("Arial", 10))
        self.clear_button.setStyleSheet("color: #FFFFFF; background-color: #FF4444; border: none; border-radius: 5px;")
        self.layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clear_inputs)
        
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setFont(QFont("Arial", 10))
        self.calculate_button.setStyleSheet("color: #FFFFFF; background-color: #33CC33; border: none; border-radius: 5px;")
        self.layout.addWidget(self.calculate_button)
        self.calculate_button.clicked.connect(self.calculate_interest)
        
        # Create menu
        menu = self.menuBar()
        organization_menu = menu.addMenu("Our organization")
        website_action = QAction("Website", self)
        website_action.triggered.connect(self.open_website)
        organization_menu.addAction(website_action)
        
        # Set main window properties
        self.setGeometry(300, 300, 400, 300)
    
    def clear_inputs(self):
        for field in self.input_fields:
            field.clear()
        self.result_label.clear()
    
    def calculate_interest(self):
        inputs = [field.text() for field in self.input_fields]
    
        # Check if exactly 3 non-empty inputs are provided
        if len(list(filter(None, inputs))) != 3:
            QMessageBox.warning(self, "Error", "Please enter exactly three inputs.")
            return
        interest_type = "Simple Interest" if self.simple_interest_radio.isChecked() else "Compound Interest"
        
        
        if inputs[0] == '':
            p = float(inputs[1])
            n = float(inputs[2])
            m = float(inputs[3])
            # Check if the input values are non-negative
            if m <= 0 or p <= 0 or n <= 0:
                QMessageBox.warning(self, "Error", "Please enter positive values.")
                return
            if interest_type == 'Simple Interest':
                i = m/(1+p*n/100)
            else:
                i = m/(1+p/100)**n
            self.result_label.setText(f"Missing value: {i:.2f}")
        if inputs[1] == '':
            i = float(inputs[0])
            n = float(inputs[2])
            m = float(inputs[3])
            # Check if the input values are non-negative
            if m <= 0 or i <= 0 or n <= 0:
                QMessageBox.warning(self, "Error", "Please enter positive values.")
                return
            if interest_type == 'Simple Interest':
                p = (m-i)*100/(i*n)
            else:
                p = 100*((m/i)**(1/n)-1)
            self.result_label.setText(f"Missing value: {p:.2f}")
        if inputs[2] == '':
            p = float(inputs[1])
            i = float(inputs[0])
            m = float(inputs[3])
            # Check if the input values are non-negative
            if m <= 0 or p <= 0 or i <= 0:
                QMessageBox.warning(self, "Error", "Please enter positive values.")
                return
            if interest_type == 'Simple Interest':
                n = (m-i)*100/(i*p)
            else:
                n = log(m/i,1+p/100)
            self.result_label.setText(f"Missing value: {n:.2f}")
        if inputs[3] == '':
            p = float(inputs[1])
            n = float(inputs[2])
            i = float(inputs[0])
            # Check if the input values are non-negative
            if i <= 0 or p <= 0 or n <= 0:
                QMessageBox.warning(self, "Error", "Please enter positive values.")
                return
            if interest_type == 'Simple Interest':
                m = i+(i*p/100)*n
            else:
                m = i*(1+p/100)**n
            self.result_label.setText(f"Missing value: {m:.2f}")
    
    def open_website(self):
        # Open the organization website in the default browser
        QDesktopServices.openUrl(QUrl("https://matestudy.netlify.app"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    study_mate = StudyMateApp()
    study_mate.show()
    sys.exit(app.exec_())
