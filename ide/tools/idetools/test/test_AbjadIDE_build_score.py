import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(is_test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Travis-CI can not find fonts for XeTeX tests."
    )
def test_AbjadIDE_build_score_01():

    with ide.Test():
        input_ = 'red~score %letter bld q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        lines = [
            'Building score ...',
            'Collecting segment lys ...',
            'Removing red_score/builds/_segments/segment-01.ly ...',
            'Writing red_score/builds/_segments/segment-01.ly ...',
            'Removing red_score/builds/_segments/segment-02.ly ...',
            'Writing red_score/builds/_segments/segment-02.ly ...',
            'Removing red_score/builds/_segments/segment-03.ly ...',
            'Writing red_score/builds/_segments/segment-03.ly ...',
            '',
            'Generating music ...',
            'Removing red_score/builds/letter/music.ly ...',
            'Examining segments alphabetically ...',
            'Examining red_score/segments/segment_01 ...',
            'Examining red_score/segments/segment_02 ...',
            'Examining red_score/segments/segment_03 ...',
            'Writing red_score/builds/letter/music.ly ...'
            '',
            'Interpreting music ...',
            'Interpreting red_score/builds/letter/music.ly ...',
            'Writing red_score/builds/letter/music.pdf ...',
            '',
            'Interpreting front cover ...',
            'Interpreting red_score/builds/letter/front-cover.tex ...',
            'Writing red_score/builds/letter/front-cover.pdf ...',
            '',
            'Interpreting preface ...',
            'Interpreting red_score/builds/letter/preface.tex ...',
            'Writing red_score/builds/letter/preface.pdf ...',
            '',
            'Interpreting back cover ...',
            'Interpreting red_score/builds/letter/back-cover.tex ...',
            'Writing red_score/builds/letter/back-cover.pdf ...',
            '',
            'Generating score ...',
            'Removing red_score/builds/letter/score.tex ...',
            'Writing red_score/builds/letter/score.tex ...',
            '',
            'Interpreting score ...',
            'Interpreting red_score/builds/letter/score.tex ...',
            'Writing red_score/builds/letter/score.pdf ...',
            '',
            'Opening red_score/builds/letter/score.pdf ...',
            '',
            ]
        for line in lines:
            assert line in transcript
