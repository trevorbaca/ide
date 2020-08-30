import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_edit_files_01():
    """
    Handles nonexisting numeric input.
    """

    abjad_ide("red gg ef 0 q")
    transcript = abjad_ide.io.transcript
    assert "Matching '0' to 0 files ..." in transcript

    abjad_ide("red gg ef 1 q")
    transcript = abjad_ide.io.transcript
    assert "Matching '1' to 0 files ..." in transcript

    abjad_ide("red gg ef 99 q")
    transcript = abjad_ide.io.transcript
    assert "Matching '99' to 0 files ..." in transcript
