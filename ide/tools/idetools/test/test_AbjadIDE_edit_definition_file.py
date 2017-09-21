import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_definition_file_01():
    r'''In material directory.
    '''

    abjad_ide('red~score %magic df q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').materials('magic_numbers', 'definition.py')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_definition_file_02():
    r'''In segment directory.
    '''

    abjad_ide('red~score %A df q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segments('segment_01', 'definition.py')
    assert f'Editing {path.trim()} ...' in transcript
