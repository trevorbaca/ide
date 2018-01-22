import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_layout_py_01():
    
    abjad_ide('red %let ype q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score', 'builds', 'letter-score', 'layout.py')
    assert f'Editing {path.trim()} ...' in transcript
