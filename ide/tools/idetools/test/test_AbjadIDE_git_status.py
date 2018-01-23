import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_git_status_01():
    r'''In score directories.
    '''

    path = ide.Path('red_score')

    abjad_ide('red st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red bb st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red dd st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red ee st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red gg st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red gg A st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red mm st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red mm rpc st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red oo st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red tt st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red yy st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript


def test_AbjadIDE_git_status_02():
    r'''In scores directory.
    '''

    abjad_ide('st q')
    transcript = abjad_ide.io.transcript
    for path in [ide.Path('red_score'), ide.Path('blue_score')]:
        assert f'Git status {path.wrapper()} ...' in transcript


def test_AbjadIDE_git_status_03():
    r'''In library directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll st q')
    transcript = abjad_ide.io.transcript
    root = ide.Path('/Users/trevorbaca/baca')
    assert f'Git status {root} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript
