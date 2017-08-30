import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_git_push_every_package_01():

    paths = [ide.PackagePath('red_score'), ide.PackagePath('blue_score')]

    input_ = 'push* q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    for path in paths:
        assert f'Git push {path.wrapper} ...' in transcript
