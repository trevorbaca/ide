import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_materials_directory_01():
    r'''From builds directory.
    '''

    abjad_ide('red~score bb mm q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds',
        'Red Score (2017) : materials',
        ]
