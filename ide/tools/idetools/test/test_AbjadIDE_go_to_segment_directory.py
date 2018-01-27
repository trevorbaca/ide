import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_segment_directory_01():
    r'''From material directory.
    '''

    abjad_ide('red %metro _ q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials : metronome_marks',
        'Red Score (2017) : segments : _',
        ]


def test_AbjadIDE_go_to_segment_directory_02():
    r'''From segment directory.
    '''

    abjad_ide('red _ A B q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments : _',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : segments : B',
        ]
