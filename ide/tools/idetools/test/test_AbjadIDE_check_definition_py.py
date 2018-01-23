import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_check_definition_py_01():
    r'''In material directory.
    '''

    path = ide.Path(
        'red_score', 'materials', 'red_pitch_classes', 'definition.py')
    abjad_ide('red %rpc dpk q')
    transcript = abjad_ide.io.transcript
    assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript


def test_AbjadIDE_check_definition_py_02():
    r'''In materials directory.
    '''

    abjad_ide('red mm dpk q')
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


def test_AbjadIDE_check_definition_py_03():
    r'''In segment directory.
    '''

    path = ide.Path('red_score', 'segments', 'A', 'definition.py')
    abjad_ide('red %A dpk q')
    transcript = abjad_ide.io.transcript
    assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript


def test_AbjadIDE_check_definition_py_04():
    r'''In segments directory.
    '''

    abjad_ide('red gg dpk q')
    transcript = abjad_ide.io.transcript
    for name in ['_', 'A', 'B']:
        path = ide.Path('red_score', 'segments', name, 'definition.py')
        assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript
