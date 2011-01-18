import xml.sax
import sys
import os

source = 'data/'
target = 'pages/'
if not os.path.exists(target):
	os.makedirs(target)

def copy_in_skeleton():
    skeleton = file(source+'skeleton.html','r').read()
    file(target+'skeleton.html','w').write(skeleton)

    shield = file(source+'ecusa-shield.png','rb').read()
    file(target+'logo.png','wb').write(shield)

def parse_xml(filename):
    class Handler(xml.sax.handler.ContentHandler):
        def __init__(self):
            self._target = None
            self._pagenumber = None
            self._name = None
            self._credit = None
            self._parentSection = None
            self._names = {0: 'Book of Common Prayer',
                           -1: 'Bookmarks'}
            self._children = {}

        def _storeSection(self, from_id, to_id, name):
            self._names[to_id] = name
            self._children[from_id] = '%s,%d' % (self._children.get(from_id,''),
                                                 to_id)

        def startElement(self, name, attributes):
            if name=='content':
                if not self._pagenumber:
                    print 'content outside page'
                    sys.exit(255)

                self._target = file('%s/%04d' % (target, self._pagenumber),
                                    'w')

            elif name=='book-of-common-prayer':
                self._name = attributes['name']
                self._credit = attributes['credit']
                self._title = attributes['title']
            elif name=='page':
                self._pagenumber = int(attributes['id'])
            elif name=='section':
                if attributes['level']=='1':
                    self._parentSection = self._pagenumber
                    self._storeSection(0,
                                       self._parentSection,
                                       attributes['title'])
                elif attributes['level']=='2':
                    if not self._parentSection:
                        print 'Level 2 section outside a level 1 section'
                        sys.exit(255)
                    
                    self._storeSection(self._parentSection,
                                       self._pagenumber,
                                       attributes['title'])
            else:
                print 'unknown tag: ',name
                sys.exit(255)

        def endElement(self, name):
            if name=='content':
                self._target.close()
                self._target = None

            elif name=='page':
                self._pagenumber = None

        def characters(self, content):
            if self._target:
                self._target.write(content)

        def endDocument(self):
            conf = file(target+'/bcp.ini', 'w')
            conf.write('[general]\n')
            conf.write('name=%s\n' % (self._name,))
            conf.write('title=%s\n' % (self._title,))
            conf.write('credit=%s\n' % (self._credit,))
            conf.write('\n')

            for k in sorted(self._names.keys()):
                conf.write('[%s]\n' % (k,))
                conf.write('name=%s\n' % (self._names[k],))
                if self._children.has_key(k):
                    conf.write('children=%s\n' % (self._children[k][1:],))
                conf.write('\n')

            conf.close()

    handler = Handler()

    xml.sax.parse(filename, handler)

if __name__=='__main__':
    copy_in_skeleton()
    parse_xml(source+'bcp.xml')
