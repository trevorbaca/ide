# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_Wrangler_copy_01():
    r'''Copies score package.
    '''

    pretty_path = os.path.join(
        configuration.composer_scores_directory,
        'pretty_example_score',
        )

    with systemtools.FilesystemState(remove=[pretty_path]):
        input_ = 'cp Red~Example~Score Pretty~Example~Score y q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(pretty_path)
        manager = ide.tools.idetools.PackageManager(
            path=pretty_path,
            session=abjad_ide._session,
            )
        title = 'Pretty Example Score'
        manager._add_metadatum(
            manager._session,
            manager._metadata_py_path,
            'title',
            title,
            )
        input_ = 'rm Pretty~Example~Score remove q'
        abjad_ide._run(input_=input_)
        assert not os.path.exists(pretty_path)


def test_Wrangler_copy_02():
    r'''Copies material package outside score.
    
    Partial test because we can't be sure any user score packages will be
    present. And because Score PackageManager allows copying into user score
    packages only (because copying into example score packages could pollute
    the example score packages).
    '''

    input_ = 'mm cp performer~inventory~(Red~Example~Score) <return> q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._session._transcript.contents

    titles = [
        'Abjad IDE - all score directories',
        'Abjad IDE - all materials directories',
        'Abjad IDE - all materials directories',
        'Abjad IDE - all materials directories',
        ]
    assert abjad_ide._session._transcript.titles == titles
    assert 'Select storehouse:' in contents


def test_Wrangler_copy_03():
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
        abjad_ide._run(input_=input_)
        contents = abjad_ide._session._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied_performer_inventory' in contents


def test_Wrangler_copy_04():
    r'''Includes preservation message in getter help.
    '''

    input_ = 'red~example~score m cp tempo~inventory ? foo n q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._session._transcript.contents
        
    string = 'Existing package name> tempo_inventory'
    assert string in contents
    string = 'Value must be string. Press <return> to preserve existing name.'
    assert string in contents


def test_Wrangler_copy_05():
    r'''Copies segment package outside score.
    
    Partial test because we can't be sure any user score packages will be
    present. And because Score PackageManager allows copying into user score 
    packges only (because copying into example score packages could pollute the
    example score packages).
    '''

    input_ = 'gg cp A~(Red~Example~Score) <return> q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._session._transcript.contents

    titles = [
        'Abjad IDE - all score directories',
        'Abjad IDE - all segments directories',
        'Abjad IDE - all segments directories',
        'Abjad IDE - all segments directories',
        ]
    assert abjad_ide._session._transcript.titles == titles
    assert 'Select storehouse:' in contents


def test_Wrangler_copy_06():
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
        abjad_ide._run(input_=input_)
        contents = abjad_ide._session._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied_segment_01' in contents


def test_Wrangler_copy_07():
    r'''Copies build file outside score.
    
    Partial test because we can't be sure any user score packages will be
    present. And because Score PackageManager allows copying into user score
    packages only (because copying into example score packages could pollute
    the example score packages).
    '''

    input_ = 'uu cp score.pdf~(Red~Example~Score) <return> q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._session._transcript.contents

    titles = [
        'Abjad IDE - all score directories',
        'Abjad IDE - all build directories',
        'Abjad IDE - all build directories',
        'Abjad IDE - all build directories',
        ]
    assert abjad_ide._session._transcript.titles == titles
    assert 'Select storehouse:' in contents


def test_Wrangler_copy_08():
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
        abjad_ide._run(input_=input_)
        contents = abjad_ide._session._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied-score.pdf' in contents