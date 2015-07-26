# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_PackageWrangler_check_every_package_01():
    r'''Checks every score package.
    '''

    lines = [
        'Étude Example Score (2013):',
        '    Top level (10 assets): OK',
        '    Build directory (1 files): OK',
        '    Distribution directory (0 files): OK',
        '    Makers directory (0 files): OK',
        '    Materials directory (0 packages): OK',
        '    Segments directory (0 packages): OK',
        '    Stylesheets directory (0 files): OK',
        'Red Example Score (2013):',
        '    Top level (10 assets): OK',
        '    Build directory (18 files): OK',
        '    Distribution directory (2 files): OK',
        '    Makers directory (2 files): OK',
        '    Materials directory (5 packages):',
        '        Magic numbers: OK',
        '        Performer inventory: OK',
        '        Pitch range inventory: OK',
        '        Tempo inventory: OK',
        '        Time signatures: OK',
        '    Segments directory (3 packages):',
        '        A: OK',
        '        B: OK',
        '        C: OK',
        '    Stylesheets directory (4 files): OK',
        ]

    input_ = 'ck* y n q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents
    for line in lines:
        assert line in contents


def test_PackageWrangler_check_every_package_02():
    r'''Supplies missing build directory.
    '''

    score_directory = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        )
    build_directory = os.path.join(score_directory, 'build')
        
    with systemtools.FilesystemState(keep=[build_directory]):
        shutil.rmtree(build_directory)
        input_ = 'ck* y y q'
        abjad_ide._run(input_=input_)
        assert os.path.isdir(build_directory)


def test_PackageWrangler_check_every_package_03():
    r'''Supplies missing initializer.
    '''

    segment_directory = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_02',
        )
    initializer = os.path.join(segment_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[initializer]):
        os.remove(initializer)
        input_ = 'ck* y y q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(initializer)


def test_MaterialPackageWrangler_check_every_package_01():
    r'''Checks every material package in score.
    '''

    lines = [
        'Materials directory (5 packages)',
        'Magic numbers: OK',
        'Performer inventory: OK',
        'Pitch range inventory: OK',
        'Tempo inventory: OK',
        'Time signatures: OK',
        ]

    input_ = 'red~example~score m ck* y n q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents
    for line in lines:
        assert line in contents


def test_MaterialPackageWrangler_check_every_package_02():
    r'''Checks every material package everywhere.
    '''

    lines = [
        'Magic numbers (Red Example Score): OK',
        'Performer inventory (Red Example Score): OK',
        'Pitch range inventory (Red Example Score): OK',
        'Tempo inventory (Red Example Score): OK',
        'Time signatures (Red Example Score): OK',
        ]

    input_ = 'mm ck* y n q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents
    for line in lines:
        assert line in contents

def test_MaterialPackageWrangler_check_every_package_03():
    r'''Supplies missing initializer.
    '''

    material_directory = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'tempo_inventory',
        )
    initializer = os.path.join(material_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[initializer]):
        os.remove(initializer)
        input_ = 'red~example~score m ck* y y q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(initializer)


def test_SegmentPackageWrangler_check_every_package_01():
    r'''Checks every segment package in score.
    '''

    lines = [
        'Segments directory (3 packages)',
        'A: OK',
        'B: OK',
        'C: OK',
        ]

    input_ = 'red~example~score g ck* y n q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents
    for line in lines:
        assert line in contents


def test_SegmentPackageWrangler_check_every_package_02():
    r'''Checks every segment package everywhere.
    '''

    lines = [
        'A (Red Example Score): OK',
        'B (Red Example Score): OK',
        'C (Red Example Score): OK',
        ]

    input_ = 'gg ck* y n q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents
    for line in lines:
        assert line in contents


def test_SegmentPackageWrangler_check_every_package_03():
    r'''Supplies missing initializer.
    '''

    segment_directory = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    initializer = os.path.join(segment_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[initializer]):
        os.remove(initializer)
        input_ = 'red~example~score g ck* y y q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(initializer)