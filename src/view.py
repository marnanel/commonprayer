from PySide.QtCore import *
from PySide.QtGui import *
import sys
from model import *

class CommonPrayerWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)

		self._html = QTextBrowser()
		self.setCentralWidget(self._html)

	def setHtml(self, html):
		self._html.setHtml(html)
