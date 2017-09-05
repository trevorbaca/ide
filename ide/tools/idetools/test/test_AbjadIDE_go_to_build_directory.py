import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_build_directory_01():

    abjad_ide('red~score %letter q')
    transcript = abjad_ide._io_manager._transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds : letter',
        ]
