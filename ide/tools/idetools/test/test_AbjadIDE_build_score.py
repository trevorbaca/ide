import ide
#import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


# TODO: update to to format-specific build directories
#def test_AbjadIDE_build_score_01():
#
#    music_pdf = pathlib.Path(
#        abjad_ide.configuration.example_scores_directory,
#        'red_score',
#        'red_score',
#        'build',
#        'music.pdf',
#        )
#    score_pdf = pathlib.Path(
#        abjad_ide.configuration.example_scores_directory,
#        'red_score',
#        'red_score',
#        'build',
#        'score.pdf',
#        )
#    paths = (music_pdf, score_pdf)
#
#    with ide.Test():
#        input_ = 'red~score bb bld q'
#        abjad_ide._start(input_=input_)
#        contents = abjad_ide._io_manager._transcript.contents
#
#    lines = [
#        'Building score ...',
#        'Copying segment LilyPond files into build directory ...',
#        'Preserving red_score/red_score/build/segment-01.ly ...',
#        'Preserving red_score/red_score/build/segment-02.ly ...',
#        'Preserving red_score/red_score/build/segment-03.ly ...',
#        'Generating music LilyPond file ...',
#        'Examining segments in alphabetical order ...',
#        'Examining red_score/red_score/segments/segment_01 ...',
#        'Examining red_score/red_score/segments/segment_02 ...',
#        'Examining red_score/red_score/segments/segment_03 ...',
#        'Preserving red_score/red_score/build/music.ly ...',
#        'Calling LilyPond on red_score/red_score/build/music.ly ...',
#        'Preserving red_score/red_score/build/music.pdf ...',
#        'Interpreting red_score/red_score/build/front-cover.tex ...',
#        'Preserving red_score/red_score/build/front-cover.pdf ...',
#        'Interpreting red_score/red_score/build/preface.tex ...',
#        'Preserving red_score/red_score/build/preface.pdf ...',
#        'Interpreting red_score/red_score/build/back-cover.tex ...',
#        'Preserving red_score/red_score/build/back-cover.pdf ...',
#        'Generating score LaTeX file ...',
#        'Preserving red_score/red_score/build/score.tex ...',
#        'Interpreting red_score/red_score/build/score.tex ...',
#        'Overwriting red_score/red_score/build/score.pdf ...',
#        'Opening red_score/red_score/build/score.pdf ...',
#        ]
#
#    for line in lines:
#        assert line in contents
