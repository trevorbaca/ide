import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_git_commit_every_package_01():

    input_ = 'ci* q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._session._attempted_method == 'git_commit_every_package'
