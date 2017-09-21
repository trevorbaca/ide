import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_preface_source_01():
    
    abjad_ide('red %letter re q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').build('letter', 'preface.tex')
    assert f'Editing {path.trim()} ...' in transcript
