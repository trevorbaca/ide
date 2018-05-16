import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_show_clipboard_01():

    abjad_ide('cbs q')
    transcript = abjad_ide.io.transcript
    assert 'Showing empty clipboard ...' in transcript

    abjad_ide('cbc Red,Blue cbs q')
    transcript = abjad_ide.io.transcript
    assert 'Showing clipboard ...' in transcript
    assert ide.Path('red_score').wrapper().trim() in transcript
    assert ide.Path('blue_score').wrapper().trim() in transcript
