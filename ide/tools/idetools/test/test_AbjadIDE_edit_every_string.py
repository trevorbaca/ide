import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_every_string_01():
    r'''Works in scores directory.
    '''

    abjad_ide('ee* foo q')
    transcript = abjad_ide.io.transcript
    assert 'Enter search string> foo' in transcript


def test_AbjadIDE_edit_every_string_02():
    r'''Works in score directory.
    '''

    abjad_ide('red~score ee* foo q')
    transcript = abjad_ide.io.transcript
    assert 'Enter search string> foo' in transcript


def test_AbjadIDE_edit_every_string_03():
    r'''Works in external directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdk ee* foo q')
    transcript = abjad_ide.io.transcript
    assert 'Enter search string> foo' in transcript
