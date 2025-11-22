PYTHON   = python3


build:
	$(PYTHON) setup.py build

sdist:
	$(PYTHON) setup.py sdist

clean:
	rm -rf build
	rm -rf __pycache__

distclean: clean
	rm -f MANIFEST _meta.py
	rm -rf dist

meta:
	$(PYTHON) setup.py meta


.PHONY: build sdist clean distclean meta
