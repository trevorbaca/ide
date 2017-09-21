import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_check_definition_file_01():
    r'''In material directory.
    '''

    path = ide.Path('red_score').material('magic_numbers', 'definition.py')
    abjad_ide('red~score %magic dfk q')
    transcript = abjad_ide.io.transcript
    assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript


def test_AbjadIDE_check_definition_file_02():
    r'''In segment directory.
    '''

    path = ide.Path('red_score').segment('segment_01', 'definition.py')
    abjad_ide('red~score %A dfk q')
    transcript = abjad_ide.io.transcript
    assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript
