import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_show_clipboard_01():

    abjad_ide('cs q')
    transcript = abjad_ide.io.transcript
    assert 'Showing empty clipboard ...' in transcript

    abjad_ide('cp Red,Blue cs q')
    transcript = abjad_ide.io.transcript
    assert 'Showing clipboard ...' in transcript
    assert ide.Path('red_score').wrapper().trim() in transcript
    assert ide.Path('blue_score').wrapper().trim() in transcript
