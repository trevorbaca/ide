# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_copy_01():
    r'''Copies example score package into composer scores directory.

    (No test provided to copy into Abjad IDE example scores directory
    because copying into Abjad IDE example scores directory not supported.)
    '''

    pretty_path = os.path.join(
        configuration.composer_scores_directory,
        'pretty_example_score',
        )
    inner_pretty_path = os.path.join(
        pretty_path,
        'pretty_example_score',
        )

    with systemtools.FilesystemState(remove=[pretty_path]):
        input_ = 'cp Red~Example~Score Pretty~Example~Score y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.exists(pretty_path)
        assert os.path.exists(inner_pretty_path)
        title = 'Pretty Example Score'
        abjad_ide._add_metadatum(
            inner_pretty_path,
            'title',
            title,
            )
        input_ = 'rm Pretty~Example~Score remove q'
        abjad_ide._run_main_menu(input_=input_)
        assert not os.path.exists(pretty_path)


def test_AbjadIDE_copy_02():
    r'''Copies material package in score.
    '''

    source_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'performer_inventory',
        )
    target_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'copied_performer_inventory',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'red~example~score m cp'
        input_ += ' performer~inventory copied~performer~inventory y q'
        abjad_ide._run_main_menu(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied_performer_inventory' in contents


def test_AbjadIDE_copy_03():
    r'''Includes preservation message in getter help.
    '''

    input_ = 'red~example~score m cp tempo~inventory ? foo n q'
    abjad_ide._run_main_menu(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
        
    string = 'Existing package name> tempo_inventory'
    assert string in contents
    string = 'Value must be string. Press <return> to preserve existing name.'
    assert string in contents


def test_AbjadIDE_copy_04():
    r'''Copies segment package in score.
    '''

    source_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    target_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'copied_segment_01',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'red~example~score g cp'
        input_ += ' A copied_segment_01 y q'
        abjad_ide._run_main_menu(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied_segment_01' in contents


def test_AbjadIDE_copy_05():
    r'''Copies build file in score.
    '''

    source_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'score.pdf',
        )
    target_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'copied-score.pdf',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'red~example~score u cp'
        input_ += ' score.pdf copied-score.pdf y q'
        abjad_ide._run_main_menu(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied-score.pdf' in contents


def test_AbjadIDE_copy_06():
    r'''Copies maker file in score.
    '''

    source_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'makers',
        'ScoreTemplate.py',
        )
    target_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'makers',
        'CopiedScoreTemplate.py',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'red~example~score k cp'
        input_ += ' ScoreTemplate.py CopiedScoreTemplate.py y q'
        abjad_ide._run_main_menu(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'CopiedScoreTemplate.py' in contents


def test_AbjadIDE_copy_07():
    r'''Copies stylesheet in score.
    '''

    source_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'stylesheets',
        'stylesheet.ily',
        )
    target_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'stylesheets',
        'copied-stylesheet.ily',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'red~example~score y cp'
        input_ += ' stylesheet.ily copied-stylesheet.ily y q'
        abjad_ide._run_main_menu(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied-stylesheet.ily' in contents