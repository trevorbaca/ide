import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_string_01():
    abjad_ide("es foo q")
    transcript = abjad_ide.io.transcript
    assert "Enter search string> foo" in transcript
