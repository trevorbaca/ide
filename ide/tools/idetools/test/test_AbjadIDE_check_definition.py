# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_check_definition_01():
    r'''In material directory.
    '''

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        'definition.py',
        )

    input_ = 'red~example~score %magic dfk q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    message = '{} ... OK'
    message = message.format(abjad_ide._trim_path(path))
    assert message in contents
    assert 'Total time ' in contents


def test_AbjadIDE_check_definition_02():
    r'''In segment directory.
    '''

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        'definition.py',
        )

    input_ = 'red~example~score %A dfk q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    message = '{} ... OK'
    message = message.format(abjad_ide._trim_path(path))
    assert message in contents
    assert 'Total time ' in contents
