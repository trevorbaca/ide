# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_Menu__display_available_commands_01():

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = '? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'help' in contents
    assert 'new score' in contents


def test_Menu__display_available_commands_02():
    r'''Hidden menu persists after junk.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    abjad_ide._session._allow_unknown_command_during_test = True
    input_ = '? asdf q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - scores - available commands',
        ]
    assert abjad_ide._transcript.titles == titles


def test_Menu__display_available_commands_03():
    r'''Hidden menu persists after LilyPond log.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = '? ll q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - scores - available commands',
        ]
    assert abjad_ide._transcript.titles == titles


def test_Menu__display_available_commands_04():
    r'''Hidden menu is available when managing score package.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score ? q'
    abjad_ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - available commands',
        ]
    assert abjad_ide._transcript.titles == titles