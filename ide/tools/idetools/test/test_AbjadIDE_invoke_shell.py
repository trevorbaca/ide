import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_invoke_shell_01():
    r'''In scores directory.
    '''

    abjad_ide('!pwd q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('test_scores')
    assert str(path) in transcript


def test_AbjadIDE_invoke_shell_02():
    r'''In material directory.
    '''

    abjad_ide('red~score mm tempi !pwd q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').materials / 'tempi'
    assert str(path) in transcript


def test_AbjadIDE_invoke_shell_03():
    r'''In builds directory.
    '''

    abjad_ide('red~score bb !pwd q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').builds
    assert str(path) in transcript


def test_AbjadIDE_invoke_shell_04():
    r'''In external directory.
    '''

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('cdk !pwd q')
    transcript = abjad_ide.io.transcript
    assert '/Users/trevorbaca/Desktop' in transcript


def test_AbjadIDE_invoke_shell_05():
    r'''Works with spaces in command.
    '''

    abjad_ide('!ls~-a q')
    transcript = abjad_ide.io.transcript
    assert '.' in transcript
    assert '..' in transcript
    assert '__metadata__.py' in transcript
    assert 'blue_score' in transcript
    assert 'red_score' in transcript
