import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_git_commit_01():
    r'''Available everywhere except scores directory.
    '''

    path = ide.Path('red_score')

    abjad_ide('? q')
    transcript = abjad_ide.io.transcript
    assert 'git - commit (ci)' not in transcript

    abjad_ide('red~score ci q')
    transcript = abjad_ide.io.transcript
    assert f'Git commit {path.wrapper()} ...' in transcript

    abjad_ide('red~score bb ci q')
    transcript = abjad_ide.io.transcript
    assert f'Git commit {path.wrapper()} ...' in transcript

    abjad_ide('red~score dd ci q')
    transcript = abjad_ide.io.transcript
    assert f'Git commit {path.wrapper()} ...' in transcript

    abjad_ide('red~score ee ci q')
    transcript = abjad_ide.io.transcript
    assert f'Git commit {path.wrapper()} ...' in transcript

    abjad_ide('red~score oo ci q')
    transcript = abjad_ide.io.transcript
    assert f'Git commit {path.wrapper()} ...' in transcript

    abjad_ide('red~score mm ci q')
    transcript = abjad_ide.io.transcript
    assert f'Git commit {path.wrapper()} ...' in transcript

    abjad_ide('red~score mm magic ci q')
    transcript = abjad_ide.io.transcript
    assert f'Git commit {path.wrapper()} ...' in transcript

    abjad_ide('red~score gg ci q')
    transcript = abjad_ide.io.transcript
    assert f'Git commit {path.wrapper()} ...' in transcript

    abjad_ide('red~score gg A ci q')
    transcript = abjad_ide.io.transcript
    assert f'Git commit {path.wrapper()} ...' in transcript

    abjad_ide('red~score yy ci q')
    transcript = abjad_ide.io.transcript
    assert f'Git commit {path.wrapper()} ...' in transcript

    abjad_ide('red~score tt ci q')
    transcript = abjad_ide.io.transcript
    assert f'Git commit {path.wrapper()} ...' in transcript


def test_AbjadIDE_git_commit_02():
    r'''In library directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll ci q')
    transcript = abjad_ide.io.transcript
    root = ide.Path('/Users/trevorbaca/baca')
    assert f'Git commit {root} ...' in transcript
