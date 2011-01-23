from PySide.QtCore import *
from PySide.QtGui import *
import sys

class GoToPage(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self, parent)
		self.setWindowTitle('Go to page')

