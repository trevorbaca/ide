import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_git_push_01():
    r'''Available everywhere except scores directory.
    '''

    path = ide.PackagePath('red_score')

    input_ = '? q'
    abjad_ide._start(input_=input_)
    assert 'git - push (push)' not in abjad_ide._transcript

    input_ = 'red~score push q'
    abjad_ide._start(input_=input_)
    assert f'Git push {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score bb push q'
    abjad_ide._start(input_=input_)
    assert f'Git push {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score dd push q'
    abjad_ide._start(input_=input_)
    assert f'Git push {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score ee push q'
    abjad_ide._start(input_=input_)
    assert f'Git push {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score gg push q'
    abjad_ide._start(input_=input_)
    assert f'Git push {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score gg A push q'
    abjad_ide._start(input_=input_)
    assert f'Git push {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score mm push q'
    abjad_ide._start(input_=input_)
    assert f'Git push {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score mm magic~numbers push q'
    abjad_ide._start(input_=input_)
    assert f'Git push {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score oo push q'
    abjad_ide._start(input_=input_)
    assert f'Git push {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score tt push q'
    abjad_ide._start(input_=input_)
    assert f'Git push {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score yy push q'
    abjad_ide._start(input_=input_)
    assert f'Git push {path.wrapper} ...' in abjad_ide._transcript
