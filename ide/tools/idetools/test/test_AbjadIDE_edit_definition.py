import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_definition_01():
    r'''In material directory.
    '''

    abjad_ide('red %magic dfe q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').materials('magic_numbers', 'definition.py')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_definition_02():
    r'''In segment directory.
    '''

    abjad_ide('red %A dfe q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segments('A', 'definition.py')
    assert f'Editing {path.trim()} ...' in transcript
