import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_git_push_01():
    r'''Available everywhere except scores directory.
    '''

    path = ide.Path('red_score')

    abjad_ide('? q')
    transcript = abjad_ide.io.transcript
    assert 'git - push (push)' not in transcript

    abjad_ide('red push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper()} ...' in transcript

    abjad_ide('red bb push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper()} ...' in transcript

    abjad_ide('red dd push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper()} ...' in transcript

    abjad_ide('red ee push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper()} ...' in transcript

    abjad_ide('red gg push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper()} ...' in transcript

    abjad_ide('red gg A push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper()} ...' in transcript

    abjad_ide('red mm push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper()} ...' in transcript

    abjad_ide('red mm magic push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper()} ...' in transcript

    abjad_ide('red oo push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper()} ...' in transcript

    abjad_ide('red tt push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper()} ...' in transcript

    abjad_ide('red yy push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper()} ...' in transcript


def test_AbjadIDE_git_push_02():
    r'''In library directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll push q')
    transcript = abjad_ide.io.transcript
    root = ide.Path('/Users/trevorbaca/baca')
    assert f'Git push {root} ...' in transcript
