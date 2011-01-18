from PySide.QtCore import *
from PySide.QtGui import *
import sys
from model import *

class CommonPrayerWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)

		self._html = QTextBrowser()
		self.setCentralWidget(self._html)

		self._prev = QAction("<-", self)
		self._next = QAction("->", self)

		self.connect(self._prev,
			SIGNAL('triggered()'),
			self,
			SLOT('goPrevious()'))

		self.connect(self._next,
			SIGNAL('triggered()'),
			self,
			SLOT('goNext()'))

		self.menuBar().addAction(self._prev)
		self.menuBar().addAction(self._next)

	def goPrevious(self):
		self.emit(SIGNAL('move(QString)'),
			'previous')

	def goNext(self):
		self.emit(SIGNAL('move(QString)'),
			'next')

	def setHtml(self, html):
		self._html.setHtml(html)
