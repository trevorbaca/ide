import abjad


def test_Path_is_external_01():

    path = abjad.Path("/Users/trevorbaca/Scores/_docs")
    assert path.is_external()
    assert not path.is_score_package_path()
