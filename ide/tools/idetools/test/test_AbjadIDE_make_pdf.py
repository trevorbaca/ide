import abjad
import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_pdf_01():
    r'''In material directory.
    '''

    segment_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'magic_numbers',
        )
    ly_path = pathlib.Path(segment_directory, 'illustration.ly')
    pdf_path = pathlib.Path(segment_directory, 'illustration.pdf')

    with ide.Test(keep=[ly_path]):
        ly_path.unlink()
        if pdf_path.exists():
            pdf_path.unlink()
        input_ = 'red~score mm magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        assert ly_path.is_file()
        assert pdf_path.is_file()
        assert abjad.TestManager._compare_backup(ly_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Calling Python on' in contents
    assert 'Abjad runtime ' in contents
    assert 'LilyPond runtime ' in contents
    assert 'Total time ' in contents


def test_AbjadIDE_make_pdf_02():
    r'''In material directory.
    '''

    segment_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'magic_numbers',
        )
    ly_path = pathlib.Path(segment_directory, 'illustration.ly')
    pdf_path = pathlib.Path(segment_directory, 'illustration.pdf')

    with ide.Test(keep=[ly_path]):
        assert ly_path.is_file()
        input_ = 'red~score mm magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        assert ly_path.is_file()
        assert abjad.TestManager._compare_backup(ly_path)
        assert pdf_path.is_file()

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Calling Python on' in contents
    assert 'Removing' in contents
    assert abjad_ide._trim(ly_path) in contents
    #assert abjad_ide._trim(pdf_path) in contents
    assert 'Abjad runtime ' in contents
    assert 'LilyPond runtime ' in contents
    assert 'Total time ' in contents


def test_AbjadIDE_make_pdf_03():
    r'''In segment directory.
    '''

    segment_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'segments',
        'segment_01',
        )
    ly_path = pathlib.Path(segment_directory, 'illustration.ly')
    pdf_path = pathlib.Path(segment_directory, 'illustration.pdf')
    illustrate_file_path = pathlib.Path(
        segment_directory,
        '__illustrate__.py',
        )

    with ide.Test(keep=[ly_path]):
        ly_path.unlink()
        if pdf_path.exists():
            pdf_path.unlink()
        input_ = 'red~score gg A pdfm q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert ly_path.is_file()
        assert pdf_path.is_file()
        assert abjad.TestManager._compare_backup(ly_path)

    message = 'Calling Python on {} ...'
    message = message.format(abjad_ide._trim(illustrate_file_path))
    assert message in contents
    message = 'Opening {} ...'
    message = message.format(abjad_ide._trim(pdf_path))
    assert message in contents
    assert 'Total time ' in contents
