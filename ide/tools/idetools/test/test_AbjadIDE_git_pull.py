import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_git_pull_01():
    r'''Available everywhere except scores directory.
    '''

    path = ide.PackagePath('red_score')

    input_ = '? q'
    abjad_ide._start(input_=input_)
    assert 'git - pull (pull)' not in abjad_ide._transcript

    input_ = 'red~score pull q'
    abjad_ide._start(input_=input_)
    assert f'Git pull {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score bb pull q'
    abjad_ide._start(input_=input_)
    assert f'Git pull {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score dd pull q'
    abjad_ide._start(input_=input_)
    assert f'Git pull {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score ee pull q'
    abjad_ide._start(input_=input_)
    assert f'Git pull {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score gg pull q'
    abjad_ide._start(input_=input_)
    assert f'Git pull {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score gg A pull q'
    abjad_ide._start(input_=input_)
    assert f'Git pull {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score mm pull q'
    abjad_ide._start(input_=input_)
    assert f'Git pull {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score mm magic~numbers pull q'
    abjad_ide._start(input_=input_)
    assert f'Git pull {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score oo pull q'
    abjad_ide._start(input_=input_)
    assert f'Git pull {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score tt pull q'
    abjad_ide._start(input_=input_)
    assert f'Git pull {path.wrapper} ...' in abjad_ide._transcript

    input_ = 'red~score yy pull q'
    abjad_ide._start(input_=input_)
    assert f'Git pull {path.wrapper} ...' in abjad_ide._transcript
