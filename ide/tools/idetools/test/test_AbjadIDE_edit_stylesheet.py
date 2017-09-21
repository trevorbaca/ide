import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_stylesheet_01():
    
    abjad_ide('red %letter ye q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').builds('letter', 'stylesheet.ily')
    assert f'Editing {path.trim()} ...' in transcript
