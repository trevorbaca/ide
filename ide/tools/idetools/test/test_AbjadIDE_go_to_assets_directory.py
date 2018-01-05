import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_assets_directory_01():
    r'''From material directory.
    '''


    abjad_ide('red mm metronome aa q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : metronome_marks',
        'Red Score (2017) : builds : _assets (empty)',
        ]
    assert '.gitignore' not in transcript


def test_AbjadIDE_go_to_assets_directory_02():
    r'''From segment directory.
    '''


    abjad_ide('red gg A aa q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : builds : _assets (empty)',
        ]


def test_AbjadIDE_go_to_assets_directory_03():
    r'''From score directory.
    '''

    abjad_ide('red aa q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds : _assets (empty)',
        ]


def test_AbjadIDE_go_to_assets_directory_04():
    r'''From builds directory to builds directory.
    '''

    abjad_ide('red aa aa q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds : _assets (empty)',
        'Red Score (2017) : builds : _assets (empty)',
        ]


def test_AbjadIDE_go_to_assets_directory_05():
    r'''Git ignore file is hidden.
    '''

    abjad_ide('red aa q')
    transcript = abjad_ide.io.transcript
    assert '.gitignore' not in transcript
