# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_check_every_package_01():
    r'''Works in score.
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
    r'''Works in library.
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
    r'''Supplies missing directory and missing file.
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