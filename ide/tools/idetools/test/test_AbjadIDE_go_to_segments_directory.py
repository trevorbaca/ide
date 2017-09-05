import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_segments_directory_01():
    r'''From material directory.
    '''

    abjad_ide('red~score mm tempi gg q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : tempi',
        'Red Score (2017) : segments',
        ]


def test_AbjadIDE_go_to_segments_directory_02():
    r'''From segment directory.
    '''

    abjad_ide('red~score gg A gg q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : segments',
        ]


def test_AbjadIDE_go_to_segments_directory_03():
    r'''From score directory.
    '''

    abjad_ide('red~score gg q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        ]


def test_AbjadIDE_go_to_segments_directory_04():
    r'''Makes sure reverse-order view is in effect.
    '''

    abjad_ide('blue~score gg q')
    transcript = abjad_ide.io_manager.transcript
    assert '1: segment_02' in transcript
    assert '2: segment_01' in transcript
