import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_smart_edit_01():
    """
    Edits etc file.
    """

    abjad_ide("red @notes.txt q")
    transcript = abjad_ide.io.transcript
    path = ide.Path(scores, "red_score", "red_score", "etc", "notes.txt")
    assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_smart_edit_02():
    """
    Edits segment definition file.
    """

    abjad_ide("red @A q")
    transcript = abjad_ide.io.transcript
    path = ide.Path(scores, "red_score", "red_score", "segments", "A", "definition.py")
    assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_smart_edit_03():
    """
    Edits stylesheet.
    """

    abjad_ide("red @contexts q")
    transcript = abjad_ide.io.transcript
    path = ide.Path(scores, "red_score", "red_score", "stylesheets", "contexts.ily")
    assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_smart_edit_04():
    """
    Missing pattern.
    """

    abjad_ide("@ q")
    transcript = abjad_ide.io.transcript
    assert "Missing '@' pattern ..." in transcript


def test_AbjadIDE_smart_edit_05():
    """
    Unmatched pattern.
    """

    abjad_ide("@asdf q")
    transcript = abjad_ide.io.transcript
    assert "Matching '@asdf' to 0 files ..." in transcript
