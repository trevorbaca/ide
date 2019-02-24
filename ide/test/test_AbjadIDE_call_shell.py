import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_call_shell_01():
    """
    In scores directory.
    """

    abjad_ide('!pwd q')
    transcript = abjad_ide.io.transcript
    assert "Calling shell on 'pwd' ..." in transcript


def test_AbjadIDE_call_shell_02():
    """
    In material directory.
    """

    abjad_ide('red mm metronome !pwd q')
    transcript = abjad_ide.io.transcript
    assert "Calling shell on 'pwd' ..." in transcript


def test_AbjadIDE_call_shell_03():
    """
    In builds directory.
    """

    abjad_ide('red bb !pwd q')
    transcript = abjad_ide.io.transcript
    assert "Calling shell on 'pwd' ..." in transcript


def test_AbjadIDE_call_shell_04():
    """
    Works with spaces in command.
    """

    abjad_ide('!ls~-a q')
    transcript = abjad_ide.io.transcript
    assert "Calling shell on 'ls -a' ..." in transcript


def test_AbjadIDE_call_shell_05():
    """
    Empty excalamation raises no exception.
    """

    abjad_ide('! q')
    transcript = abjad_ide.io.transcript
    assert "Calling shell on '' ..." in transcript
