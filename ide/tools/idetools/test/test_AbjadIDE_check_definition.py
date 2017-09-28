import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_check_definition_01():
    r'''In material directory.
    '''

    path = ide.Path(
        'red_score', 'materials', 'red_pitch_classes', 'definition.py')
    abjad_ide('red %rpc dfk q')
    transcript = abjad_ide.io.transcript
    assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript


def test_AbjadIDE_check_definition_02():
    r'''In segment directory.
    '''

    path = ide.Path('red_score', 'segments', 'A', 'definition.py')
    abjad_ide('red %A dfk q')
    transcript = abjad_ide.io.transcript
    assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript
