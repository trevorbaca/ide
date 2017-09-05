import abjad
import ide


def test_Path_is_external_01():

    scores = abjad.abjad_configuration.composer_scores_directory
    if 'trevorbaca' not in scores:
        return

    path = ide.Path('/Users/trevorbaca/Scores/_docs')
    assert path.is_external()
    assert not path.is_package_path()
