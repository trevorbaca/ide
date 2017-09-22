import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_text_01():
    r'''Works in scores directory.
    '''

    abjad_ide('it foo q')
    transcript = abjad_ide.io.transcript
    assert 'Enter search string> foo' in transcript


def test_AbjadIDE_edit_text_02():
    r'''Works in score directory.
    '''

    abjad_ide('red it foo q')
    transcript = abjad_ide.io.transcript
    assert 'Enter search string> foo' in transcript


def test_AbjadIDE_edit_text_03():
    r'''Works in external directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdk it foo q')
    transcript = abjad_ide.io.transcript
    assert 'Enter search string> foo' in transcript
