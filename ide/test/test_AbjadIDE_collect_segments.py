import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_collect_segments_01():
    """
    In build directory.
    """

    with ide.Test():

        abjad_ide('red %let ggc q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Collecting segment lys ...',
            ' Writing red_score/builds/letter-score/_segments/segment--.ily ...',
            ' Writing red_score/builds/letter-score/_segments/segment--.ly ...',
            ' Writing red_score/builds/letter-score/_segments/segment-A.ily ...',
            ' Writing red_score/builds/letter-score/_segments/segment-A.ly ...',
            ' Writing red_score/builds/letter-score/_segments/segment-B.ily ...',
            ' Writing red_score/builds/letter-score/_segments/segment-B.ly ...',
            ]:
          assert line in lines, repr(line)
