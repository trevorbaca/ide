import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_empty_clipboard_01():

    abjad_ide('pc Red,Blue pe ps q')
    transcript = abjad_ide.io.transcript
    assert not bool(abjad_ide._clipboard)
    assert 'Emptying clipboard ...' in transcript
    assert 'Showing empty clipboard ...' in transcript
