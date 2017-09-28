import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_hop_to_next_package_01():
    r'''In materials directory.
    '''

    abjad_ide('red mm > > > q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : instruments',
        'Red Score (2017) : materials : metronome_marks',
        'Red Score (2017) : materials : ranges',
        ]


def test_AbjadIDE_hop_to_next_package_02():
    r'''In material directory.
    '''

    abjad_ide('red mm instruments > > q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : instruments',
        'Red Score (2017) : materials : metronome_marks',
        'Red Score (2017) : materials : ranges',
        ]


def test_AbjadIDE_hop_to_next_package_03():
    r'''In segments directory.
    '''

    abjad_ide('red gg > > > q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : _',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : segments : B',
        ]


def test_AbjadIDE_hop_to_next_package_04():
    r'''In segment directory.
    '''

    abjad_ide('red gg _ > > q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : _',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : segments : B',
        ]
