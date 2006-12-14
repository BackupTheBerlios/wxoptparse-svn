cd docs
rst2html.py --stylesheet-path=default.css index.rst index.html
cd ..
python setup.py --command-packages=setuptools.command bdist_egg
python setup.py sdist --formats=zip
