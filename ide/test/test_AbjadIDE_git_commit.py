import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_git_commit_01():
    """
    In score package directories.
    """

    path = ide.Path('red_score')

    abjad_ide('red ci q')
    transcript = abjad_ide.io.transcript
    assert f'Nothing to commit ...' in transcript

    abjad_ide('red bb ci q')
    transcript = abjad_ide.io.transcript
    assert f'Nothing to commit ...' in transcript

    abjad_ide('red dd ci q')
    transcript = abjad_ide.io.transcript
    assert f'Nothing to commit ...' in transcript

    abjad_ide('red ee ci q')
    transcript = abjad_ide.io.transcript
    assert f'Nothing to commit ...' in transcript

    abjad_ide('red oo ci q')
    transcript = abjad_ide.io.transcript
    assert f'Nothing to commit ...' in transcript

    abjad_ide('red mm ci q')
    transcript = abjad_ide.io.transcript
    assert f'Nothing to commit ...' in transcript

    abjad_ide('red mm rpc ci q')
    transcript = abjad_ide.io.transcript
    assert f'Nothing to commit ...' in transcript

    abjad_ide('red gg ci q')
    transcript = abjad_ide.io.transcript
    assert f'Nothing to commit ...' in transcript

    abjad_ide('red gg A ci q')
    transcript = abjad_ide.io.transcript
    assert f'Nothing to commit ...' in transcript

    abjad_ide('red yy ci q')
    transcript = abjad_ide.io.transcript
    assert f'Nothing to commit ...' in transcript

    abjad_ide('red tt ci q')
    transcript = abjad_ide.io.transcript
    assert f'Nothing to commit ...' in transcript


def test_AbjadIDE_git_commit_02():
    """
    In scores directory.
    """

    abjad_ide('ci Updated. q')
    transcript = abjad_ide.io.transcript
    assert 'Commit message> Updated.' in transcript
    for path in [ide.Path('red_score'), ide.Path('blue_score')]:
        assert f'{path.wrapper} ...' in transcript
        assert 'Nothing to commit ...' in transcript


def test_AbjadIDE_git_commit_03():
    """
    In library.
    """

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll ci q')
    transcript = abjad_ide.io.transcript
    root = ide.Path('/Users/trevorbaca/baca')
    assert 'Nothing to commit ...' in transcript
