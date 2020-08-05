import pytest

import abjad
import ide

pytest_plugins = ["helpers_namespace"]


@pytest.fixture(autouse=True)
def add_ide(doctest_namespace):
    doctest_namespace["ide"] = ide


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["abjad"] = abjad
