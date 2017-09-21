import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_wrapper_directory_01():
    r'''From material directory.
    '''

    abjad_ide('red~score mm tempi ww q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : tempi',
        'Red Score (2017) : wrapper',
        ]
    assert 'red_score' in transcript
    assert '.gitignore' in transcript


def test_AbjadIDE_go_to_wrapper_directory_02():
    r'''From segment directory.
    '''

    abjad_ide('red~score gg A ww q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : wrapper',
        ]


def test_AbjadIDE_go_to_wrapper_directory_03():
    r'''From builds directory.
    '''


    abjad_ide('red~score bb ww q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds',
        'Red Score (2017) : wrapper',
        ]
