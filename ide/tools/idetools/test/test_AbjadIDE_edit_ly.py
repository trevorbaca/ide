import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_ly_01():

    path = ide.PackagePath('red_score').segments / 'segment_01'
    path /= 'illustration.ly'

    input_ = 'red~score %A ly q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript
