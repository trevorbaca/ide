import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_replace_01():
    """
    In score directory.
    """

    with ide.Test():

        abjad_ide("red sr RhythmMaker q")
        transcript = abjad_ide.io.transcript
        assert "Enter search string> RhythmMaker" in transcript
        string = "class RhythmMaker(rmakers.RhythmMaker):"
        assert string in transcript

        abjad_ide("red rp RhythmMaker FooMaker y q")
        transcript = abjad_ide.io.transcript
        assert "Enter search string> RhythmMaker" in transcript
        assert "Enter replace string> FooMaker" in transcript
        assert "Replaced 8 instances over 6 lines in 3 files." in transcript

        abjad_ide("red rp FooMaker RhythmMaker y q")
        transcript = abjad_ide.io.transcript
        assert "Enter search string> FooMaker" in transcript
        assert "Enter replace string> RhythmMaker" in transcript
        assert "Replaced 8 instances over 6 lines in 3 files." in transcript
