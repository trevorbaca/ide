project = ide

formatPaths = ${project}/ tests/ *.py
testPaths = ${project}/ tests/
flakeIgnore = --ignore=E123,E203,E231,E265,E266,E501,E722,F81,W503
flakeExclude := --exclude=
flakeExclude := $(flakeExclude)ide/__init__.py
flakeExclude := $(flakeExclude),ide/scores/red_score/red_score/materials/__init__.py
flakeExclude := $(flakeExclude),ide/scores/red_score/red_score/tools/__init__.py
flakeExclude := $(flakeExclude),ide/scores/red_score/red_score/__init__.py
flakeExclude := $(flakeExclude),ide/scores/blue_score/blue_score/materials/__init__.py
flakeExclude := $(flakeExclude),ide/scores/blue_score/blue_score/tools/__init__.py
flakeExclude := $(flakeExclude),ide/scores/blue_score/blue_score/__init__.py
flakeExclude := $(flakeExclude),ide/scores/green_score/green_score/materials/__init__.py
flakeExclude := $(flakeExclude),ide/scores/green_score/green_score/tools/__init__.py
flakeExclude := $(flakeExclude),ide/scores/green_score/green_score/__init__.py
flakeOptions = --max-line-length=90 --isolated
blackExclude = --exclude='__metadata__.py|definition.py|layout.py'

black-check:
	black --target-version py37 ${blackExclude} --check --diff ${formatPaths}

black-reformat:
	black --target-version py37 ${blackExclude} ${formatPaths}

flake8:
	flake8 ${flakeExclude} ${flakeOptions} ${flakeIgnore} ${formatPaths}

isort-check:
	isort \
		--case-sensitive \
		--check-only \
		--line-width 90 \
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

isort-reformat:
	isort \
		--case-sensitive \
		--line-width 90 \
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

test:
	make black-check
	make flake8
	make isort-check
	make mypy
	make pytest
