import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_back_cover_tex_01():
    
    abjad_ide('red %letter bce q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score', 'builds', 'letter-score', 'back-cover.tex')
    assert f'Editing {path.trim()} ...' in transcript
