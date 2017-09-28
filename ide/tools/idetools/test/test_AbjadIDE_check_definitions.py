import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_check_definitions_01():
    r'''In materials directory.
    '''

    abjad_ide('red mm dfk* q')
    transcript = abjad_ide.io.transcript
    for name in [
        'instruments',
        'red_pitch_classes',
        'metronome_marks',
        'ranges',
        'time_signatures',
        ]:
        path = ide.Path('red_score', 'materials', name, 'definition.py')
        assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript


def test_AbjadIDE_check_definitions_02():
    r'''In segments directory.
    '''

    abjad_ide('red gg dfk* q')
    transcript = abjad_ide.io.transcript
    for name in ['_', 'A', 'B']:
        path = ide.Path('red_score', 'segments', name, 'definition.py')
        assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript
