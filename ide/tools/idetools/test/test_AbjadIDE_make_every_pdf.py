# -*- coding: utf-8 -*-
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_make_every_pdf_01():
    r'''In materials directory when neither LilyPond files nor PDFs exist.
    '''

    path = configuration.abjad_ide_example_scores_directory
    path = os.path.join(
        path,
        'red_example_score',
        'red_example_score',
        'materials',
        )
    # only this package has an illustrate file
    package_names = (
        'magic_numbers',
        )
    ly_paths = [
        os.path.join(path, _, 'illustration.ly')
        for _ in package_names
        ]
    pdf_paths = [_.replace('.ly', '.pdf') for _ in ly_paths]
    paths = ly_paths + pdf_paths

    with systemtools.FilesystemState(keep=paths):
        for path in paths:
            os.remove(path)
        assert not any(os.path.exists(_) for _ in paths)
        input_ = 'red~example~score mm pdfm* y q'
        abjad_ide._start(input_=input_)
        assert all(os.path.isfile(_) for _ in paths)
        assert systemtools.TestManager._compare_backup(pdf_paths)

    contents = abjad_ide._io_manager._transcript.contents
    for path in paths:
        assert abjad_ide._trim_path(path) in contents

    assert 'Will illustrate ...' in contents
    assert 'INPUT:' in contents
    assert 'OUTPUT:' in contents
    # TODO: make this messaging work
    #assert 'Writing' in contents


def test_AbjadIDE_make_every_pdf_02():
    r'''In segments directory when neither LilyPond files nor PDFs exist.
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
        for path in paths:
            os.remove(path)
        assert not any(os.path.exists(_) for _ in paths)
        input_ = 'red~example~score gg pdfm* y q'
        abjad_ide._start(input_=input_)
        assert all(os.path.isfile(_) for _ in paths)
        assert systemtools.TestManager._compare_backup(pdf_paths)

    contents = abjad_ide._io_manager._transcript.contents
    for path in paths:
        assert abjad_ide._trim_path(path) in contents

    assert 'Will illustrate ...' in contents
    assert 'INPUT:' in contents
    assert 'OUTPUT:' in contents
    assert 'Writing' in contents


def test_AbjadIDE_make_every_pdf_03():
    r'''In segments directory when PDFs already exist.
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
        input_ = 'red~example~score gg pdfm* y q'
        abjad_ide._start(input_=input_)
        # attempt (but fail) to generate PDFs a second time
        input_ = 'red~example~score gg pdfm* y q'
        abjad_ide._start(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    for path in paths:
        assert abjad_ide._trim_path(path) in contents

    assert 'Will illustrate ...' in contents
    assert 'INPUT:' in contents
    assert 'OUTPUT:' in contents
    assert 'Preserving' in contents