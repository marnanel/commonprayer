import os.path
import ConfigParser

class CommonPrayerModel:
    def __init__(self,
                 source_dir = '/opt/commonprayer/',
                 bookmarks = '~/.config/commonprayer.ini'):
        self._dir = source_dir
        self._bookmarks = bookmarks
        self._config = ConfigParser.ConfigParser()
        self._config.read(self._dir+'/bcp.ini')

        self._skeleton = file('%s/skeleton.html' % (source_dir,), 'r').read()

    def _named_page_before(self, page):
	candidate = 0
	name = '(Problem: no name)'
	page = int(page)

	for named in self._config.sections():
		if named[0]>='0' and named[0]<='9':
			n = int(named)
			if n<page and n>candidate:
				candidate = n
				name = self._config.get(named, 'name')
	return name

    def name_of(self, item, add_number = False):
        i = str(item)
        if self._config.has_option(i, 'name'):
            name = self._config.get(i, 'name')
        else:
	    name = self._named_page_before(item)

        if add_number:
            name = "%s - %s" % (item, name)

        return name

    def _children_hash(self, s, add_numbers=False):
        result = {}
        for x in [int(x) for x in s.split(',')]:
            result[x] = self.name_of(x, add_numbers)
        return result

    def __getitem__(self, item):
        i = str(item)
        result = {}

        result['name'] = self.name_of(i, True)

        if item==-1:
            result['children'] = {}
            cp = ConfigParser.ConfigParser()
            cp.read(self._bookmarks)
            result['children'] = self._children_hash(cp.get('bookmarks', 'pages'), True)
        elif self._config.has_option(i, 'children'):
            result['children'] = self._children_hash(self._config.get(i, 'children'))
        else:
            result['children'] = {}

        filename = '%s/%04d' % (self._dir, item)
        if os.path.exists(filename):
            html = self._skeleton
            html = html.replace('%(body)s',
                                file(filename, 'r').read())
            result['html'] = html

        return result

if __name__ == '__main__':

    import tempfile
    tempdir = tempfile.mkdtemp()
    print tempdir

    files = {'bcp.ini':
                 """
[general]
name=test data

[-1]
name=Bookmarks

[0]
name=test data
children=1,3

[1]
name=Lemonade

[3]
name=Edibles
children=4,5,6

[4]
name=Apples

[5]
name=Oranges

[6]
name=Bananas
""",
             '0001': 'Lemonade is delicious.',
             '0002': 'But so is water.',
             '0003': 'This is an index page.',
             '0004': 'Apples are fruit.',
             '0005': 'So are oranges.',
             '0006': 'Bananas are fruit, and good for you.',
             '0007': 'We like bananas.',
             'bookmarks.ini': """
[bookmarks]
pages=4,6
""",
             "skeleton.html": "[[[%(body)s]]]",
             }

    expect = [
        (1, {'html': '[[[Lemonade is delicious.]]]', 'name': 'Lemonade', 'children': {}}),
        (3, {'html': '[[[This is an index page.]]]', 'name': 'Edibles', 'children': {4: 'Apples', 5: 'Oranges', 6: 'Bananas'}}),
        (-1, {'name': 'Bookmarks', 'children': {4: '4 - Apples', 6: '6 - Bananas'}}),
        #(2, '[[[But so is water.]]]'),
        ]

    for f in files.keys():
        file('%s/%s' % (tempdir, f), 'w').write(files[f])

    cpm = CommonPrayerModel(tempdir,
                            tempdir+'/bookmarks.ini')

    import json # really simple deep comparison

    for e in expect:
        got = json.dumps(cpm[e[0]])
        wanted = json.dumps(e[1])
        if got==wanted:
            print "pass"
        else:
            print "fail"
            print "got   : ", got
            print "wanted: ", wanted
