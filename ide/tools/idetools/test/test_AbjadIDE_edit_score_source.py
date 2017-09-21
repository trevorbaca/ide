import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_score_source_01():
    
    abjad_ide('red %letter se q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').build('letter', 'score.tex')
    assert f'Editing {path.trim()} ...' in transcript
