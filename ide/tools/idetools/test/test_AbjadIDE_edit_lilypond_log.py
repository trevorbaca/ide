import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_lilypond_log_01():

    input_ = 'red~score mm tempi lpg q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._session._attempted_to_open_file
