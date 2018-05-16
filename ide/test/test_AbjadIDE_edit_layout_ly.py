import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_layout_ly_01():
    
    abjad_ide('red %let lle q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score', 'builds', 'letter-score', 'layout.ly')
    assert f'Editing {path.trim()} ...' in transcript
