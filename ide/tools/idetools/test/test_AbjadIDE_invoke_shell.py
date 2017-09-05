import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_invoke_shell_01():
    r'''In scores directory.
    '''

    abjad_ide('!pwd q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('test_scores')
    assert str(path) in transcript


def test_AbjadIDE_invoke_shell_02():
    r'''In material directory.
    '''

    abjad_ide('red~score mm tempi !pwd q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').materials / 'tempi'
    assert str(path) in transcript


def test_AbjadIDE_invoke_shell_03():
    r'''In builds directory.
    '''

    abjad_ide('red~score bb !pwd q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').builds
    assert str(path) in transcript
