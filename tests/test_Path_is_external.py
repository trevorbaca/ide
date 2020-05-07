import ide


def test_Path_is_external_01():

    path = ide.Path("/Users/trevorbaca/Scores/_docs")
    assert path.is_external()
    assert not path.is_score_package_path()
