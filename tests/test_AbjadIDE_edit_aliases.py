import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_aliases_01():

    abjad_ide("red gg al q")
    transcript = abjad_ide.io.transcript
    path = abjad.Path(abjad_ide.configuration.aliases_file_path)
    assert f"Editing {path.trim()} ..." in transcript
