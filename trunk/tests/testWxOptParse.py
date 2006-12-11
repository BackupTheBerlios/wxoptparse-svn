#!/usr/bin/python

#import wxversion
#wxversion.select("2.5.3")
import wxMock
import unittest
from elementtree import ElementTree
import sys, os
sys.path += ['..']
import wxoptparse

old = {
    "filename"  : "Bob",
    "path"      : "..",
    "filename2" : "No Help",
    "number"    : 2,
    "float"     : 3.1415,
    "bBool"     : False,
    "choice"    : "One",
}

new = {
    "filename"  : "Rob",
    "path"      : "/home",
    "filename2" : "Some Help",
    "number"    : 1,
    "float"     : 2.718,
    "bBool"     : False,
    "choice"    : "Two",
}

prev1 = {
  "filename"  : ["Older", ],
  "path"      : ["Older", ],
  "filename2" : ["Older", ],
  "number"    : [3, ],
  "float"     : [3.11, ],
  "bBool"     : [True, ],
  "bBool2"    : [False, ],
  "choice"    : ["Three", ],
}

prev2 = {
  "filename"  : ["Older", 'Bob'],
  "path"      : ["Older", '..'],
  "filename2" : ["Older", 'No Help'],
  "number"    : [3, 2],
  "float"     : [3.11, 3.1415],
  "bBool"     : [True],
  "bBool2"    : [False],
  "choice"    : ["Three", "One"],
}
noDefaults = {
    "filename"  : None,
    "path"      : None,
    "filename2" : None,
    "number"    : None,
    "float"     : None,
    "bBool"     : None,
    "bBool2"    : None,
    "choice"    : None,
}

