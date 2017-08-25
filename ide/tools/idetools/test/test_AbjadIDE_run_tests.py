import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_run_tests_01():

    input_ = 'red~score tests q'
    abjad_ide._start(input_=input_)
    #contents = abjad_ide._io_manager._transcript.contents

    assert abjad_ide._io_manager._session._attempted_method == '_run_pytest'
