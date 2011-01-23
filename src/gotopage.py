from PySide.QtCore import *
from PySide.QtGui import *
import sys

class GoToPage(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self, parent)
		self.setWindowTitle('Go to page')

		buttons = [
			[ '7', '8', '9', 'DEL'],
			[ '4', '5', '6', '0'],
			[ '1', '2', '3', 'OK'],
		]

		layout = QGridLayout()
		self.setLayout(layout)

		for y in range(0, len(buttons)):
			for x in range(0, len(buttons[y])):
				button = QPushButton(buttons[y][x])
				layout.addWidget(button, y+1, x)

