import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_contents_directory_01():
    r'''From builds directory.
    '''

    abjad_ide('red bb cc q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds',
        'Red Score (2017)',
        ]


def test_AbjadIDE_go_to_contents_directory_02():
    r'''From interrupted getter.
    '''

    abjad_ide('red bb new cc q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds',
        'Red Score (2017)',
        ]


def test_AbjadIDE_go_to_contents_directory_03():
    r'''From material directory.
    '''

    abjad_ide('red mm metronome cc q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : metronome_marks',
        'Red Score (2017)',
        ]
    assert '.gitignore' not in transcript


def test_AbjadIDE_go_to_contents_directory_04():
    r'''From score directory.
    '''

    abjad_ide('red cc q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017)',
        ]


def test_AbjadIDE_go_to_contents_directory_05():
    r'''From scores directory with smart match.
    '''
    
    abjad_ide('lue q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Blue Score (2017)',
        ]

    abjad_ide('BSc q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Blue Score (2017)',
        ]


def test_AbjadIDE_go_to_contents_directory_06():
    r'''From segment directory.
    '''

    abjad_ide('red gg A cc q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017)',
        ]
