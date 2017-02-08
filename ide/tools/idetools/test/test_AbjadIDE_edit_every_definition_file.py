# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_edit_every_definition_file_01():
    r'''Edits every material definition.
    '''

    input_ = 'red~example~score mm df* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    package_names = [
        'magic_numbers',
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ]
    paths = []
    for package_name in package_names:
        path = os.path.join(
            configuration.abjad_ide_example_scores_directory,
            'red_example_score',
            'red_example_score',
            'materials',
            package_name,
            'definition.py',
            )
        paths.append(path)

    assert abjad_ide._session._attempted_to_open_file
    for path in paths:
        message = 'Opening {} ...'
        message = message.format(abjad_ide._trim_path(path))
        assert message in contents


def test_AbjadIDE_edit_every_definition_file_02():
    r'''Edits every segment definition.
    '''

    input_ = 'red~example~score gg df* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    package_names = [
        'segment_01',
        'segment_02',
        'segment_03',
        ]
    paths = []
    for package_name in package_names:
        path = os.path.join(
            configuration.abjad_ide_example_scores_directory,
            'red_example_score',
            'red_example_score',
            'segments',
            package_name,
            'definition.py',
            )
        paths.append(path)

    assert abjad_ide._session._attempted_to_open_file
    for path in paths:
        message = 'Opening {} ...'
        message = message.format(abjad_ide._trim_path(path))
        assert message in contents
