from PySide.QtCore import *
from PySide.QtGui import *
import sys
from view import *
from model import *

class CommonPrayerApp(QApplication):
	def __init__(self, argv):
		QApplication.__init__(self, argv)

		self._model = CommonPrayerModel(source_dir='/home/marnanel/proj/commonprayer/pages')

		self._view = CommonPrayerWindow()
		self._view.showMaximized()

		self.display_page(100)

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

