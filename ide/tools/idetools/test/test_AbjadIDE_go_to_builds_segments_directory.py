import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_builds_segments_directory_01():
    r'''From material directory.
    '''


    abjad_ide('red mm tempi nn q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : tempi',
        'Red Score (2017) : builds : _segments',
        ]
    assert '.gitignore' not in transcript


def test_AbjadIDE_go_to_builds_segments_directory_02():
    r'''From segment directory.
    '''


    abjad_ide('red gg A nn q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : builds : _segments',
        ]


def test_AbjadIDE_go_to_builds_segments_directory_03():
    r'''From score directory.
    '''

    abjad_ide('red nn q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds : _segments',
        ]


def test_AbjadIDE_go_to_builds_segments_directory_04():
    r'''From builds directory to builds directory.
    '''

    abjad_ide('red nn nn q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds : _segments',
        'Red Score (2017) : builds : _segments',
        ]


def test_AbjadIDE_go_to_builds_segments_directory_05():
    r'''Git ignore file is hidden.
    '''

    abjad_ide('red nn q')
    transcript = abjad_ide.io.transcript
    assert '.gitignore' not in transcript
