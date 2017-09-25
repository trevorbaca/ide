import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_git_push_all_01():

    abjad_ide('push* q')
    transcript = abjad_ide.io.transcript
    for path in [ide.Path('red_score'), ide.Path('blue_score')]:
        assert f'Git push {path.wrapper()} ...' in transcript
