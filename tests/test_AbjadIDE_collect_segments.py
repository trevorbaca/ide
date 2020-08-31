import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_collect_segments_01():
    """
    In build directory.
    """

    with ide.Test():

        abjad_ide("red bb let ggc q")
        lines = abjad_ide.io.transcript.lines
        for line in [
            "Collecting segment lys ...",
            " Writing red_score/builds/letter-score/_segments/segment-01.ily ...",
            " Writing red_score/builds/letter-score/_segments/segment-01.ly ...",
            " Writing red_score/builds/letter-score/_segments/segment-02.ily ...",
            " Writing red_score/builds/letter-score/_segments/segment-02.ly ...",
            " Writing red_score/builds/letter-score/_segments/segment-03.ily ...",
            " Writing red_score/builds/letter-score/_segments/segment-03.ly ...",
        ]:
            assert line in lines, repr(line)
