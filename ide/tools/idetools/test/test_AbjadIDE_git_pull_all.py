import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_git_pull_all_01():

    abjad_ide('pull* q')
    transcript = abjad_ide.io.transcript
    for path in [ide.Path('red_score'), ide.Path('blue_score')]:
        assert f'Git pull {path.wrapper()} ...' in transcript
