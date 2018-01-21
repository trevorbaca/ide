import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_score_tex_01():
    
    abjad_ide('red %letter re q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score', 'builds', 'letter-score', 'score.tex')
    assert f'Editing {path.trim()} ...' in transcript
