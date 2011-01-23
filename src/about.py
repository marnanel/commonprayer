from PySide.QtCore import *
from PySide.QtGui import *
import sys

class About(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self, parent)
		self.setWindowTitle('About the Book of Common Prayer')

