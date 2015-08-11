# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Menu__change_input_to_directive_01():
    r'''Works with accented characters.
    '''

    input_ = 'étude q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    string = 'Étude Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_02():
    r'''Works without accented characters.
    '''

    input_ = 'etude q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    string = 'Étude Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_03():
    r'''Works with mixed case.
    '''

    input_ = 'Red~example~score q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    string = 'Red Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_04():
    r'''Works with mixed case.
    '''

    input_ = 'red~Example~score q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    string = 'Red Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_05():
    r'''Works with mixed case.
    '''

    input_ = 'red~example~Score q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    string = 'Red Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_06():
    r'''Works with mixed case.
    '''

    input_ = 'RED~EXAMPLE~SCORE q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    string = 'Red Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_07():
    r'''Material that is list of numbers does not aliases numeric assets entry.

    The '1' in the input below is correctly interpret as the __init__.py file,
    assigned the number 1. in the menu section; this is not alises by the
    presence of the number 1 in the series of magic numbers itself:
    1, 3, 4, 7, ....
    '''

    input_ = 'red~example~score m magic~numbers 1 q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file