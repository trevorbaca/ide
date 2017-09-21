import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_external_directory_01():

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdk q')
    transcript = abjad_ide.io.transcript
    assert '/Users/trevorbaca/Desktop' in transcript
    assert '.gitignore' not in transcript

    # regression: underscore files appear in external directory
    abjad_ide('cdj .. boiler q')
    transcript = abjad_ide.io.transcript
    assert '/Users/trevorbaca/abjad/abjad/boilerplate' in transcript
    assert '.gitignore' not in transcript
    assert '__aliases__.py' in transcript
