import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_empty_clipboard_01():

    abjad_ide('cbc Red,Blue cbe cbs q')
    transcript = abjad_ide.io.transcript
    assert not bool(abjad_ide.clipboard)
    assert 'Emptying clipboard ...' in transcript
    assert 'Showing empty clipboard ...' in transcript
