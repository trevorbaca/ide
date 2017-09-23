import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_quit_01():
    r'''In scores directory.
    '''

    abjad_ide('q')


def test_AbjadIDE_quit_02():
    r'''In builds directory.
    '''

    abjad_ide('red bb q')


def test_AbjadIDE_quit_03():
    r'''In material directory.
    '''

    abjad_ide('red %tempi q')


def test_AbjadIDE_quit_04():
    r'''In score directory.
    '''

    abjad_ide('red q')


def test_AbjadIDE_quit_05():
    r'''In segment directory.
    '''

    abjad_ide('red %A q')
