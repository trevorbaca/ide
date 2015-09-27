# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_build_score_01():

    music_pdf = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'music.pdf',
        )
    score_pdf = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'score.pdf',
        )
    paths = (music_pdf, score_pdf)

    with systemtools.FilesystemState(keep=paths):
        input_ = 'red~example~score bb bld q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    lines = [
        'Building score ...',
        'Copying segment LilyPond files into build directory ...',
        'Preserving red_example_score/red_example_score/build/segment-01.ly ...',
        'Preserving red_example_score/red_example_score/build/segment-02.ly ...',
        'Preserving red_example_score/red_example_score/build/segment-03.ly ...',
        'Generating music LilyPond file ...',
        'Examining segments in alphabetical order ...',
        'Examining red_example_score/red_example_score/segments/segment_01 ...',
        'Examining red_example_score/red_example_score/segments/segment_02 ...',
        'Examining red_example_score/red_example_score/segments/segment_03 ...',
        'Preserving red_example_score/red_example_score/build/music.ly ...',
        'Calling LilyPond on red_example_score/red_example_score/build/music.ly ...',
        'Preserving red_example_score/red_example_score/build/music.pdf ...',
        'Calling LaTeX on red_example_score/red_example_score/build/front-cover.tex ...',
        'Preserving red_example_score/red_example_score/build/front-cover.pdf ...',
        'Calling LaTeX on red_example_score/red_example_score/build/preface.tex ...',
        'Preserving red_example_score/red_example_score/build/preface.pdf ...',
        'Calling LaTeX on red_example_score/red_example_score/build/back-cover.tex ...',
        'Preserving red_example_score/red_example_score/build/back-cover.pdf ...',
        'Generating score LaTeX file ...',
        'Preserving red_example_score/red_example_score/build/score.tex ...',
        'Calling LaTeX on red_example_score/red_example_score/build/score.tex ...',
        'Overwriting red_example_score/red_example_score/build/score.pdf ...',
        'Opening red_example_score/red_example_score/build/score.pdf ...',
        ]

    for line in lines:
        assert line in contents