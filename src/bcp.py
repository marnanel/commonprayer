from PySide.QtCore import *
from PySide.QtGui import *
import sys
from view import *
from model import *
from gotopage import *
from about import *

class CommonPrayerApp(QApplication):
	def __init__(self, argv):
		QApplication.__init__(self, argv)

		self._model = CommonPrayerModel(source_dir='/home/marnanel/proj/commonprayer/pages')

		self._view = CommonPrayerWindow()
		self._view.showMaximized()

		self._enumerate_sections()

		self.connect(self._view,
			SIGNAL('jump(QString,int)'),
			self,
			SLOT('jump(QString,int)'))

		self._page = 100
		self.display_page(self._page)

	def _enumerate_sections(self, candidate=None):
		toplevel = False

		if candidate is None:
			toplevel = True
			candidate = self._model[0]['children']

		for page in sorted(candidate.keys()):
			page_or_placeholder = page

			inner = self._model[page]['children']

			if toplevel and len(inner)!=0:
				page_or_placeholder = -1

			self._view.addSection(candidate[page],
				page_or_placeholder,
				not toplevel)

			if toplevel:
				self._enumerate_sections(inner)

	def jump(self, mode, wrt=-1):
		if wrt==-1:
			wrt = self._page

		# Special case some modes.
		if mode=='goto':
			self._gotopage = GoToPage(self._view)
			self.connect(self._gotopage,
				SIGNAL("jump(QString,int)"),
				self,
				SLOT("jump(QString,int)"))
			self._gotopage.show()
			return
		elif mode=='about':
			self._about = About(self._view)
			self._about.show()
			return

		page = self._model.move(mode, wrt)

		self._page = page['page']
		# FIXME: display the warning, if there was one
		self.display_page(self._page)

	def display_page(self, page_number):
		page = self._model[page_number]

		if page.has_key('html'):
			self._view.setHtml(page['html'])

		if page.has_key('name'):
			self._view.setWindowTitle(
				'%s - Book of Common Prayer' % (
					page['name']))

if __name__=='__main__':
	app = CommonPrayerApp(sys.argv)
	sys.exit(app.exec_())

