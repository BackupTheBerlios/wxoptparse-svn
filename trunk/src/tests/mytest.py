import optparse

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", action="store", type="string", dest="filename", default="Bob", 
        help="Filename")
    parser.add_option("-p", "--path", action="store", type="string", dest="path", default="..", 
        help="Path")
    
    parser.add_option("-2", "--noHelp", action="store", type="string", dest="filename2", default="No Help")
    
    parser.add_option("-n", "--count", action="store", type="int", dest="number", default="2",
        help="Count")
    parser.add_option("-m", "--float", action="store", type="float", dest="float", default=3.1415,
        help="Float")
    parser.add_option("-b", "--bool", action="store_true", dest="bBool", default = False,
        help="True by default")
    parser.add_option("", "--nbool", action="store_true", dest="bBool2", default = False,
        help="False by default")
    #~ parser.add_option("-q", "--quiet",
                  #~ action="store_const", const=0, dest="verbose", help="Quiet")
    #~ parser.add_option("-v", "--verbose",
                      #~ action="store_const", const=1, dest="verbose", help="Verbose")
    #~ parser.add_option("--noisy",
                      #~ action="store_const", const=2, dest="verbose", help="Very verbose")

    parser.add_option("--choice", type="choice", dest="choice", choices=('One', "Two", "Three"), default='One',
        help="One of ...")
    
    # This is required for my unit tests, don't need normally
    if '_wxOptParseCallback' in globals():
        parser._wxOptParseCallback = _wxOptParseCallback
    
    (options, args) = parser.parse_args()
