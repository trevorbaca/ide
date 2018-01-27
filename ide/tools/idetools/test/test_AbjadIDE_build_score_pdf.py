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
            'Collecting segment lys ...',
            'Removing red_score/builds/letter-score/music.ly ...',
            'Examining segments alphabetically ...',
            'Examining red_score/segments/_ ...',
            'Examining red_score/segments/A ...',
            'Examining red_score/segments/B ...',
            'Writing red_score/builds/letter-score/music.ly ...',
            'Writing red_score/builds/letter-score/_segments/segment-_.ly ...',
            'Writing red_score/builds/letter-score/_segments/segment-A.ly ...',
            'Writing red_score/builds/letter-score/_segments/segment-B.ly ...',
            'Found no + tags in letter-score ...',
            'Found no -LETTER_SCORE tags in letter-score ...',
            'Found no +LETTER_SCORE tags in letter-score ...',
            'Found no EOL_FERMATA tags in letter-score ...',
            'Found no SHIFTED_CLEF tags in letter-score ...',
            'Found no persistent indicator color expression tags in letter-score ...',
            'Found no persistent indicator color suppression tags in letter-score ...',
            'Found no score annotation tags in letter-score ...',
            'Found no broken spanner expression tags in letter-score ...',
            'Found no broken spanner suppression tags in letter-score ...',
            '',
            'Removing red_score/builds/letter-score/music.ly ...',
            'Examining segments alphabetically ...',
            'Examining red_score/segments/_ ...',
            'Examining red_score/segments/A ...',
            'Examining red_score/segments/B ...',
            'Writing red_score/builds/letter-score/music.ly ...',
            '',
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
