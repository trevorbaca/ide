import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_git_pull_01():
    r'''Available everywhere except scores directory.
    '''

    path = ide.Path('red_score')

    abjad_ide('? q')
    transcript = abjad_ide.io_manager.transcript
    assert 'git - pull (pull)' not in transcript

    abjad_ide('red~score pull q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Git pull {path.wrapper} ...' in transcript

    abjad_ide('red~score bb pull q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Git pull {path.wrapper} ...' in transcript

    abjad_ide('red~score dd pull q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Git pull {path.wrapper} ...' in transcript

    abjad_ide('red~score ee pull q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Git pull {path.wrapper} ...' in transcript

    abjad_ide('red~score gg pull q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Git pull {path.wrapper} ...' in transcript

    abjad_ide('red~score gg A pull q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Git pull {path.wrapper} ...' in transcript

    abjad_ide('red~score mm pull q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Git pull {path.wrapper} ...' in transcript

    abjad_ide('red~score mm magic pull q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Git pull {path.wrapper} ...' in transcript

    abjad_ide('red~score oo pull q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Git pull {path.wrapper} ...' in transcript

    abjad_ide('red~score tt pull q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Git pull {path.wrapper} ...' in transcript

    abjad_ide('red~score yy pull q')
    transcript = abjad_ide.io_manager.transcript
    assert f'Git pull {path.wrapper} ...' in transcript
