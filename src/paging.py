from glob import glob

class NextPage:
	def __init__(self, wrt):
		self._wrt = wrt
		self._candidate = None
		self._lowest = None

	def take(self, number):
		if self._lowest is None or number < self._lowest:
			self._lowest = number

		if number > self._wrt and (self._candidate is None or number < self._candidate):
			self._candidate = number

		return False

	def result(self):
		warning = ''

		if self._candidate is None:
			self._candidate = self._lowest
			warning = 'first'

		return { 'page': self._candidate,
			'warning': warning }

class PreviousPage:
	def __init__(self, wrt):
		self._wrt = wrt
		self._candidate = None
		self._highest = None

	def take(self, number):
		if self._highest is None or number > self._highest:
			self._highest = number

		if number < self._wrt and (self._candidate is None or number > self._candidate):
			self._highest = number

		return False

	def result(self):
		warning = ''

		if self._candidate is None:
			self._candidate = self._highest
			warning = 'last'

		return { 'page': self._candidate,
			'warning': warning }

class NearestPage:
	def __init__(self, wrt):
		self._wrt = wrt
		self._candidate = None

	def take(self, number):
		if self._candidate is None or abs(number-self._wrt) < abs(self._candidate-self._wrt):
			self._candidate = number

		return False

	def result(self):
		warning = ''

		if self._candidate != self._wrt:
			warning = 'nearest'

		return { 'page': self._candidate,
			'warning': warning }

class Paging:
	def __init__(self, path):
		self._path = path + '/*'

	def scan(self, recipient):

		for file in glob(self._path):
			name = file[file.rindex('/')+1:]
			if '.' in name:
				continue
			recipient.take(int(name))

		return recipient.result()

p = Paging('pages')
print p.scan(NearestPage(0))

