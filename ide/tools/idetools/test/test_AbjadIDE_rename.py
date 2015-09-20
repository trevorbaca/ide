# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_rename_01():
    r'''Renames score package.
    '''

    path_100_outer = os.path.join(
        configuration.composer_scores_directory,
        'example_score_100',
        )
    path_100_inner = os.path.join(
        configuration.composer_scores_directory,
        'example_score_100',
        'example_score_100',
        )
    path_101_outer = os.path.join(
        configuration.composer_scores_directory,
        'example_score_101',
        )
    path_101_inner = os.path.join(
        configuration.composer_scores_directory,
        'example_score_101',
        'example_score_101',
        )

    with systemtools.FilesystemState(remove=[path_100_outer, path_101_outer]):
        input_ = 'new example~score~100 q'
        abjad_ide._start_abjad_ide(input_=input_)
        assert os.path.exists(path_100_outer)
        assert os.path.exists(path_100_inner)
        title = 'Example Score 100'
        abjad_ide._add_metadatum(
            path_100_inner,
            'title',
            title,
            )
        input_ = 'ren Example~Score~100 example_score_101 y q'
        abjad_ide._start_abjad_ide(input_=input_)
        assert not os.path.exists(path_100_outer)
        assert os.path.exists(path_101_outer)
        assert os.path.exists(path_101_inner)


def test_AbjadIDE_rename_02():
    r'''Renames material package in score.
    '''

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'test_material',
        )
    new_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'new_test_material',
        )

    with systemtools.FilesystemState(remove=[path, new_path]):
        input_ = 'red~example~score mm new test~material q'
        abjad_ide._start_abjad_ide(input_=input_)
        assert os.path.exists(path)
        input_ = 'red~example~score mm ren test~material new~test~material y q'
        abjad_ide._start_abjad_ide(input_=input_)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)


def test_AbjadIDE_rename_03():
    r'''Renames segment package inside score.
    '''

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_04',
        )
    new_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'renamed_segment_04',
        )

    new_input = 'red~example~score gg new segment~04 q'
    rename_input = 'red~example~score gg ren segment~04 renamed_segment_04 y q'

    with systemtools.FilesystemState(remove=[path, new_path]):
        abjad_ide._start_abjad_ide(input_=new_input)
        assert os.path.exists(path)
        abjad_ide._start_abjad_ide(input_=rename_input)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)


def test_AbjadIDE_rename_04():
    r'''Renames build file inside score.
    '''

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'new-file.txt',
        )
    new_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'renamed-file.txt',
        )

    new_input = 'red~example~score bb new new-file.txt q'
    rename_input = 'red~example~score bb ren new-file.txt renamed-file.txt y q'

    with systemtools.FilesystemState(remove=[path, new_path]):
        abjad_ide._start_abjad_ide(input_=new_input)
        assert os.path.exists(path)
        abjad_ide._start_abjad_ide(input_=rename_input)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)


def test_AbjadIDE_rename_05():
    r'''Renames maker file inside score.
    '''

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'makers',
        'NewMaker.py',
        )
    new_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'makers',
        'RenamedMaker.py',
        )

    new_input = 'red~example~score kk new NewMaker.py q'
    rename_input = 'red~example~score kk ren NewMaker.py RenamedMaker.py y q'

    with systemtools.FilesystemState(remove=[path, new_path]):
        abjad_ide._start_abjad_ide(input_=new_input)
        assert os.path.exists(path)
        abjad_ide._start_abjad_ide(input_=rename_input)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)


def test_AbjadIDE_rename_06():
    r'''Renames stylesheet inside score.
    '''

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'stylesheets',
        'new-stylesheet.ily',
        )
    new_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'stylesheets',
        'renamed-stylesheet.ily',
        )

    new_input = 'red~example~score yy new new-stylesheet.ily q'
    rename_input = 'red~example~score yy ren new-stylesheet.ily'
    rename_input += ' renamed-stylesheet.ily y q'

    with systemtools.FilesystemState(remove=[path, new_path]):
        abjad_ide._start_abjad_ide(input_=new_input)
        assert os.path.exists(path)
        abjad_ide._start_abjad_ide(input_=rename_input)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)