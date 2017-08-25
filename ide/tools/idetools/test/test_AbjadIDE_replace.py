import abjad
import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_replace_01():
    r'''In score directory.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'tools',
        'RhythmMaker.py',
        )

    with ide.Test():
        input_ = 'red~score sr RhythmMaker q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert 'class RhythmMaker(abjad.rhythmmakertools.RhythmMaker):' in contents
        input_ = 'red~score rp RhythmMaker FooMaker y q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert 'Replaced 2 instances over 1 line in 1 file.' in contents
        input_ = 'red~score rp FooMaker RhythmMaker y q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert 'Replaced 2 instances over 1 line in 1 file.' in contents
