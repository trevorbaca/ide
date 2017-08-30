import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_git_commit_01():
    r'''Available everywhere except scores directory.
    '''

    path = ide.PackagePath('red_score')

    input_ = '? q'
    abjad_ide._start(input_=input_)
    assert 'git - commit (ci)' not in abjad_ide._transcript

    input_ = 'red~score ? ci q'
    abjad_ide._start(input_=input_)
    assert f'Git commit {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score bb ? ci q'
    abjad_ide._start(input_=input_)
    assert f'Git commit {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score dd ? ci q'
    abjad_ide._start(input_=input_)
    assert f'Git commit {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score ee ? ci q'
    abjad_ide._start(input_=input_)
    assert f'Git commit {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score oo ? ci q'
    abjad_ide._start(input_=input_)
    assert f'Git commit {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score mm ? ci q'
    abjad_ide._start(input_=input_)
    assert f'Git commit {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score mm magic~numbers ? ci q'
    abjad_ide._start(input_=input_)
    assert f'Git commit {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score gg ? ci q'
    abjad_ide._start(input_=input_)
    assert f'Git commit {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score gg A ? ci q'
    abjad_ide._start(input_=input_)
    assert f'Git commit {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score yy ? ci q'
    abjad_ide._start(input_=input_)
    assert f'Git commit {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score tt ? ci q'
    abjad_ide._start(input_=input_)
    assert f'Git commit {path.wrapper} ...' in abjad_ide._transcript
