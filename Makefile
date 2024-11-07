install:
	pip install --break-system-packages build
	python -m build
	pip install --break-system-packages dist/*.whl

uninstall:
	pip uninstall --break-system-packages arquix

.PHONY: install uninstall
