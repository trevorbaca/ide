# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_make_every_pdf_01():
    r'''In materials directory.
    
    Neither LilyPond files nor PDFs exist.
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

    with abjad.FilesystemState(keep=paths):
        for path in paths:
            os.remove(path)
        assert not any(os.path.exists(_) for _ in paths)
        input_ = 'red~example~score mm pdfm* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert all(os.path.isfile(_) for _ in paths)
        assert abjad.TestManager._compare_backup(pdf_paths)

    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
        message = 'Writing {} ...'
        message = message.format(abjad_ide._trim_path(ly_path))
        assert message in contents
        message = 'Writing {} ...'
        message = message.format(abjad_ide._trim_path(pdf_path))
        assert message in contents

    assert not 'Opening' in contents
    assert 'Total time ' in contents


def test_AbjadIDE_make_every_pdf_02():
    r'''In segments directory.
    
    Neither LilyPond files nor PDFs exist.
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

    with abjad.FilesystemState(keep=paths):
        for path in paths:
            os.remove(path)
        assert not any(os.path.exists(_) for _ in paths)
        input_ = 'red~example~score gg pdfm* q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert all(os.path.isfile(_) for _ in paths)
        assert abjad.TestManager._compare_backup(pdf_paths)

#    for ly_path, pdf_path in zip(ly_paths, pdf_paths):
#        message = 'Writing {} ...'
#        message = message.format(abjad_ide._trim_path(ly_path))
#        assert message in contents
#        message = 'Writing {} ...'
#        message = message.format(abjad_ide._trim_path(pdf_path))
#        assert message in contents

    assert not 'Opening' in contents
    assert 'Total time ' in contents
