import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_hop_to_previous_package_01():
    """
    In materials directory.
    """

    abjad_ide('red mm < < < q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : time_signatures',
        'Red Score (2017) : materials : red_pitch_classes',
        'Red Score (2017) : materials : ranges',
        ]


def test_AbjadIDE_hop_to_previous_package_02():
    """
    In material directory.
    """

    abjad_ide('red mm instruments < < q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : instruments',
        'Red Score (2017) : materials : time_signatures',
        'Red Score (2017) : materials : red_pitch_classes',
        ]


def test_AbjadIDE_hop_to_previous_package_03():
    """
    In segments directory.
    """

    abjad_ide('red gg < < < q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : B',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : segments : _',
        ]


def test_AbjadIDE_hop_to_previous_package_04():
    """
    In segment directory.
    """

    abjad_ide('red gg _ < < q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : _',
        'Red Score (2017) : segments : B',
        'Red Score (2017) : segments : A',
        ]

