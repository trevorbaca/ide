# -*- coding: utf-8 -*-
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_every_ly_01():
    r'''In materials directory.
    
    LilyPond files exist but PDFs do not exist.
    '''

    path = configuration.abjad_ide_example_scores_directory
    path = os.path.join(
        path,
        'red_example_score',
        'red_example_score',
        'materials',
        )
    package_names = (
        'magic_numbers',
        'pitch_range_inventory',
        'tempo_inventory',
        )
    ly_paths = [
        os.path.join(path, _, 'illustration.ly')
        for _ in package_names
        ]
    pdf_paths = [_.replace('.ly', '.pdf') for _ in ly_paths]
    paths = ly_paths + pdf_paths

    with systemtools.FilesystemState(keep=paths):
        for path in pdf_paths:
            os.remove(path)
        assert not any(os.path.exists(_) for _ in pdf_paths)
        input_ = 'red~example~score mm lyi* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert all(os.path.isfile(_) for _ in pdf_paths)
        assert systemtools.TestManager._compare_backup(pdf_paths)

    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
        message = 'Calling LilyPond on {} ...'
        message = message.format(abjad_ide._trim_path(ly_path))
        assert message in contents
        message = 'Writing {} ...'
        message = message.format(abjad_ide._trim_path(pdf_path))
        assert message in contents

    assert not 'Preserving' in contents
    assert 'Total time ' in contents


def test_AbjadIDE_interpret_every_ly_02():
    r'''In materials directory.

    LilyPond files and PDFs already exists.
    '''

    path = configuration.abjad_ide_example_scores_directory
    path = os.path.join(
        path,
        'red_example_score',
        'red_example_score',
        'materials',
        )
    package_names = (
        'magic_numbers',
        'pitch_range_inventory',
        'tempo_inventory',
        )
    ly_paths = [
        os.path.join(path, _, 'illustration.ly')
        for _ in package_names
        ]
    pdf_paths = [_.replace('.ly', '.pdf') for _ in ly_paths]
    paths = ly_paths + pdf_paths

    with systemtools.FilesystemState(keep=paths):
        # remove existing PDFs
        for pdf_path in pdf_paths:
            os.remove(pdf_path)
        # generate PDFs a first time
        input_ = 'red~example~score mm lyi* q'
        abjad_ide._start(input_=input_)
        # attempt (but fail) to generate PDFs a second time
        input_ = 'red~example~score mm lyi* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
        message = 'Calling LilyPond on {} ...'
        message = message.format(abjad_ide._trim_path(ly_path))
        assert message in contents
        message = 'Preserving {} ...'
        message = message.format(abjad_ide._trim_path(pdf_path))
        assert message in contents

    assert 'Total time ' in contents


def test_AbjadIDE_interpret_every_ly_03():
    r'''In segments directory.
    
    LilyPond files exist but PDFs do not exist.
    '''

    path = configuration.abjad_ide_example_scores_directory
    path = os.path.join(
        path,
        'red_example_score',
        'red_example_score',
        'segments',
        )
    package_names = (
        'segment_01',
        'segment_02',
        'segment_03',
        )
    ly_paths = [
        os.path.join(path, _, 'illustration.ly')
        for _ in package_names
        ]
    pdf_paths = [_.replace('.ly', '.pdf') for _ in ly_paths]
    paths = ly_paths + pdf_paths

    with systemtools.FilesystemState(keep=paths):
        for path in pdf_paths:
            os.remove(path)
        assert not any(os.path.exists(_) for _ in pdf_paths)
        input_ = 'red~example~score gg lyi* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert all(os.path.isfile(_) for _ in pdf_paths)
        assert systemtools.TestManager._compare_backup(pdf_paths)

    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
        message = 'Calling LilyPond on {} ...'
        message = message.format(abjad_ide._trim_path(ly_path))
        assert message in contents
        message = 'Writing {} ...'
        message = message.format(abjad_ide._trim_path(pdf_path))
        assert message in contents

    assert not 'Preserving' in contents
    assert 'Total time ' in contents


def test_AbjadIDE_interpret_every_ly_04():
    r'''In segments directory.

    LilyPond files and PDFs already exist.
    '''

    path = configuration.abjad_ide_example_scores_directory
    path = os.path.join(
        path,
        'red_example_score',
        'red_example_score',
        'segments',
        )
    package_names = (
        'segment_01',
        'segment_02',
        'segment_03',
        )
    ly_paths = [
        os.path.join(path, _, 'illustration.ly')
        for _ in package_names
        ]
    pdf_paths = [_.replace('.ly', '.pdf') for _ in ly_paths]
    paths = ly_paths + pdf_paths

    with systemtools.FilesystemState(keep=paths):
        # remove existing PDFs
        for pdf_path in pdf_paths:
            os.remove(pdf_path)
        # generate PDFs a first time
        input_ = 'red~example~score gg lyi* q'
        abjad_ide._start(input_=input_)
        # attempt (but fail) to generate PDFs a second time
        input_ = 'red~example~score gg lyi* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
        message = 'Calling LilyPond on {} ...'
        message = message.format(abjad_ide._trim_path(ly_path))
        assert message in contents
        message = 'Preserving {} ...'
        message = message.format(abjad_ide._trim_path(pdf_path))
        assert message in contents

    assert 'Total time ' in contents