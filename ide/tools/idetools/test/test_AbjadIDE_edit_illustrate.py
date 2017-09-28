import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_illustrate_01():

    abjad_ide('red %rpc ill q')
    transcript = abjad_ide.io.transcript
    path = ide.Path(
        'red_score', 'materials', 'red_pitch_classes', '__illustrate__.py')
    assert f'Editing {path.trim()} ...' in transcript
