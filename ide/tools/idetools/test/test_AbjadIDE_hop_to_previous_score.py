import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_hop_to_previous_score_01():
    r'''In materials directory.
    '''

    abjad_ide('red mm << << << q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Blue Score (2017)',
        'Red Score (2017)',
        'Blue Score (2017)',
        ]


def test_AbjadIDE_hop_to_previous_score_02():
    r'''In scores directory.
    '''

    abjad_ide('<< << << q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Blue Score (2017)',
        'Red Score (2017)',
        ]
