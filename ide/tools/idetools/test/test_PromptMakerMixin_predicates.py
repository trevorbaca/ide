# -*- encoding: utf-8 -*-
from ide.tools.idetools import PromptMakerMixin


def test_PromptMakerMixin_01():

    assert PromptMakerMixin.is_boolean(True)
    assert PromptMakerMixin.is_boolean(False)

    assert not PromptMakerMixin.is_boolean(None)
    assert not PromptMakerMixin.is_boolean('')
    assert not PromptMakerMixin.is_boolean(0)
    assert not PromptMakerMixin.is_boolean(1)


def test_PromptMakerMixin_02():

    assert PromptMakerMixin.is_identifier('foo_bar')
    assert PromptMakerMixin.is_identifier('FooBar')
    assert PromptMakerMixin.is_identifier('_foo_bar')
    assert PromptMakerMixin.is_identifier('__foo_bar')
    assert PromptMakerMixin.is_identifier('_')
    assert PromptMakerMixin.is_identifier('f')

    assert not PromptMakerMixin.is_boolean(None)
    assert not PromptMakerMixin.is_boolean('')
    assert not PromptMakerMixin.is_boolean('1')
    assert not PromptMakerMixin.is_boolean('foo_!')
    assert not PromptMakerMixin.is_boolean('foo_#')
    assert not PromptMakerMixin.is_boolean('foo_@')


def test_PromptMakerMixin_03():

    assert PromptMakerMixin.is_page_layout_unit('in')
    assert PromptMakerMixin.is_page_layout_unit('mm')
    assert PromptMakerMixin.is_page_layout_unit('cm')
    assert PromptMakerMixin.is_page_layout_unit('pt')
    assert PromptMakerMixin.is_page_layout_unit('pica')

    assert not PromptMakerMixin.is_page_layout_unit('foo')
    assert not PromptMakerMixin.is_page_layout_unit(None)
    assert not PromptMakerMixin.is_page_layout_unit(-1)
    assert not PromptMakerMixin.is_page_layout_unit(1)


def test_PromptMakerMixin_04():

    assert PromptMakerMixin.is_paper_dimension_string('8.5 x 11 in')
    assert PromptMakerMixin.is_paper_dimension_string('11 x 8.5 in')
    assert PromptMakerMixin.is_paper_dimension_string('11 x 17 in')
    assert PromptMakerMixin.is_paper_dimension_string('17 x 11 in')
    assert PromptMakerMixin.is_paper_dimension_string('210 x 297 mm')
    assert PromptMakerMixin.is_paper_dimension_string('297 x 210 mm')

    assert not PromptMakerMixin.is_paper_dimension_string('8.5 x 11')
    assert not PromptMakerMixin.is_paper_dimension_string('8.5x11')
    assert not PromptMakerMixin.is_paper_dimension_string('8.5x11in')
    assert not PromptMakerMixin.is_paper_dimension_string('A4')
    assert not PromptMakerMixin.is_paper_dimension_string('foo')
    assert not PromptMakerMixin.is_paper_dimension_string(None)
    assert not PromptMakerMixin.is_paper_dimension_string(-1)
    assert not PromptMakerMixin.is_paper_dimension_string(1)