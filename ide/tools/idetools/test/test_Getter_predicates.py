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

    assert Getter.is_identifier('foo_bar')
    assert Getter.is_identifier('FooBar')
    assert Getter.is_identifier('_foo_bar')
    assert Getter.is_identifier('__foo_bar')
    assert Getter.is_identifier('_')
    assert Getter.is_identifier('f')

    assert not Getter.is_boolean(None)
    assert not Getter.is_boolean('')
    assert not Getter.is_boolean('1')
    assert not Getter.is_boolean('foo_!')
    assert not Getter.is_boolean('foo_#')
    assert not Getter.is_boolean('foo_@')


def test_Getter_predicates_03():

    assert Getter.is_page_layout_unit('in')
    assert Getter.is_page_layout_unit('mm')
    assert Getter.is_page_layout_unit('cm')
    assert Getter.is_page_layout_unit('pt')
    assert Getter.is_page_layout_unit('pica')

    assert not Getter.is_page_layout_unit('foo')
    assert not Getter.is_page_layout_unit(None)
    assert not Getter.is_page_layout_unit(-1)
    assert not Getter.is_page_layout_unit(1)


def test_Getter_predicates_04():

    assert Getter.is_paper_dimension_string('8.5 x 11 in')
    assert Getter.is_paper_dimension_string('11 x 8.5 in')
    assert Getter.is_paper_dimension_string('11 x 17 in')
    assert Getter.is_paper_dimension_string('17 x 11 in')
    assert Getter.is_paper_dimension_string('210 x 297 mm')
    assert Getter.is_paper_dimension_string('297 x 210 mm')

    assert not Getter.is_paper_dimension_string('8.5 x 11')
    assert not Getter.is_paper_dimension_string('8.5x11')
    assert not Getter.is_paper_dimension_string('8.5x11in')
    assert not Getter.is_paper_dimension_string('A4')
    assert not Getter.is_paper_dimension_string('foo')
    assert not Getter.is_paper_dimension_string(None)
    assert not Getter.is_paper_dimension_string(-1)
    assert not Getter.is_paper_dimension_string(1)