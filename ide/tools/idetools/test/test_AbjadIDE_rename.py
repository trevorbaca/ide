# -*- coding: utf-8 -*-
import ide
import os
import shutil
from abjad import *
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_rename_01():
    r'''Renames score directory.
    '''

    path_100_outer = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'example_score_100',
        )
    path_100_inner = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'example_score_100',
        'example_score_100',
        )
    path_101_outer = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'example_score_101',
        )
    path_101_inner = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'example_score_101',
        'example_score_101',
        )

    paths = (
        path_100_outer,
        path_100_inner,
        path_101_outer,
        path_101_inner,
        )
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    with systemtools.FilesystemState(remove=[path_100_outer, path_101_outer]):
        input_ = 'new example~score~100 q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(path_100_outer)
        assert os.path.exists(path_100_inner)
        title = 'Example Score 100'
        abjad_ide._add_metadatum(
            path_100_inner,
            'title',
            title,
            )
        input_ = 'ren Example~Score~100 example_score_101 y q'
        abjad_ide._start(input_=input_)
        assert not os.path.exists(path_100_outer)
        assert os.path.exists(path_101_outer)
        assert os.path.exists(path_101_inner)


def test_AbjadIDE_rename_02():
    r'''Renames material directory in score.
    '''

    old_path = os.path.join(
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

    paths = (
        old_path,
        new_path,
        )
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    with systemtools.FilesystemState(remove=[old_path, new_path]):
        input_ = 'red~example~score mm new test~material q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(old_path)
        input_ = 'red~example~score mm ren test~material new~test~material y q'
        abjad_ide._start(input_=input_)
        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)


def test_AbjadIDE_rename_03():
    r'''Renames segment directory inside score.
    '''

    old_path = os.path.join(
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

    paths = (
        old_path,
        new_path,
        )
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    with systemtools.FilesystemState(remove=[old_path, new_path]):
        abjad_ide._start(input_=new_input)
        assert os.path.exists(old_path)
        abjad_ide._start(input_=rename_input)
        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)


def test_AbjadIDE_rename_04():
    r'''Renames build subdirectory inside score.
    '''

    old_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        )
    assert os.path.isdir(old_path)
    new_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'standard-size',
        )

    rename_input = 'red~example~score bb ren letter-portrait standard-size y q'

    if os.path.exists(new_path):
        shutil.rmtree(new_path)

    with systemtools.FilesystemState(keep=[old_path], remove=[new_path]):
        assert os.path.exists(old_path)
        abjad_ide._start(input_=rename_input)
        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)


def test_AbjadIDE_rename_05():
    r'''Renames maker file inside score.
    '''

    old_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'tools',
        'NewMaker.py',
        )
    new_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'tools',
        'RenamedMaker.py',
        )

    new_input = 'red~example~score oo new NewMaker.py q'
    rename_input = 'red~example~score oo ren NewMaker.py RenamedMaker.py y q'

    paths = (
        old_path,
        new_path,
        )
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    with systemtools.FilesystemState(remove=[old_path, new_path]):
        abjad_ide._start(input_=new_input)
        assert os.path.exists(old_path)
        abjad_ide._start(input_=rename_input)
        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)


def test_AbjadIDE_rename_06():
    r'''Renames stylesheet inside score.
    '''

    old_path = os.path.join(
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

    paths = (
        old_path,
        new_path,
        )
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    with systemtools.FilesystemState(remove=[old_path, new_path]):
        abjad_ide._start(input_=new_input)
        assert os.path.exists(old_path)
        abjad_ide._start(input_=rename_input)
        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)