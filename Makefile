.PHONY: help clean-pyc lint test shell coverage html publish
.DEFAULT_GOAL := help

help: ## See what commands are available.
	@echo "clean-pyc - remove Python file artifacts"
	@echo "i18n - extract the marked strings to gettext po files."
	@echo "l10n - generate the gettext mo files."
	@echo "publish - publishes a new version to pypi."

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

develop: clean-pyc
	pip install -r requirements.txt

i18n:
	cd ls/joyful && django-admin makemessages --all

l10n:
	cd ls/joyful && django-admin compilemessages

publish:
	rm -f dist/* && python setup.py sdist bdist_wheel && twine upload dist/* && echo 'Success! Go to https://pypi.python.org/pypi/ls.joyful and check that all is well.'
	python -m webbrowser https://pypi.python.org/pypi/ls.joyful/#history