class testWxOptParse(unittest.TestCase):
    def setUp(self):
        self.optparse = None
        self.app = None
        self.frame = None
    
    def grabParent(self, wxoptparse, app, frame):
        self.optparse = wxoptparse
        self.app = app
        self.frame = frame
    
    def diffFilenameDict(self, strFilename, compareDict):
        elements = []
        et = ElementTree.parse(strFilename)
        for item in et.findall('//option'):
            strName = item.attrib['name']
            if strName in compareDict:
                if 'lastval' not in item.attrib:
                    self.fail("Didn't find element 'lastval' in file %s, for item %s" % (strFilename, strName))
                elif item.attrib['lastval'] != str(compareDict[strName]):
                    self.fail("For element '%s', '%s' != '%s'" % (strName, item.attrib['lastval'], compareDict[strName]))
                    
                elements.append(strName)
            else:
                self.fail('%s not found in dictionary' % (strName))
        
        for key in compareDict.keys():
            if key not in elements:
                self.fail("Didn't find the key %s in the XML" % (key))
        
    def createXml(self, strFilename, info, previous = None):
        """ Create an XML file using a dictionary """
        
        fo = file(strFilename, "w")
        fo.write("<?xml version='1.0' encoding='iso-8859-1'?>\n")
        fo.write("<wxOptParse>\n")
        for key, value in info.items():
            fo.write('  <option name="%s" lastval="%s">\n' % (key, value))
            if previous and key in previous:
                for prev in previous[key]:
                    fo.write('    <recent value="%s" />\n' % (prev))
            fo.write('  </option>\n')

        fo.write("</wxOptParse>\n")

    def verifyValues(self, new):
        self.assertEqual(self.optparse.options.filename,  new['filename'])
        self.assertEqual(self.optparse.options.filename2, new['filename2'])
        self.assertEqual(self.optparse.options.path,      new['path'])
        self.assertEqual(self.optparse.options.number,    new['number'])
        self.assertEqual(self.optparse.options.float,     new['float'])
        if new['bBool'] == False and self.optparse.options.bBool == None:
            pass
        else:
            self.assertEqual(self.optparse.options.bBool,     new['bBool']) # False becomes none in this case
        self.assertEqual(self.optparse.options.choice,    new['choice'])
        self.diffFilenameDict(self.frame.getXmlFilename(), new)

    def testCreateXml(self):
        """ This test erases the XML and creates a new one by clicking "go" """
        
        strFilename = "mytest.py"
        sys.argv[0] = strFilename # Let's cheat
        try:
            os.unlink("mytest.args") # Erase
        except:
            pass
        
        myNotebook = execfile(strFilename, { 
            '__name__' : "__main__",
            '_wxOptParseCallback' : self.grabParent
             })
        
        self.assertEqual(self.frame.getXmlFilename(), "mytest.args")
        self.frame.OnGo(None)
        self.verifyValues(old)

    def testLoadLastValues(self):
        """ This test creates the XML and verifies that it loads the last values """
        
        self.createXml("mytest.args", new, prev1)
        strFilename = "mytest.py"
        sys.argv[0] = strFilename # Let's cheat
        myNotebook = execfile(strFilename, { 
            '__name__' : "__main__",
            '_wxOptParseCallback' : self.grabParent
             })
        
        self.assertEqual(self.frame.getXmlFilename(), "mytest.args")
        self.frame.OnGo(None)
        self.verifyValues(new)

    def testCreateXmlNoDefaults(self):
        """ This test erases the XML and creates a new one by clicking "go" with no defaults """
        
        strFilename = "noDefaultsTest.py"
        sys.argv[0] = strFilename # Let's cheat
        try:
            os.unlink("noDefaultsTest.args") # Erase
        except:
            pass
        
        myNotebook = execfile(strFilename, { 
            '__name__' : "__main__",
            '_wxOptParseCallback' : self.grabParent
             })
        
        self.assertEqual(self.frame.getXmlFilename(), "noDefaultsTest.args")
        self.frame.OnGo(None)
        self.verifyValues(noDefaults)

    def testLoadPreviousNoDefaults(self):
        """ This test creates the XML and verifies that it loads the previous values 
        
        Currenty this test fails.
        """
        
        self.createXml("noDefaultsTest.args", new)
        strFilename = "noDefaultsTest.py"
        sys.argv[0] = strFilename # Let's cheat
        myNotebook = execfile(strFilename, { 
            '__name__' : "__main__",
            '_wxOptParseCallback' : self.grabParent
             })
        
        self.assertEqual(self.frame.getXmlFilename(), "noDefaultsTest.args")
        self.frame.OnGo(None)
        
        self.verifyValues(new)

    def testChangeFromDefaults(self):
        """ This test erases the XML and changes all the values away from the defaults """
        
        strFilename = "mytest.py"
        sys.argv[0] = strFilename 
        try:
            os.unlink("mytest.args") # Erase
        except:
            pass
        
        myNotebook = execfile(strFilename, { 
            '__name__' : "__main__",
            '_wxOptParseCallback' : self.grabParent
             })
        
        self.assertEqual(self.frame.getXmlFilename(), "mytest.args")
        for ctrl, option in self.frame.ctrlOptions:
            if option.dest in new:
                ctrl.SetValue(new[option.dest])
            else:
                fail("Missing %s in new" % (option.name))
            
        self.frame.OnGo(None)
        self.verifyValues(new)

    def testChangeFromPrevious(self):
        """ This test creates the XML and verifies that it loads the previous values """
        
        self.createXml("mytest.args", new)
        strFilename = "mytest.py"
        sys.argv[0] = strFilename # Let's cheat
        myNotebook = execfile(strFilename, { 
            '__name__' : "__main__",
            '_wxOptParseCallback' : self.grabParent
             })
        
        self.assertEqual(self.frame.getXmlFilename(), "mytest.args")
        
        for ctrl, option in self.frame.ctrlOptions:
            if option.dest in new:
                ctrl.SetValue(old[option.dest])
            else:
                fail("Missing %s in new" % (option.name))
        
        self.frame.OnGo(None)
        
        self.verifyValues(old)

    def testLoadLastValues(self):
        """ This test creates the XML and verifies that it loads the last values """
        
        self.createXml("mytest.args", new, prev2)
        strFilename = "mytest.py"
        sys.argv[0] = strFilename # Let's cheat
        myNotebook = execfile(strFilename, { 
            '__name__' : "__main__",
            '_wxOptParseCallback' : self.grabParent
             })
        
        self.assertEqual(self.frame.getXmlFilename(), "mytest.args")
        for ctrl, option in self.frame.ctrlOptions:
            if option.dest in old:
                ctrl.SetValue(old[option.dest])
            else:
                fail("Missing %s in new" % (option.name))
        self.frame.OnGo(None)
        self.verifyValues(old)

    def testGrep(self):
        """ This test creates the XML and verifies that it loads the last values """
        
        strFilename = "grepTest.py"
        sys.argv[0] = strFilename # Let's cheat
        myNotebook = execfile(strFilename, { 
            '__name__' : "__main__",
            '_wxOptParseCallback' : self.grabParent
             })
        
        self.frame.OnGo(None)


if __name__ == '__main__':
    unittest.main()