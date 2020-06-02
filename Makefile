project = ide

formatPaths = ${project}/ tests/ *.py
testPaths = ${project}/ tests/
flakeIgnore = --ignore=E203,E266,E501,W503
flakeExclude := --exclude=__metadata__.py
flakeOptions = --isolated --max-line-length=88
blackExclude = --exclude='__metadata__.py|definition.py|layout.py'

black-check:
	black --check --diff --target-version py38 ${blackExclude} ${formatPaths}

black-reformat:
	black --target-version py38 ${blackExclude} ${formatPaths}

flake8-check:
	flake8 ${flakeExclude} ${flakeIgnore} ${flakeOptions} ${formatPaths}

isort-check:
	isort \
		--case-sensitive \
		--check-only \
		--diff \
		--line-width=88 \
		--multi-line=3 \
		--project=abjad \
		--project=abjadext \
		--project=baca \
		--recursive \
		--skip ${project}/__init__.py \
		--skip-glob '*boilerplate*' \
		--thirdparty=ply \
		--thirdparty=roman \
		--thirdparty=uqbar \
		--trailing-comma \
		--use-parentheses \
		${formatPaths}

isort-reformat:
	isort \
		--apply \
		--case-sensitive \
		--check-only \
		--diff \
		--line-width=88 \
		--multi-line=3 \
		--project=abjad \
		--project=abjadext \
		--project=baca \
		--recursive \
		--skip ${project}/__init__.py \
		--skip-glob '*boilerplate*' \
		--thirdparty=ply \
		--thirdparty=roman \
		--thirdparty=uqbar \
		--trailing-comma \
		--use-parentheses \
		${formatPaths}

mypy:
	mypy ${project}/

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
	make black-reformat
	make isort-reformat

check:
	make black-check
	make flake8-check
	make isort-check

test:
	make black-check
	make flake8-check
	make isort-check
	make mypy
	make pytest
