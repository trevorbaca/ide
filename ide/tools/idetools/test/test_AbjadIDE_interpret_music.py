import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_music_01():
    r'''Makes music.pdf when music.pdf doesn't yet exist.
    '''

    ly_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'music.ly',
        )
    pdf_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'music.pdf',
        )

    with abjad.FilesystemState(keep=[ly_path, pdf_path]):
        pdf_path.unlink()
        assert not pdf_path.exists()
        input_ = 'red~example~score bb letter-portrait mi q'
        abjad_ide._start(input_=input_)
        assert pdf_path.is_file()
        assert abjad.TestManager._compare_backup(ly_path)
        assert abjad.TestManager._compare_backup(pdf_path)


def test_AbjadIDE_interpret_music_02():
    r'''Preserves music.pdf when music.candidate.pdf compares
    equal to music.pdf.
    '''

    ly_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'music.ly',
        )
    pdf_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'music.pdf',
        )

    with abjad.FilesystemState(keep=[ly_path, pdf_path]):
        # remove existing PDF
        pdf_path.unlink()
        # generate PDF a first time
        input_ = 'red~example~score bb letter-portrait mi q'
        abjad_ide._start(input_=input_)
        # attempt (but fail) to generate PDF a second time
        input_ = 'red~example~score bb letter-portrait mi q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    assert 'Preserving' in contents
