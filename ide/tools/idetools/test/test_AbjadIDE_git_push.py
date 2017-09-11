import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_git_push_01():
    r'''Available everywhere except scores directory.
    '''

    path = ide.Path('red_score')

    abjad_ide('? q')
    transcript = abjad_ide.io.transcript
    assert 'git - push (push)' not in transcript

    abjad_ide('red~score push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper} ...' in transcript

    abjad_ide('red~score bb push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper} ...' in transcript

    abjad_ide('red~score dd push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper} ...' in transcript

    abjad_ide('red~score ee push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper} ...' in transcript

    abjad_ide('red~score gg push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper} ...' in transcript

    abjad_ide('red~score gg A push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper} ...' in transcript

    abjad_ide('red~score mm push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper} ...' in transcript

    abjad_ide('red~score mm magic push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper} ...' in transcript

    abjad_ide('red~score oo push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper} ...' in transcript

    abjad_ide('red~score tt push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper} ...' in transcript

    abjad_ide('red~score yy push q')
    transcript = abjad_ide.io.transcript
    assert f'Git push {path.wrapper} ...' in transcript


def test_AbjadIDE_git_push_02():
    r'''In library directory.
    '''

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('lib push q')
    transcript = abjad_ide.io.transcript
    root = ide.Path('/Users/trevorbaca/baca')
    assert f'Git push {root} ...' in transcript
