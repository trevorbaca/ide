import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_make_pdf_01():
    r'''In material directory.

    Creates PDF and LilyPond files when none exists.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = os.path.join(segment_directory, 'illustration.ly')
    pdf_path = os.path.join(segment_directory, 'illustration.pdf')

    with abjad.FilesystemState(keep=[ly_path, pdf_path]):
        os.remove(ly_path)
        os.remove(pdf_path)
        input_ = 'red~example~score mm magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        assert abjad.TestManager._compare_backup(ly_path)
        assert abjad.TestManager._compare_backup(pdf_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Calling Python on' in contents
    assert 'Abjad runtime ' in contents
    assert 'LilyPond runtime ' in contents
    assert 'Total time ' in contents


def test_AbjadIDE_make_pdf_02():
    r'''In material directory.

    Removes .ly and .pdf files when they already exist.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = os.path.join(segment_directory, 'illustration.ly')
    pdf_path = os.path.join(segment_directory, 'illustration.pdf')

    with abjad.FilesystemState(keep=[ly_path, pdf_path]):
        assert os.path.exists(ly_path)
        assert os.path.exists(pdf_path)
        input_ = 'red~example~score mm magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Calling Python on' in contents
    assert 'Removing' in contents
    assert abjad_ide._trim_path(ly_path) in contents
    assert abjad_ide._trim_path(pdf_path) in contents
    assert 'Abjad runtime ' in contents
    assert 'LilyPond runtime ' in contents
    assert 'Total time ' in contents


def test_AbjadIDE_make_pdf_03():
    r'''In segment directory.

    Creates PDF and LilyPond files when none exists.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    ly_path = os.path.join(segment_directory, 'illustration.ly')
    pdf_path = os.path.join(segment_directory, 'illustration.pdf')
    illustrate_file_path = os.path.join(
        segment_directory,
        '__illustrate__.py',
        )

    with abjad.FilesystemState(keep=[ly_path, pdf_path]):
        os.remove(ly_path)
        os.remove(pdf_path)
        input_ = 'red~example~score gg A pdfm q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        assert abjad.TestManager._compare_backup(ly_path)
        assert abjad.TestManager._compare_backup(pdf_path)

    message = 'Calling Python on {} ...'
    message = message.format(abjad_ide._trim_path(illustrate_file_path))
    assert message in contents
    message = 'Opening {} ...'
    message = message.format(abjad_ide._trim_path(pdf_path))
    assert message in contents
    assert 'Total time ' in contents
