import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)

# TODO: add transcript asserts

def test_AbjadIDE_replace_01():
    r'''In score directory.
    '''

    with ide.Test():

        abjad_ide('red~score sr RhythmMaker q')
        transcript = abjad_ide.io_manager.transcript
        string = 'class RhythmMaker(abjad.rhythmmakertools.RhythmMaker):'
        assert string in transcript

        abjad_ide('red~score rp RhythmMaker FooMaker y q')
        transcript = abjad_ide.io_manager.transcript
        assert 'Replaced 2 instances over 1 lines in 1 files.' in transcript

        abjad_ide('red~score rp FooMaker RhythmMaker y q')
        transcript = abjad_ide.io_manager.transcript
        assert 'Replaced 2 instances over 1 lines in 1 files.' in transcript
