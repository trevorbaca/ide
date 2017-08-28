import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_git_status_01():
    r'''Available everwhere except scores directory.
    '''

    input_ = '? q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert 'git - status (st)' not in transcript

    input_ = 'red~score ? st q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert 'git - status (st)' in transcript
    assert abjad_ide._session._attempted_method == 'git_status'

    input_ = 'red~score bb ? st q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert 'git - status (st)' in transcript
    assert abjad_ide._session._attempted_method == 'git_status'

    input_ = 'red~score dd ? st q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert 'git - status (st)' in transcript
    assert abjad_ide._session._attempted_method == 'git_status'

    input_ = 'red~score ee ? st q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert 'git - status (st)' in transcript
    assert abjad_ide._session._attempted_method == 'git_status'

    input_ = 'red~score gg ? st q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert 'git - status (st)' in transcript
    assert abjad_ide._session._attempted_method == 'git_status'

    input_ = 'red~score gg A ? st q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert 'git - status (st)' in transcript
    assert abjad_ide._session._attempted_method == 'git_status'

    input_ = 'red~score mm ? st q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert 'git - status (st)' in transcript
    assert abjad_ide._session._attempted_method == 'git_status'

    input_ = 'red~score mm magic~numbers ? st q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert 'git - status (st)' in transcript
    assert abjad_ide._session._attempted_method == 'git_status'

    input_ = 'red~score oo ? st q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert 'git - status (st)' in transcript
    assert abjad_ide._session._attempted_method == 'git_status'

    input_ = 'red~score tt ? st q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert 'git - status (st)' in transcript
    assert abjad_ide._session._attempted_method == 'git_status'

    input_ = 'red~score yy ? st q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert 'git - status (st)' in transcript
    assert abjad_ide._session._attempted_method == 'git_status'
