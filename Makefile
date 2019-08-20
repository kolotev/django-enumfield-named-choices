.PHONY: test
test:
	python3 setup.py test

.PHONY: flake8
flake8:
	flake8 --ignore=E501,F403 --max-complexity 12 django_enumfield_named_choices

.PHONY: install
install:
	python3 setup.py install

.PHONY: develop
develop:
	python3 setup.py develop

.PHONY: coverage
coverage:
	coverage run --include=django_enumfield_named_choices/* setup.py test

.PHONY: clean
clean:
	rm -rf .tox/ dist/ *.egg *.egg-info .coverage* .eggs
