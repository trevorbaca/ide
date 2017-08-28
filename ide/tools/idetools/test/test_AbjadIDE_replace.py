import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_replace_01():
    r'''In score directory.
    '''

    with ide.Test():
        path = ide.Path('red_score').tools / 'RhythmMaker.py'

        input_ = 'red~score sr RhythmMaker q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'class RhythmMaker(abjad.rhythmmakertools.RhythmMaker):' in \
            transcript

        input_ = 'red~score rp RhythmMaker FooMaker y q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Replaced 2 instances over 1 line in 1 file.' in transcript

        input_ = 'red~score rp FooMaker RhythmMaker y q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Replaced 2 instances over 1 line in 1 file.' in transcript
