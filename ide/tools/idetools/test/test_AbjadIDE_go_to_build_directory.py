import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_build_directory_01():

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - builds directory - letter',
        ]

    input_ = 'red~score %letter q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles
