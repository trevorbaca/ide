import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_git_status_every_package_01():

    input_ = 'st* q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._session._attempted_method == 'git_status'

    input_ = 'red~score st* q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert "Unknown command: 'st*'." in transcript
