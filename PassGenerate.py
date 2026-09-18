from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit, QCheckBox, QSpinBox, QProgressBar, QMessageBox
from PyQt5 import uic
import sys
import random


class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		# Load the ui file
		uic.loadUi("firstPassGenerate.ui", self)
		self.setWindowTitle("Password Generator ")
		
        # define widgets
		self.visibleButton = self.findChild(QPushButton, "visibleButton")
		self.copyButton = self.findChild(QPushButton, "copyButton")
		self.generateButton = self.findChild(QPushButton, "generateButton")
		self.refreshButton = self.findChild(QPushButton, "refreshButton")
		
		self.passwordLineEdit = self.findChild(QLineEdit, "passwordLineEdit")
		self.passwordLineEdit.setEchoMode(QLineEdit.Normal)
		
		self.digitCheckBox = self.findChild(QCheckBox, "digitCheckBox")
		self.symbolCheckBox = self.findChild(QCheckBox, "symbolCheckBox")
		self.uppercaseCheckBox = self.findChild(QCheckBox, "uppercaseCheckBox")
		self.lowercaseCheckBox = self.findChild(QCheckBox, "lowercaseCheckBox")
		
		self.lengthLabel = self.findChild(QLabel, "lengthLabel")
		self.strengthLabel = self.findChild(QLabel, "strengthLabel")
		
		self.lengthSpinBox = self.findChild(QSpinBox, "lengthSpinBox")
		
		self.strengthprogressBar = self.findChild(QProgressBar, "strengthProgressBar")
		self.strengthprogressBar.setRange(0, 100)
		self.strengthprogressBar.setValue(0)

		# signals and slots
		self.visibleButton.clicked.connect(self.visibility)
		self.copyButton.clicked.connect(self.copyPassword)
		self.generateButton.clicked.connect(self.generatePassword)
		self.refreshButton.clicked.connect(self.refresh)

		# show the app
		self.show()
		
	# create a list of allowable characters to generate password
	def getAllowedCharacters(self):
		self.charList = ""
		if self.digitCheckBox.isChecked():
			self.charList += "0123456789"
		if self.symbolCheckBox.isChecked():
			self.charList += "!@#$%^&"
		if self.uppercaseCheckBox.isChecked():
			self.charList += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		if self.lowercaseCheckBox.isChecked():
			self.charList += "abcdefghijklmnopqrstuvwxyz"
		return self.charList
	

    # generate password
	def generatePassword(self):
		charList = self.getAllowedCharacters()
		length = self.lengthSpinBox.value()
		if not charList:
			QMessageBox.warning(self, "warning", "Please select at least one character type")
		else:
			password = ""
			for _ in range(length):
			    password += random.choice(charList)
			self.passwordLineEdit.setText(password)
			score  = self.clacScore(password)
			self.strengthprogressBar.setValue(score)
			self.updateScoreLabel(score)
			
	
	# visibility of password	
	def visibility(self):
		if self.passwordLineEdit.echoMode() == QLineEdit.Password:
			self.passwordLineEdit.setEchoMode(QLineEdit.Normal)
		else:
			self.passwordLineEdit.setEchoMode(QLineEdit.Password)
			
	# copy password to clipboard		
	def copyPassword(self):
		password = self.passwordLineEdit.text()
		if not password:
			QMessageBox.warning(self, "warning", "There is no password to copy.")
		else:
			clipboard = QApplication.clipboard()
			clipboard.setText(password)
			
	# calculate the score of password
	def clacScore(self, password):
		totalScore = 0
		lengthScore = 0
		if len(password) <= 8:
			lengthScore += 15
		elif len(password) > 8 and len(password) <= 16:
			lengthScore += 30
		elif len(password) > 16:
			lengthScore += 40
		totalScore += lengthScore
		if any(char.isupper() for char in password):
			totalScore += 15
		if any(char.islower() for char in password):
			totalScore += 15
		if any(char.isdigit() for char in password):
			totalScore += 15
		if any(char in "!@#$%^&" for char in password):
			totalScore += 15
		return totalScore
	

	def updateScoreLabel(self, score):
		if score <= 45:
			self.strengthLabel.setText("Strength : Weak")
			self.strengthLabel.setStyleSheet("color : red;")
			self.strengthprogressBar.setStyleSheet("QProgressBar::chunk {background-color: red;}")
		elif score <=60:
			self.strengthLabel.setText("Strength : Medium")
			self.strengthLabel.setStyleSheet("color : orange;")
			self.strengthprogressBar.setStyleSheet("QProgressBar::chunk {background-color: orange;}")
		elif score <= 90:
			self.strengthLabel.setText("Strength : Strong")
			self.strengthLabel.setStyleSheet("color : light green;")
			self.strengthprogressBar.setStyleSheet("QProgressBar::chunk {background-color: light green;}")
		else:
			self.strengthLabel.setText("Strength : Very Strong")
			self.strengthLabel.setStyleSheet("color : green;")
			self.strengthprogressBar.setStyleSheet("QProgressBar::chunk {background-color: green;}")
		
	
			

	# regenerate password with previous settings
	def refresh(self):
		self.generatePassword()
		


		
# Initialize The App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
