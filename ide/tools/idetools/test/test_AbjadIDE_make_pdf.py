import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_make_pdf_01():
    r'''In material directory.

    Creates PDF and LilyPond files when none exists.
    '''

    segment_directory = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = pathlib.Path(segment_directory, 'illustration.ly')
    pdf_path = pathlib.Path(segment_directory, 'illustration.pdf')

    with abjad.FilesystemState(keep=[ly_path, pdf_path]):
        ly_path.unlink()
        pdf_path.unlink()
        input_ = 'red~example~score mm magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        assert ly_path.is_file()
        assert pdf_path.is_file()
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

    segment_directory = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = pathlib.Path(segment_directory, 'illustration.ly')
    pdf_path = pathlib.Path(segment_directory, 'illustration.pdf')

    with abjad.FilesystemState(keep=[ly_path, pdf_path]):
        assert ly_path.is_file()
        assert pdf_path.is_file()
        input_ = 'red~example~score mm magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        assert ly_path.is_file()
        assert pdf_path.is_file()

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Calling Python on' in contents
    assert 'Removing' in contents
    assert str(abjad_ide._trim(ly_path)) in contents
    assert str(abjad_ide._trim(pdf_path)) in contents
    assert 'Abjad runtime ' in contents
    assert 'LilyPond runtime ' in contents
    assert 'Total time ' in contents


def test_AbjadIDE_make_pdf_03():
    r'''In segment directory.

    Creates PDF and LilyPond files when none exists.
    '''

    segment_directory = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    ly_path = pathlib.Path(segment_directory, 'illustration.ly')
    pdf_path = pathlib.Path(segment_directory, 'illustration.pdf')
    illustrate_file_path = pathlib.Path(
        segment_directory,
        '__illustrate__.py',
        )

    with abjad.FilesystemState(keep=[ly_path, pdf_path]):
        ly_path.unlink()
        pdf_path.unlink()
        input_ = 'red~example~score gg A pdfm q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert ly_path.is_file()
        assert pdf_path.is_file()
        assert abjad.TestManager._compare_backup(ly_path)
        assert abjad.TestManager._compare_backup(pdf_path)

    message = 'Calling Python on {!s} ...'
    message = message.format(abjad_ide._trim(illustrate_file_path))
    assert message in contents
    message = 'Opening {!s} ...'
    message = message.format(abjad_ide._trim(pdf_path))
    assert message in contents
    assert 'Total time ' in contents
