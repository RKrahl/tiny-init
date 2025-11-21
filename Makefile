PYTHON   = python3


build:
	$(PYTHON) setup.py build

sdist:
	$(PYTHON) setup.py sdist

clean:
	rm -f *~
	rm -rf build

distclean: clean
	rm -f MANIFEST
	rm -rf dist


.PHONY: build sdist clean distclean
