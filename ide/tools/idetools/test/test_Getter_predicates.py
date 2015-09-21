# -*- coding: utf-8 -*-
from ide.tools.idetools import Getter


def test_Getter_predicates_01():

    assert Getter.is_boolean(True)
    assert Getter.is_boolean(False)

    assert not Getter.is_boolean(None)
    assert not Getter.is_boolean('')
    assert not Getter.is_boolean(0)
    assert not Getter.is_boolean(1)


def test_Getter_predicates_02():

    assert not Getter.is_boolean(None)
    assert not Getter.is_boolean('')
    assert not Getter.is_boolean('1')
    assert not Getter.is_boolean('foo_!')
    assert not Getter.is_boolean('foo_#')
    assert not Getter.is_boolean('foo_@')