import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_lilypond_log_01():

    abjad_ide("lp q")
    transcript = abjad_ide.io.transcript
    path = abjad.Configuration().lilypond_log_file_path
    path = ide.Path(path)
    assert f"Editing {path.trim()} ..." in transcript
