import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_git_diff_all_01():
    r'''Available in scores directory only.
    '''

    abjad_ide('diff* q')
    transcript = abjad_ide.io.transcript
    for path in [ide.Path('red_score'), ide.Path('blue_score')]:
        assert f'Git diff {path.wrapper().trim()} ...' in transcript
