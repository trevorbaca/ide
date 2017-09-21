import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_git_status_01():
    r'''Available everwhere except scores directory.
    '''

    path = ide.Path('red_score')

    abjad_ide('? q')
    transcript = abjad_ide.io.transcript
    assert 'git - status (st)' not in transcript

    abjad_ide('red~score st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red~score bb st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red~score dd st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red~score ee st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red~score gg st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red~score gg A st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red~score mm st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red~score mm magic st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red~score oo st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red~score tt st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript

    abjad_ide('red~score yy st q')
    transcript = abjad_ide.io.transcript
    assert f'Git status {path.wrapper()} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript


def test_AbjadIDE_git_status_02():
    r'''In library directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('lib st q')
    transcript = abjad_ide.io.transcript
    root = ide.Path('/Users/trevorbaca/baca')
    assert f'Git status {root} ...' in transcript
    assert 'Git submodule foreach git fetch ...' in transcript
