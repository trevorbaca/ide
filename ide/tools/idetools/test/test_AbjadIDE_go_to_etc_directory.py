import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_etc_directory_01():
    r'''From material directory.
    '''

    abjad_ide('red mm metronome ee q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : metronome_marks',
        'Red Score (2017) : etc',
        ]
    assert '.gitignore' not in transcript


def test_AbjadIDE_go_to_etc_directory_02():
    r'''From segment directory.
    '''

    abjad_ide('red gg A ee q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : etc',
        ]


def test_AbjadIDE_go_to_etc_directory_03():
    r'''From builds directory to etc directory.
    '''

    abjad_ide('red bb ee q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds',
        'Red Score (2017) : etc',
        ]
