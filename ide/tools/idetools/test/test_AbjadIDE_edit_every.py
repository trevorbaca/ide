import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_every_01():
    r'''Works in scores directory.
    '''

    abjad_ide('ee* foo q')
    transcript = abjad_ide.io_manager.transcript
    assert 'Enter search string> foo' in transcript


def test_AbjadIDE_edit_every_02():
    r'''Works in score directory.
    '''

    abjad_ide('red~score ee* foo q')
    transcript = abjad_ide.io_manager.transcript
    assert 'Enter search string> foo' in transcript
