import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_material_directory_01():

    abjad_ide('red~score %magic q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials : magic_numbers',
        ]
