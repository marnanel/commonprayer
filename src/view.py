from PySide.QtCore import *
from PySide.QtGui import *
import sys
from model import *
from settings import *

class JumpAction(QAction):
	def __init__(self, name, parent, mode, number=-1):
		QAction.__init__(self, name, parent)

		self._mode = mode
		self._number = number

		self.connect(self,
			SIGNAL("triggered()"),
			self,
			SLOT("_send_mode_and_number()"))

	def _send_mode_and_number(self):
		self.emit(SIGNAL("jump(QString,int)"),
			self._mode,
			self._number)

class CommonPrayerWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)

		self._html = QTextBrowser()
		self.setCentralWidget(self._html)

		self.menuBar().addAction(self._jump_action("Previous", 'previous'))
		self.menuBar().addAction(self._jump_action("Next", 'next'))

		self._sections = QMenu('Sections')
		self.menuBar().addMenu(self._sections)

	def _jump_action(self, name, mode, number=-1):
		action = JumpAction(name, self, mode, number)
		self.connect(action, SIGNAL("jump(QString,int)"),
			self, SIGNAL("jump(QString,int)"))
		return action

	def addSection(self, name, number, subsection):
		"""
		Adds a new section of the book.
		Currently only supports two levels.

		name - the name of the section.
		number - the page number; if -1, represents
			no page as such, but there are
			subpages.
		subsection - True if level 2, False if level 1.
		"""
		if subsection:
			if number==-1:
				pass # shouldn't happen
			else:
				item = self._jump_action(name, 'exact', number)
				self._latest_section.addAction(item)
		else:
			if number==-1:
				item = QMenu(name)
				self._sections.addMenu(item)
				self._latest_section = item
			else:
				item = self._jump_action(name, 'exact', number)
				self._sections.addAction(item)

	def setHtml(self, html):
		self._html.setHtml(html)
