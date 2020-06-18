import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.configuration.test_scores_directory


def test_AbjadIDE_edit_all_01():
    """
    Handles nonexisting numeric input.
    """

    abjad_ide("red gg @@0 q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@@0' to 0 files ..." in transcript

    abjad_ide("red gg @@1 q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@@1' to 0 files ..." in transcript

    abjad_ide("red gg @@99 q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@@99' to 0 files ..." in transcript


def test_AbjadIDE_edit_all_02():
    """
    Handles empty input, junk input and nonfile input.
    """

    abjad_ide("@@asdf q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@@asdf' to 0 files ..." in transcript
