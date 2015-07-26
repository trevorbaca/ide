# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_PackageWrangler_copy_package_01():
    r'''Copies score package.
    '''

    pretty_path = os.path.join(
        abjad_ide._configuration.user_score_packages_directory,
        'pretty_example_score',
        )

    with systemtools.FilesystemState(remove=[pretty_path]):
        input_ = 'cp Red~Example~Score Pretty~Example~Score y q'
        abjad_ide._run(input_=input_)
        assert os.path.exists(pretty_path)
        manager = ide.idetools.ScorePackageManager
        manager = manager(path=pretty_path, session=abjad_ide._session)
        title = 'Pretty Example Score'
        manager._add_metadatum('title', title)
        input_ = 'rm Pretty~Example~Score remove q'
        abjad_ide._run(input_=input_)
        assert not os.path.exists(pretty_path)


def test_PackageWrangler_copy_package_02():
    r'''Copies material package outside score.
    
    Partial test because we can't be sure any user score packages will be
    present. And because Score PackageManager allows copying into user score 
    packages only (because copying into example score packages could pollute the
    example score packages).
    '''

    input_ = 'mm cp performer~inventory~(Red~Example~Score) q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - materials depot',
        'Abjad IDE - materials depot',
        ]
    assert abjad_ide._transcript.titles == titles
    assert 'Select storehouse:' in contents


def test_PackageWrangler_copy_package_03():
    r'''Copies material package in score.
    '''

    source_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'performer_inventory',
        )
    target_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'copied_performer_inventory',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'red~example~score m cp'
        input_ += ' performer~inventory copied~performer~inventory y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied_performer_inventory' in contents


def test_PackageWrangler_copy_package_04():
    r'''Includes preservation message in getter help.
    '''

    input_ = 'red~example~score m cp tempo~inventory ? q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents
        
    string = 'Existing material package name> tempo_inventory'
    assert string in contents
    string = 'Value must be string. Press <return> to preserve existing name.'
    assert string in contents


def test_PackageWrangler_copy_package_05():
    r'''Copies segment package outside score.
    
    Partial test because we can't be sure any user score packages will be
    present. And because Score PackageManager allows copying into user score 
    packges only (because copying into example score packages could pollute the
    example score packages).
    '''

    input_ = 'gg cp A~(Red~Example~Score) q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments depot',
        'Abjad IDE - segments depot',
        ]
    assert abjad_ide._transcript.titles == titles
    assert 'Select storehouse:' in contents


def test_PackageWrangler_copy_package_06():
    r'''Copies segment package in score.
    '''

    source_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    target_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'copied_segment_01',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'red~example~score g cp'
        input_ += ' A copied_segment_01 y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied_segment_01' in contents