import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_segments_directory_01():
    """
    From material directory.
    """

    abjad_ide('red mm metronome gg q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : metronome_marks',
        'Red Score (2017) : segments',
        ]
    assert '.gitignore' not in transcript


def test_AbjadIDE_go_to_segments_directory_02():
    """
    From segment directory.
    """

    abjad_ide('red gg A gg q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : segments',
        ]


def test_AbjadIDE_go_to_segments_directory_03():
    """
    From score directory.
    """

    abjad_ide('red gg q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        ]


def test_AbjadIDE_go_to_segments_directory_04():
    """
    Makes sure reverse-order view is in effect.
    """

    abjad_ide('blu gg q')
    transcript = abjad_ide.io.transcript
    assert '1: A' in transcript
    assert '2: _' in transcript
