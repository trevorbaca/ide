blackExclude = --exclude='__metadata__.py|definition.py|layout.py'

black-check:
	black --check --diff ${blackExclude} --target-version=py38 .

black-reformat:
	black ${blackExclude} --target-version=py38 .

flakeIgnore = --ignore=E203,E266,E501,W503
flakeExclude := --exclude=__metadata__.py
flakeOptions = --isolated --max-line-length=88

flake8:
	flake8 ${flakeExclude} ${flakeIgnore} ${flakeOptions}

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
	--thirdparty=ply \
	--thirdparty=roman \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	.

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
	--thirdparty=ply \
	--thirdparty=roman \
	--thirdparty=uqbar \
	--trailing-comma \
	--use-parentheses \
	.

mypy:
	mypy .

project = ide

pytest:
	rm -Rf htmlcov
	pytest \
	--cov-config=.coveragerc \
	--cov-report=html \
	--cov-report=term \
	--cov=${project}/ \
	--durations=20 \
	.

pytest-x:
	rm -Rf htmlcov
	pytest \
	-x \
	--cov-config=.coveragerc \
	--cov-report=html \
	--cov-report=term \
	--cov=${project}/ \
	--durations=20 \
	.

reformat:
	make black-reformat
	make isort-reformat

check:
	make black-check
	make flake8
	make isort-check
	make mypy

test:
	make black-check
	make flake8
	make isort-check
	make mypy
	make pytest
