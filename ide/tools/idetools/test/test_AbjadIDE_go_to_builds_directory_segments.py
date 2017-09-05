import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_builds_directory_segments_01():
    r'''From material directory.
    '''

    titles = [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : tempi',
        'Red Score (2017) : builds : _segments',
        ]

    abjad_ide('red~score mm tempi nn q')
    transcript = abjad_ide.io_manager.transcript
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_builds_directory_segments_02():
    r'''From segment directory.
    '''

    titles = [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : builds : _segments',
        ]

    abjad_ide('red~score gg A nn q')
    transcript = abjad_ide.io_manager.transcript
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_builds_directory_segments_03():
    r'''From score directory.
    '''

    abjad_ide('red~score nn q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds : _segments',
        ]


def test_AbjadIDE_go_to_builds_directory_segments_04():
    r'''From builds directory to builds directory.
    '''

    abjad_ide('red~score nn nn q')
    transcript = abjad_ide.io_manager.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds : _segments',
        'Red Score (2017) : builds : _segments',
        ]


def test_AbjadIDE_go_to_builds_directory_segments_05():
    r'''Git ignore file is hidden.
    '''

    abjad_ide('red~score nn q')
    transcript = abjad_ide.io_manager.transcript
    assert '.gitignore' not in transcript
