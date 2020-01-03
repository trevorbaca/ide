project = ide

formatPaths = ${project}/ tests/ *.py
testPaths = ${project}/ tests/
flakeIgnore = --ignore=E123,E203,E265,E266,E501,E722,F81,W503
flakeExclude = --exclude=boilerplate,abjad/__init__.py,abjad/pitch/__init__.py
flakeOptions = --max-line-length=90 --isolated
blackExclude = --exclude='__metadata__.py|definition.py|layout.py'

black-check:
	black --target-version py37 ${blackExclude} --check --diff ${formatPaths}

black-reformat:
	black --target-version py37 ${blackExclude} ${formatPaths}

flake8:
	flake8 ${flakeExclude} ${flakeOptions} ${flakeIgnore} ${formatPaths}

isort:
	isort \
		--case-sensitive \
		--multi-line 3 \
		--project abjad \
		--project abjadext \
		--recursive \
		--skip ${project}/__init__.py \
		--skip-glob '*boilerplate*' \
		--thirdparty ply \
		--thirdparty roman \
		--thirdparty uqbar \
		--trailing-comma \
		--use-parentheses -y \
		${formatPaths}

mypy:
	mypy --ignore-missing-imports ${project}/

pytest:
	rm -Rf htmlcov/
	pytest \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term \
		--cov=${project}/ \
		--durations=20 \
		${testPaths}

pytest-x:
	rm -Rf htmlcov/
	pytest \
		-x \
		--cov-config=.coveragerc \
		--cov-report=html \
		--cov-report=term \
		--cov=${project}/ \
		--durations=20 \
		${testPaths}

reformat:
	make isort
	make black-reformat

test:
	make black-check
	make flake8
	make mypy
	make pytest
