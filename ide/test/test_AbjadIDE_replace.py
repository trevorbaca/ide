import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_replace_01():
    """
    In score directory.
    """

    with ide.Test():

        abjad_ide('red sr RhythmMaker q')
        transcript = abjad_ide.io.transcript
        assert 'Enter search string> RhythmMaker' in transcript
        string = 'class RhythmMaker(abjad.rhythmos.RhythmMaker):'
        assert string in transcript

        abjad_ide('red rp RhythmMaker FooMaker y q')
        transcript = abjad_ide.io.transcript
        assert 'Enter search string> RhythmMaker' in transcript
        assert 'Enter replace string> FooMaker' in transcript
        assert 'Replaced 4 instances over 2 lines in 2 files.' in transcript

        abjad_ide('red rp FooMaker RhythmMaker y q')
        transcript = abjad_ide.io.transcript
        assert 'Enter search string> FooMaker' in transcript
        assert 'Enter replace string> RhythmMaker' in transcript
        assert 'Replaced 4 instances over 2 lines in 2 files.' in transcript


def test_AbjadIDE_replace_02():
    r'''In library.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll rp RhythmMaker <return> q')
    transcript = abjad_ide.io.transcript
    assert 'Enter search string> RhythmMaker' in transcript
    assert 'Enter replace string>' in transcript
