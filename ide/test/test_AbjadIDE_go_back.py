import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_back_01():

    abjad_ide('red mm metronome oo - - q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : metronome_marks',
        'Red Score (2017) : tools',
        'Red Score (2017) : materials : metronome_marks',
        'Red Score (2017) : tools',
        ]


def test_AbjadIDE_go_back_02():

    abjad_ide('red gg A bb - - q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : builds',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : builds',
        ]


def test_AbjadIDE_go_back_03():

    abjad_ide('red - - - q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Abjad IDE : scores',
        ]


def test_AbjadIDE_go_back_04():
    """
    Regression: back manages scores directory rather than quitting.
    """

    abjad_ide('- q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Abjad IDE : scores',
        ]
