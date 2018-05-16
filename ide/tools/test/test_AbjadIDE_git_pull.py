import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_git_pull_01():
    r'''In score directories.
    '''

    path = ide.Path('red_score')

    abjad_ide('red pull q')
    transcript = abjad_ide.io.transcript
    assert f'Git pull {path.wrapper()} ...' in transcript

    abjad_ide('red bb pull q')
    transcript = abjad_ide.io.transcript
    assert f'Git pull {path.wrapper()} ...' in transcript

    abjad_ide('red dd pull q')
    transcript = abjad_ide.io.transcript
    assert f'Git pull {path.wrapper()} ...' in transcript

    abjad_ide('red ee pull q')
    transcript = abjad_ide.io.transcript
    assert f'Git pull {path.wrapper()} ...' in transcript

    abjad_ide('red gg pull q')
    transcript = abjad_ide.io.transcript
    assert f'Git pull {path.wrapper()} ...' in transcript

    abjad_ide('red gg A pull q')
    transcript = abjad_ide.io.transcript
    assert f'Git pull {path.wrapper()} ...' in transcript

    abjad_ide('red mm pull q')
    transcript = abjad_ide.io.transcript
    assert f'Git pull {path.wrapper()} ...' in transcript

    abjad_ide('red mm rpc pull q')
    transcript = abjad_ide.io.transcript
    assert f'Git pull {path.wrapper()} ...' in transcript

    abjad_ide('red oo pull q')
    transcript = abjad_ide.io.transcript
    assert f'Git pull {path.wrapper()} ...' in transcript

    abjad_ide('red tt pull q')
    transcript = abjad_ide.io.transcript
    assert f'Git pull {path.wrapper()} ...' in transcript

    abjad_ide('red yy pull q')
    transcript = abjad_ide.io.transcript
    assert f'Git pull {path.wrapper()} ...' in transcript


def test_AbjadIDE_git_pull_02():
    r'''In scores directory.
    '''

    abjad_ide('pull q')
    transcript = abjad_ide.io.transcript
    for path in [ide.Path('red_score'), ide.Path('blue_score')]:
        assert f'Git pull {path.wrapper()} ...' in transcript


def test_AbjadIDE_git_pull_03():
    r'''In library directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll pull q')
    transcript = abjad_ide.io.transcript
    root = ide.Path('/Users/trevorbaca/baca')
    assert f'Git pull {root} ...' in transcript
