import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_ly_01():

    abjad_ide('red~score %A ly q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segments / 'segment_01' / 'illustration.ly'
    assert f'Editing {path.trim()} ...' in transcript
