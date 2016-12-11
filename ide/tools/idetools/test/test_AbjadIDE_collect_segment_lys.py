# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_collect_segment_lys_01():
    r'''Build directory contains no LilyPond files.
    '''

    _segments_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        '_segments',
        )

    ly_names, ly_paths = [], []
    for number in ('01', '02', '03'):
        ly_name = 'segment-{}.ly'
        ly_name = ly_name.format(number)
        ly_names.append(ly_name)
        ly_path = os.path.join(_segments_directory, ly_name)
        ly_paths.append(ly_path)

    with abjad.systemtools.FilesystemState(keep=ly_paths):
        for ly_path in ly_paths:
            os.remove(ly_path)
        input_ = 'red~example~score bb lyc q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        for ly_path in ly_paths:
            assert os.path.isfile(ly_path)

    for ly_path in ly_paths:
        message = 'Writing {} ...'
        message = message.format(abjad_ide._trim_path(ly_path))
        assert message in contents


def test_AbjadIDE_collect_segment_lys_02():
    r'''Build directory contains LilyPond files.
    '''

    _segments_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        '_segments',
        )

    ly_names, ly_paths = [], []
    for number in ('01', '02', '03'):
        ly_name = 'segment-{}.ly'
        ly_name = ly_name.format(number)
        ly_names.append(ly_name)
        ly_path = os.path.join(_segments_directory, ly_name)
        ly_paths.append(ly_path)

    with abjad.systemtools.FilesystemState(keep=ly_paths):
        input_ = 'red~example~score bb lyc y q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    for ly_path in ly_paths:
        message = 'Preserving {} ...'
        message = message.format(abjad_ide._trim_path(ly_path))
        assert message in contents
