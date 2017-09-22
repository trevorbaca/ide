import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_ly_01():

    abjad_ide('red~score %A lye q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segments('A', 'illustration.ly')
    assert f'Editing {path.trim()} ...' in transcript
