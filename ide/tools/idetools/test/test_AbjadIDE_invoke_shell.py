import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_invoke_shell_01():
    r'''In scores directory.
    '''

    path = ide.Path('example_scores')
    input_ = '!pwd q'
    abjad_ide._start(input_=input_)
    assert str(path) in abjad_ide._io_manager._transcript.contents


def test_AbjadIDE_invoke_shell_02():
    r'''In material directory.
    '''

    path = ide.Path('red_score').materials / 'tempi'
    input_ = 'red~score mm tempi !pwd q'
    abjad_ide._start(input_=input_)
    assert str(path) in abjad_ide._io_manager._transcript.contents


def test_AbjadIDE_invoke_shell_03():
    r'''In build directory.
    '''

    path = ide.Path('red_score').build
    input_ = 'red~score bb !pwd q'
    abjad_ide._start(input_=input_)
    assert str(path) in abjad_ide._io_manager._transcript.contents
