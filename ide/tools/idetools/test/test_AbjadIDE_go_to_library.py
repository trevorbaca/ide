import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_library_01():
    r'''From material directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('red~score mm tempi lib q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : tempi',
        'Abjad IDE : library',
        ]


def test_AbjadIDE_go_to_library_02():
    r'''From segment directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('red~score gg A lib q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Abjad IDE : library',
        ]


def test_AbjadIDE_go_to_library_03():
    r'''From score directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('red~score lib q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Abjad IDE : library',
        ]


def test_AbjadIDE_go_to_library_04():
    r'''From scores directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('lib q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Abjad IDE : library',
        ]
