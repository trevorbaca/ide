import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_check_definition_01():
    r'''In material directory.
    '''

    path = ide.PackagePath('red_score').materials / 'magic_numbers' / 'definition.py'
    input_ = 'red~score %magic dfk q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript


def test_AbjadIDE_check_definition_02():
    r'''In segment directory.
    '''

    path = ide.PackagePath('red_score').segments / 'segment_01' / 'definition.py'
    input_ = 'red~score %A dfk q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert f'{path.trim()} ... OK' in transcript
    assert 'Total time ' in transcript
