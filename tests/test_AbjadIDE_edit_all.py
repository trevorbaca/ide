import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_edit_all_01():
    """
    Edits segment definition files.
    """

    abjad_ide("red gg @@efin q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@@efin' to 3 files ..." in transcript
    for name in ["_", "A", "B"]:
        path = ide.Path(
            scores, "red_score", "red_score", "segments", name, "definition.py"
        )
        assert f"Editing {path.trim()} ..." in transcript

    abjad_ide("red gg @@ q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@@' to 15 files ..." in transcript


def test_AbjadIDE_edit_all_02():
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


def test_AbjadIDE_edit_all_03():
    """
    Handles empty input, junk input and nonfile input.
    """

    abjad_ide("@@asdf q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@@asdf' to 0 files ..." in transcript


def test_AbjadIDE_edit_all_04():
    """
    Provides warning with <= 20 files.
    """

    abjad_ide("red @@ <return> q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@@' to " in transcript
    assert " files ok?> " in transcript
