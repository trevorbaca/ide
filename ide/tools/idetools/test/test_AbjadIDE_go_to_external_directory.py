import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_external_directory_01():

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('cdk q')
    transcript = abjad_ide.io.transcript
    assert '/Users/trevorbaca/Desktop' in transcript
    assert '.gitignore' not in transcript
