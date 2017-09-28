import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_call_shell_01():
    r'''In scores directory.
    '''

    abjad_ide('!pwd q')
    transcript = abjad_ide.io.transcript
    assert "Calling shell on 'pwd' ..." in transcript


def test_AbjadIDE_call_shell_02():
    r'''In material directory.
    '''

    abjad_ide('red mm metronome !pwd q')
    transcript = abjad_ide.io.transcript
    assert "Calling shell on 'pwd' ..." in transcript


def test_AbjadIDE_call_shell_03():
    r'''In builds directory.
    '''

    abjad_ide('red bb !pwd q')
    transcript = abjad_ide.io.transcript
    assert "Calling shell on 'pwd' ..." in transcript


def test_AbjadIDE_call_shell_04():
    r'''In external directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdk !pwd q')
    transcript = abjad_ide.io.transcript
    assert "Calling shell on 'pwd' ..." in transcript


def test_AbjadIDE_call_shell_05():
    r'''Works with spaces in command.
    '''

    abjad_ide('!ls~-a q')
    transcript = abjad_ide.io.transcript
    assert "Calling shell on 'ls -a' ..." in transcript
