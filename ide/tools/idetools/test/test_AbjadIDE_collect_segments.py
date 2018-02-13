import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_collect_segments_01():
    r'''In build directory.
    '''

    with ide.Test():

        abjad_ide('red %let ggc q')
        lines = abjad_ide.io.transcript.lines
        index = lines.index('Collecting segment lys ...')
        assert lines[index:] == [
            'Collecting segment lys ...',
            ' Writing red_score/builds/letter-score/_segments/segment--.ly ...',
            ' Writing red_score/builds/letter-score/_segments/segment-A.ly ...',
            ' Writing red_score/builds/letter-score/_segments/segment-B.ly ...',
            '',
            '> q',
            '',
            ]
