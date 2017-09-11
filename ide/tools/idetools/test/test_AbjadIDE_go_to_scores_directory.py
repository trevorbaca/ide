import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_scores_directory_01():
    r'''From material directory.
    '''

    abjad_ide('red~score mm tempi ss q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : tempi',
        'Abjad IDE : scores',
        ]
    assert '.gitignore' not in transcript


def test_AbjadIDE_go_to_scores_directory_02():
    r'''From segment directory.
    '''

    abjad_ide('red~score gg A ss q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Abjad IDE : scores',
        ]


def test_AbjadIDE_go_to_scores_directory_03():
    r'''From score directory.
    '''

    abjad_ide('red~score ss q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Abjad IDE : scores',
        ]


def test_AbjadIDE_go_to_scores_directory_04():
    r'''From home to home.
    '''

    abjad_ide('ss q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Abjad IDE : scores',
        ]
