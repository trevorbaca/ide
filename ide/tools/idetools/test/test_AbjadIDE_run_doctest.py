import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_run_doctest_01():
    r'''In score directory.

    Output paths listed from score directory.
    '''

    input_ = 'red~score dt q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._session._attempted_method == '_run_doctest'


def test_AbjadIDE_run_doctest_02():
    r'''In tools directory.

    Output paths listed from score directory.
    '''

    input_ = 'red~score oo dt q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._session._attempted_method == '_run_doctest'


def test_AbjadIDE_run_doctest_03():
    r'''With caret-navigation to doctest a single file.

    Output paths listed from score directory.
    '''

    input_ = 'red~score ^ST q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._session._attempted_method == '_run_doctest'
