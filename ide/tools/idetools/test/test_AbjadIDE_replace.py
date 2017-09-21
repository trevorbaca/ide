import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_replace_01():
    r'''In score directory.
    '''

    with ide.Test():

        abjad_ide('red~score sr RhythmMaker q')
        transcript = abjad_ide.io.transcript
        assert 'Enter search string> RhythmMaker' in transcript
        string = 'class RhythmMaker(abjad.rhythmmakertools.RhythmMaker):'
        assert string in transcript

        abjad_ide('red~score rp RhythmMaker FooMaker y q')
        transcript = abjad_ide.io.transcript
        assert 'Enter search string> RhythmMaker' in transcript
        assert 'Enter replace string> FooMaker' in transcript
        assert 'Replaced 2 instances over 1 lines in 1 files.' in transcript

        abjad_ide('red~score rp FooMaker RhythmMaker y q')
        transcript = abjad_ide.io.transcript
        assert 'Enter search string> FooMaker' in transcript
        assert 'Enter replace string> RhythmMaker' in transcript
        assert 'Replaced 2 instances over 1 lines in 1 files.' in transcript


def test_AbjadIDE_replace_02():
    r'''In library.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('lib rp RhythmMaker <return> q')
    transcript = abjad_ide.io.transcript
    assert 'Enter search string> RhythmMaker' in transcript
    assert 'Enter replace string>' in transcript
