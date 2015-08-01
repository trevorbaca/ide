# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_PackageManager_check_package_01():
    r'''Displays problems only in material package.
    '''

    input_ = 'red~example~score m tempo~inventory ck y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._session._transcript.contents

    assert 'Top level (5 assets): OK' in contents
    assert 'found' not in contents
    assert 'missing' not in contents


def test_PackageManager_check_package_02():
    r'''Displays everything in material package.
    '''

    input_ = 'red~example~score m tempo~inventory ck n q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._session._transcript.contents

    lines = [
        '3 of 3 required files found:',
        '2 optional files found:',
        ]
    for line in lines:
        assert line in contents
    assert 'No problem assets found.' not in contents


def test_PackageManager_check_package_03():
    r'''Supplies missing file in material package.
    '''

    material_directory = os.path.join(
        abjad_ide._session._configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'tempo_inventory',
        )
    initializer = os.path.join(material_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[initializer]):
        os.remove(initializer)
        input_ = 'red~example~score m tempo~inventory ck y y q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(initializer)


def test_PackageManager_check_package_04():
    r'''Reports problems only in segment package.
    '''

    segment_directory = os.path.join(
        abjad_ide._session._configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_02',
        )
    initializer = os.path.join(segment_directory, '__init__.py')

    with systemtools.FilesystemState(keep=[initializer]):
        os.remove(initializer)
        input_ = 'red~example~score g B ck y n q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._session._transcript.contents

    lines = [
        '1 of 3 required files missing:',
        ]
    for line in lines:
        assert line in contents
    assert 'optional directories' not in contents
    assert 'optional files' not in contents


def test_PackageManager_check_package_05():
    r'''Reports everything in segment package.
    '''

    segment_directory = os.path.join(
        abjad_ide._session._configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_02',
        )
    initializer = os.path.join(segment_directory, '__init__.py')

    with systemtools.FilesystemState(keep=[initializer]):
        os.remove(initializer)
        input_ = 'red~example~score g B ck n n q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._session._transcript.contents

    lines = [
        '1 of 3 required files missing:',
        '2 optional files found:',
        ]
    for line in lines:
        assert line in contents


def test_PackageManager_check_package_06():
    r'''Supplies missing file in segment package.
    '''

    segment_directory = os.path.join(
        abjad_ide._session._configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    initializer = os.path.join(segment_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[initializer]):
        os.remove(initializer)
        input_ = 'red~example~score g A ck y y q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(initializer)


def test_PackageManager_check_package_07():
    r'''Reports problems only in score package.
    '''

    input_ = 'red~example~score ck y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._session._transcript.contents

    lines = [
        'Build directory (18 files): OK',
        'Distribution directory (2 files): OK',
        'Makers directory (2 files): OK',
        'Materials directory (5 packages):',
        'Segments directory (3 packages):',
        'Stylesheets directory (4 files): OK',
        ]
    for line in lines:
        assert line in contents
    assert 'found' not in contents


def test_PackageManager_check_package_08():
    r'''Reports everything in score package.
    '''

    input_ = 'red~example~score ck n q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._session._transcript.contents

    lines = [
        '6 of 6 required directories found:',
        '3 of 3 required files found:',
        '2 optional directories found:',
        ]
    for line in lines:
        assert line in contents


def test_PackageManager_check_package_09():
    r'''Reports unrecognized file in score package.
    '''

    extra_file = os.path.join(
        abjad_ide._session._configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'extra_file.txt',
        )

    with systemtools.FilesystemState(remove=[extra_file]):
        with open(extra_file, 'w') as file_pointer:
            file_pointer.write('')
        input_ = 'red~example~score ck y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._session._transcript.contents

    line = '1 unrecognized file found:'
    assert line in contents


def test_PackageManager_check_package_10():
    r'''Supplies missing directory in score package.
    '''

    score_directory = os.path.join(
        abjad_ide._session._configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        )
    build_directory = os.path.join(score_directory, 'build')
        
    with systemtools.FilesystemState(keep=[build_directory]):
        shutil.rmtree(build_directory)
        input_ = 'red~example~score ck y y q'
        abjad_ide._run(input_=input_)
        assert os.path.isdir(build_directory)


def test_PackageManager_check_package_11():
    r'''Supplies missing file in subdirectory.
    '''

    segment_directory = os.path.join(
        abjad_ide._session._configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_02',
        )
    initializer = os.path.join(segment_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[initializer]):
        os.remove(initializer)
        input_ = 'red~example~score ck y y q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(initializer)