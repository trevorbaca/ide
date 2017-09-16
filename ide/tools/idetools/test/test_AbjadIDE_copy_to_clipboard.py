import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_copy_to_clipboard_01():

    abjad_ide('cp Red,Blue q')
    transcript = abjad_ide.io.transcript
    red_score_wrapper = ide.Path('red_score').wrapper
    blue_score_wrapper = ide.Path('blue_score').wrapper
    assert red_score_wrapper in abjad_ide._clipboard
    assert blue_score_wrapper in abjad_ide._clipboard
    assert 'Select packages for clipboard> Red,Blue' in transcript
    assert 'Copying to clipboard ...' in transcript
    assert red_score_wrapper.trim() in transcript
    assert blue_score_wrapper.trim() in transcript


def test_AbjadIDE_copy_to_clipboard_02():
    r'''Can jump from selector.
    '''

    abjad_ide('cp ss q')
    transcript = abjad_ide.io.transcript
    assert 'Select packages for clipboard> ss' in transcript
    assert 'Copying to clipboard ...' not in transcript
