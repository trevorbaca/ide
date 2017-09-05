import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_external_directory_01():

    directory = abjad.abjad_configuration.composer_scores_directory
    if 'trevorbaca' not in directory:
        return

    abjad_ide('cdk q')
    transcript = abjad_ide.io_manager.transcript
    assert '/Users/trevorbaca/Desktop' in transcript
