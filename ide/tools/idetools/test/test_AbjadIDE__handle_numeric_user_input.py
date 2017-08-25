import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE__handle_numeric_user_input_01():

    input_ = 'red~score dd 1 q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._session._attempted_to_open_file
