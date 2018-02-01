import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Travis-CI can not find fonts for XeTeX tests."
    )
def test_AbjadIDE_build_score_pdf_01():

    with ide.Test():
        abjad_ide('red %let spb q')
        lines = abjad_ide.io.transcript.lines
        index = lines.index('Building score ...')
        assert lines[index:] == [
            'Building score ...',
            'Generating red_score/builds/letter-score/music.ly ...',
            ' Removing red_score/builds/letter-score/music.ly ...',
            ' Examining red_score/segments/_ ...',
            ' Examining red_score/segments/A ...',
            ' Examining red_score/segments/B ...',
            ' Writing red_score/builds/letter-score/music.ly ...',
            'Collecting segment lys ...',
            ' Writing red_score/builds/letter-score/_segments/segment-_.ly ...',
            ' Writing red_score/builds/letter-score/_segments/segment-A.ly ...',
            ' Writing red_score/builds/letter-score/_segments/segment-B.ly ...',
            'Uncoloring persistent indicators ...',
            'Hiding score annotations ...',
            ' Deactivating score annotation tags in letter-score ...',
            '  Found no score annotation tags in letter-score ...',
            'Joining broken spanners ...',
            '',
            'Generating red_score/builds/letter-score/music.ly ...',
            ' Removing red_score/builds/letter-score/music.ly ...',
            ' Examining red_score/segments/_ ...',
            ' Examining red_score/segments/A ...',
            ' Examining red_score/segments/B ...',
            ' Writing red_score/builds/letter-score/music.ly ...',
            '',
            'Preparing red_score/builds/letter-score/music.ly ...',
            'Interpreting red_score/builds/letter-score/music.ly ...',
            'Writing red_score/builds/letter-score/music.pdf ...',
            '',
            'Interpreting red_score/builds/letter-score/front-cover.tex ...',
            'Writing red_score/builds/letter-score/front-cover.pdf ...',
            '',
            'Interpreting red_score/builds/letter-score/preface.tex ...',
            'Writing red_score/builds/letter-score/preface.pdf ...',
            '',
            'Interpreting red_score/builds/letter-score/back-cover.tex ...',
            'Writing red_score/builds/letter-score/back-cover.pdf ...',
            '',
            'Generating score ...',
            'Removing red_score/builds/letter-score/score.tex ...',
            'Writing red_score/builds/letter-score/score.tex ...',
            '',
            'Interpreting red_score/builds/letter-score/score.tex ...',
            'Writing red_score/builds/letter-score/score.pdf ...',
            'Opening red_score/builds/letter-score/score.pdf ...',
            '',
            '> q',
            '',
            ]
