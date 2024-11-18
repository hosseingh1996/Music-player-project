from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QComboBox, QPushButton, QFileDialog,QSlider,QLineEdit,QCheckBox, QSpinBox
from PyQt5 import uic
import sys
import string
import random
from PyQt5 import QtCore



class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # load the ui file
        uic.loadUi("Password Generator.ui", self)
        self.setWindowTitle("password generator")

        # Define our widget
        self.edit = self.findChild(QLineEdit, name="lineEdit")
        self.upper_check = self.findChild(QCheckBox, name="uppercase")
        self.lower_check = self.findChild(QCheckBox, name="lowercase")
        self.digit_check = self.findChild(QCheckBox, name="digit")
        self.other_check = self.findChild(QCheckBox, name="other")
        self.generator_button = self.findChild(QPushButton, name="generatepassword")
        self.copy_button = self.findChild(QPushButton, name="copy")
        self.spin_box = self.findChild(QSpinBox, name="passwordlength")

        # clicked the button
        self.generator_button.clicked.connect(self.password_generator)
        self.copy_button.clicked.connect(self.copy_password)
        # show tha app
        self.show()

    def password_generator(self):
        length = self.spin_box.value()

        characters = ''

        if self.upper_check.isChecked():
            characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        if self.lower_check.isChecked():
            characters += "abcdefghijklmnopqrstuvwxyz"

        if self.digit_check.isChecked():
            characters += "0123456789"

        if self.other_check.isChecked():
            characters += "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"

        # Ensure at least one required character is in the password
        password = []
        if self.upper_check.isChecked():
            password.append(random.choice(string.ascii_uppercase))
        if self.lower_check.isChecked():
            password.append(random.choice(string.ascii_lowercase))
        if self.digit_check.isChecked():
            password.append(random.choice(string.digits))
        if self.other_check.isChecked():
            password.append(random.choice(string.punctuation))

        # Fill the remaining length with random choices from the combined set
        remaining_length = length - len(password)
        if remaining_length > 0:
            password += random.choices(characters, k=remaining_length)

        # Shuffle the resultant password
        random.shuffle(password)

        # Generate the password
        generated_password = ''.join(password)
        self.edit.setText(generated_password)

    def copy_password(self):
        copy = QApplication.clipboard()
        copy.setText(self.edit.text())


# initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()