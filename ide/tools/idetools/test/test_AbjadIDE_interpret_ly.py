import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_ly_01():
    r'''In material directory.

    LilyPond file exists but PDF does not exist.
    '''

    ly_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'tempi',
        'illustration.ly',
        )
    pdf_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'tempi',
        'illustration.pdf',
        )

    with abjad.FilesystemState(keep=[ly_path, pdf_path]):
        pdf_path.unlink()
        assert not pdf_path.exists()
        input_ = 'red~example~score mm tempi lyi q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert pdf_path.is_file()
        assert abjad.TestManager._compare_backup(pdf_path)

    message = 'Calling LilyPond on {!s} ...'
    message = message.format(abjad_ide._trim(ly_path))
    message = 'Writing {!s} ...'
    message = message.format(abjad_ide._trim(pdf_path))
    assert message in contents


def test_AbjadIDE_interpret_ly_02():
    r'''In segment directory.

    LilyPond file exists but PDF does not exist.
    '''

    ly_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        'illustration.ly',
        )
    pdf_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        'illustration.pdf',
        )

    with abjad.FilesystemState(keep=[ly_path, pdf_path]):
        pdf_path.unlink()
        assert not pdf_path.exists()
        input_ = 'red~example~score gg A lyi q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert pdf_path.is_file()
        assert abjad.TestManager._compare_backup(pdf_path)

    message = 'Calling LilyPond on {!s} ...'
    message = message.format(abjad_ide._trim(ly_path))
    message = 'Writing {!s} ...'
    message = message.format(abjad_ide._trim(pdf_path))
    assert message in contents
