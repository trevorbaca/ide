import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_build_subdirectory_01():

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - build directory - letter',
        ]

    input_ = 'red~score %letter q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles
    assert not abjad_ide._session._attempted_to_open_file
