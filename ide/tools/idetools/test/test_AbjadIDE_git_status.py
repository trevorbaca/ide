import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_git_status_01():
    r'''Available everwhere except scores directory.
    '''

    path = ide.PackagePath('red_score')

    input_ = '? q'
    abjad_ide._start(input_=input_)
    assert 'git - status (st)' not in abjad_ide._transcript

    input_ = 'red~score ? st q'
    abjad_ide._start(input_=input_)
    assert f'Git status {path.wrapper} ...' in abjad_ide._transcript
    assert 'Git submodule foreach git fetch ...' in abjad_ide._transcript

    input_ = 'red~score bb ? st q'
    abjad_ide._start(input_=input_)
    assert f'Git status {path.wrapper} ...' in abjad_ide._transcript
    assert 'Git submodule foreach git fetch ...' in abjad_ide._transcript

    input_ = 'red~score dd ? st q'
    abjad_ide._start(input_=input_)
    assert f'Git status {path.wrapper} ...' in abjad_ide._transcript
    assert 'Git submodule foreach git fetch ...' in abjad_ide._transcript

    input_ = 'red~score ee ? st q'
    abjad_ide._start(input_=input_)
    assert f'Git status {path.wrapper} ...' in abjad_ide._transcript
    assert 'Git submodule foreach git fetch ...' in abjad_ide._transcript

    input_ = 'red~score gg ? st q'
    abjad_ide._start(input_=input_)
    assert f'Git status {path.wrapper} ...' in abjad_ide._transcript
    assert 'Git submodule foreach git fetch ...' in abjad_ide._transcript

    input_ = 'red~score gg A ? st q'
    abjad_ide._start(input_=input_)
    assert f'Git status {path.wrapper} ...' in abjad_ide._transcript
    assert 'Git submodule foreach git fetch ...' in abjad_ide._transcript

    input_ = 'red~score mm ? st q'
    abjad_ide._start(input_=input_)
    assert f'Git status {path.wrapper} ...' in abjad_ide._transcript
    assert 'Git submodule foreach git fetch ...' in abjad_ide._transcript

    input_ = 'red~score mm magic~numbers ? st q'
    abjad_ide._start(input_=input_)
    assert f'Git status {path.wrapper} ...' in abjad_ide._transcript
    assert 'Git submodule foreach git fetch ...' in abjad_ide._transcript

    input_ = 'red~score oo ? st q'
    abjad_ide._start(input_=input_)
    assert f'Git status {path.wrapper} ...' in abjad_ide._transcript
    assert 'Git submodule foreach git fetch ...' in abjad_ide._transcript

    input_ = 'red~score tt ? st q'
    abjad_ide._start(input_=input_)
    assert f'Git status {path.wrapper} ...' in abjad_ide._transcript
    assert 'Git submodule foreach git fetch ...' in abjad_ide._transcript

    input_ = 'red~score yy ? st q'
    abjad_ide._start(input_=input_)
    assert f'Git status {path.wrapper} ...' in abjad_ide._transcript
    assert 'Git submodule foreach git fetch ...' in abjad_ide._transcript
