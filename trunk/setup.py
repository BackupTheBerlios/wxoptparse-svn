from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

# Notes to self:
# python setup.py sdist --formats=zip
# To create the zip file

# python setup.py --command-packages=setuptools.command bdist_egg
# To create the egg file

# python setup.py register
# to register with PyPI
# 

setup(name="wxOptParse",
    version="0.1.2",
    description="wxOptParse: run the command line options from a dialog box.",
    long_description="""\
wxOptParse is a Python program that brings up a graphical representation of the options 
that another python program has for the command line, via the optparse module.

What this means is that if if you have a program that uses optparse you can click on checkboxes, 
edit boxes, combo boxes, etc. instead of using the command line.
""",
    author="Scott Kirkwood",
    author_email="scottakirkwood@gmail.com",
    url="http://wxoptparse.berlios.de/",
    download_url='http://developer.berlios.de/project/showfiles.php?group_id=2209&release_id=3368',
    packages=find_packages(exclude='tests'),
    scripts=["runWx"],
    keywords=['wxOptParse', 'optparse', 'python', 'wxPython'],
    license='GNU GPL',
    zip_safe=True,
    platforms=['POSIX', 'Windows', 'MacOS X'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
#    package_data={'': '*.xml'},
#    install_requires=['wxPython>=2.5.3'], # Doesn't work on my machine
    )
