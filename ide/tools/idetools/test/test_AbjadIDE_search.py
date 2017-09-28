import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_search_01():
    r'''In scores directory.
    '''

    abjad_ide('sr RhythmMaker q')
    transcript = abjad_ide.io.transcript
    assert 'Enter search string> RhythmMaker' in transcript

    ack_line = 'blue_score/blue_score/materials/blue_rhythm_1/definition.py:4:'
    ack_line += 'blue_rhythm_1 = abjad.rhythmmakertools.TaleaRhythmMaker('
    grep_line = 'blue_score/blue_score/materials/blue_rhythm_1/definition.py:'
    grep_line += 'blue_rhythm_1 = abjad.rhythmmakertools.TaleaRhythmMaker('
    assert ack_line in transcript or grep_line in transcript

    ack_line = 'red_score/red_score/tools/RhythmMaker.py:4:'
    ack_line += 'class RhythmMaker(abjad.rhythmmakertools.RhythmMaker):'
    grep_line = 'red_score/red_score/tools/RhythmMaker.py:'
    grep_line += 'class RhythmMaker(abjad.rhythmmakertools.RhythmMaker):'
    assert ack_line in transcript or grep_line in transcript


def test_AbjadIDE_search_02():
    r'''In score directory.
    '''

    abjad_ide('red sr RhythmMaker q')
    transcript = abjad_ide.io.transcript
    assert 'Enter search string> RhythmMaker' in transcript

    ack_line = 'blue_score/blue_score/materials/blue_rhythm_1/definition.py:4:'
    ack_line += 'blue_rhythm_1 = rhythmmakertools.TaleaRhythmMaker('
    grep_line = 'blue_score/blue_score/materials/blue_rhythm_1/definition.py:'
    grep_line += 'blue_rhythm_1 = rhythmmakertools.TaleaRhythmMaker('
    assert ack_line not in transcript and grep_line not in transcript

    ack_line = 'tools/RhythmMaker.py:4:'
    ack_line += 'class RhythmMaker(abjad.rhythmmakertools.RhythmMaker):'
    grep_line = 'tools/RhythmMaker.py:'
    grep_line += 'class RhythmMaker(abjad.rhythmmakertools.RhythmMaker):'
    assert ack_line in transcript or grep_line in transcript


def test_AbjadIDE_search_03():
    r'''In library.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll sr RhythmMaker q')
    transcript = abjad_ide.io.transcript
    assert 'Enter search string> RhythmMaker' in transcript
