import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_git_update_01():
    r'''Available in all directories except scores directory.
    '''

    input_ = '? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'git - update (up)' not in contents

    input_ = 'red~score st ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'git - update (up)' in contents

    input_ = 'red~score bb ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'git - update (up)' in contents

    input_ = 'red~score dd ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'git - update (up)' in contents

    input_ = 'red~score ee ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'git - update (up)' in contents

    input_ = 'red~score oo ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'git - update (up)' in contents

    input_ = 'red~score mm ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'git - update (up)' in contents

    input_ = 'red~score mm magic~numbers ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'git - update (up)' in contents

    input_ = 'red~score gg ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'git - update (up)' in contents

    input_ = 'red~score gg A ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'git - update (up)' in contents

    input_ = 'red~score yy ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'git - update (up)' in contents

    input_ = 'red~score tt ? q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'git - update (up)' in contents
