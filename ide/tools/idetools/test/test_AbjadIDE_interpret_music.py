import abjad
import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_interpret_music_01():

    ly_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'music.ly',
        )
    pdf_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        'music.pdf',
        )

    with ide.Test(keep=[ly_path]):
        if pdf_path.exists():
            pdf_path.unlink()
        assert not pdf_path.exists()
        input_ = 'red~score bb letter mi q'
        abjad_ide._start(input_=input_)
        assert pdf_path.is_file()
        assert abjad.TestManager._compare_backup(ly_path)
        contents = abjad_ide._io_manager._transcript.contents

    assert 'Calling LilyPond on' in contents
    assert 'Writing' in contents
