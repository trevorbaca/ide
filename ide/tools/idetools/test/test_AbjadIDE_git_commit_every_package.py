import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_git_commit_every_package_01():

    paths = [ide.PackagePath('red_score'), ide.PackagePath('blue_score')]

    input_ = 'ci* Updated. q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert 'Commit message]> Updated.' in transcript
    for path in paths:
        assert f'Git commit {path.wrapper} ...' in transcript
