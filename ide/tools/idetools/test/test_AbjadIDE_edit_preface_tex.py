import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_preface_tex_01():
    
    abjad_ide('red %letter pe q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score', 'builds', 'letter-score', 'preface.tex')
    assert f'Editing {path.trim()} ...' in transcript
