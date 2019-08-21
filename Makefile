tox:
	tox

test:
	python3 setup.py test

flake8:
	flake8 --ignore=E501,F403 --max-complexity 12 django_enumfield_named_choices

install:
	python3 setup.py install

develop:
	python3 setup.py develop

coverage:
	coverage run --include=django_enumfield_named_choices/* setup.py test

clean:
	rm -rf .tox/ dist/ *.egg *.egg-info .coverage* .eggs

dist: django_enumfield_named_choices/__init__.py
	rm -rf dist/ 
	python3 setup.py sdist bdist_wheel

twain_check: dist
	twine check dist/*

twain_upload_test: dist twain_check
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

twain_upload: dist twain_check
	twine upload dist/*