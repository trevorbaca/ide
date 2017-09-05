import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_check_definition_01():
    r'''In material directory.
    '''

    path = ide.Path('red_score').materials / 'magic_numbers' / 'definition.py'
    abjad_ide('red~score %magic dfk q')
    transcript = abjad_ide.io_manager.transcript
    assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript


def test_AbjadIDE_check_definition_02():
    r'''In segment directory.
    '''

    path = ide.Path('red_score').segments / 'segment_01' / 'definition.py'
    abjad_ide('red~score %A dfk q')
    transcript = abjad_ide.io_manager.transcript
    assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript
