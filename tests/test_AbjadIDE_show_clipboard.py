import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_show_clipboard_01():

    abjad_ide("cbs q")
    transcript = abjad_ide.io.transcript
    assert "Showing empty clipboard ..." in transcript

    abjad_ide("cbc Red,Blue cbs q")
    transcript = abjad_ide.io.transcript
    assert "Showing clipboard ..." in transcript
    assert ide.Path(scores, "red_score").trim() in transcript
    assert ide.Path(scores, "blue_score").trim() in transcript
