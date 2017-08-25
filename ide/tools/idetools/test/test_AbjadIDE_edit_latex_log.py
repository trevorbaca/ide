import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_latex_log_01():

    input_ = 'red~score mm tempi lxg q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._session._attempted_to_open_file
