import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_quit_01():
    r'''In scores directory.
    '''

    input_ = 'q'
    abjad_ide._start(input_=input_)


def test_AbjadIDE_quit_02():
    r'''In builds directory.
    '''

    input_ = 'red~score bb q'
    abjad_ide._start(input_=input_)


def test_AbjadIDE_quit_03():
    r'''In material directory.
    '''

    input_ = 'red~score %tempi q'
    abjad_ide._start(input_=input_)


def test_AbjadIDE_quit_04():
    r'''In score directory.
    '''

    input_ = 'red~score q'
    abjad_ide._start(input_=input_)


def test_AbjadIDE_quit_05():
    r'''In segment directory.
    '''

    input_ = 'red~score %A q'
    abjad_ide._start(input_=input_)
