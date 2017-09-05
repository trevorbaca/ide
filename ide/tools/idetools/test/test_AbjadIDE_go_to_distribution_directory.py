import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_distribution_directory_01():
    r'''From material directory.
    '''

    abjad_ide('red~score mm tempi dd q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : tempi',
        'Red Score (2017) : distribution',
        ]


def test_AbjadIDE_go_to_distribution_directory_02():
    r'''From segment directory.
    '''

    abjad_ide('red~score gg A dd q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : distribution',
        ]


def test_AbjadIDE_go_to_distribution_directory_03():
    r'''From score directory.
    '''

    abjad_ide('red~score dd q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : distribution',
        ]


def test_AbjadIDE_go_to_distribution_directory_04():
    r'''From builds directory to distribution directory.
    '''

    abjad_ide('red~score bb dd q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds',
        'Red Score (2017) : distribution',
        ]
