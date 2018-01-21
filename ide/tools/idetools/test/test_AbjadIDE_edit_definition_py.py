import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_definition_py_01():
    r'''In material directory.
    '''

    abjad_ide('red %rpc dfe q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path(
        'red_score', 'materials', 'red_pitch_classes', 'definition.py')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_definition_py_02():
    r'''In segment directory.
    '''

    abjad_ide('red %A dfe q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score', 'segments', 'A', 'definition.py')
    assert f'Editing {path.trim()} ...' in transcript
