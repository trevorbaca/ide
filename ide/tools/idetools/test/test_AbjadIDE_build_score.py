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
        transcript = abjad_ide._io_manager._transcript.contents
        lines = [
            'Building score ...',
            'Collecting segment lys ...',
            'Removing red_score/build/_segments/segment-01.ly ...',
            'Writing red_score/build/_segments/segment-01.ly ...',
            'Removing red_score/build/_segments/segment-02.ly ...',
            'Writing red_score/build/_segments/segment-02.ly ...',
            'Removing red_score/build/_segments/segment-03.ly ...',
            'Writing red_score/build/_segments/segment-03.ly ...',
            '',
            'Generating music ...',
            'Removing red_score/build/letter/music.ly ...',
            'Examining segments in alphabetical order ...',
            'Examining red_score/segments/segment_01 ...',
            'Examining red_score/segments/segment_02 ...',
            'Examining red_score/segments/segment_03 ...',
            'Writing red_score/build/letter/music.ly ...'
            '',
            'Interpreting music ...',
            'Interpreting red_score/build/letter/music.ly ...',
            'Writing red_score/build/letter/music.pdf ...',
            '',
            'Interpreting front cover ...',
            'Interpreting red_score/build/letter/front-cover.tex ...',
            'Writing red_score/build/letter/front-cover.pdf ...',
            '',
            'Interpreting preface ...',
            'Interpreting red_score/build/letter/preface.tex ...',
            'Writing red_score/build/letter/preface.pdf ...',
            '',
            'Interpreting back cover ...',
            'Interpreting red_score/build/letter/back-cover.tex ...',
            'Writing red_score/build/letter/back-cover.pdf ...',
            '',
            'Generating score ...',
            'Removing red_score/build/letter/score.tex ...',
            'Writing red_score/build/letter/score.tex ...',
            '',
            'Interpreting score ...',
            'Interpreting red_score/build/letter/score.tex ...',
            'Writing red_score/build/letter/score.pdf ...',
            '',
            'Opening red_score/build/letter/score.pdf ...',
            '',
            ]
        for line in lines:
            assert line in transcript
