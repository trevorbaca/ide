import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_back_cover_source_01():
    
    abjad_ide('red %letter bce q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').build('letter', 'back-cover.tex')
    assert f'Editing {path.trim()} ...' in transcript
