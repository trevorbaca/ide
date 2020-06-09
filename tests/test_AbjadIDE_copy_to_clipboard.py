import abjad
import ide

abjad_ide = ide.AbjadIDE(test=True)
scores = ide.Configuration().test_scores_directory


def test_AbjadIDE_copy_to_clipboard_01():

    abjad_ide("cbc Red,Blue q")
    transcript = abjad_ide.io.transcript
    red_score_wrapper = abjad.Path(scores, "red_score")
    blue_score_wrapper = abjad.Path(scores, "blue_score")
    assert red_score_wrapper in abjad_ide.clipboard
    assert blue_score_wrapper in abjad_ide.clipboard
    assert "Select packages for clipboard> Red,Blue" in transcript
    assert "Copying to clipboard ..." in transcript
    assert red_score_wrapper.trim() in transcript
    assert blue_score_wrapper.trim() in transcript


def test_AbjadIDE_copy_to_clipboard_02():
    """
    Can jump from selector.
    """

    abjad_ide("cbc ss q")
    transcript = abjad_ide.io.transcript
    assert "Select packages for clipboard> ss" in transcript
    assert "Copying to clipboard ..." not in transcript
