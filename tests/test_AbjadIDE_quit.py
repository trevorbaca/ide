import ide

abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_quit_01():
    """
    In scores directory.
    """

    abjad_ide("q")


def test_AbjadIDE_quit_02():
    """
    In builds directory.
    """

    abjad_ide("red bb q")


def test_AbjadIDE_quit_03():
    """
    In material directory.
    """

    abjad_ide("red %metronome q")


def test_AbjadIDE_quit_04():
    """
    In score directory.
    """

    abjad_ide("red q")


def test_AbjadIDE_quit_05():
    """
    In segment directory.
    """

    abjad_ide("red %A q")
