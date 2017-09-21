import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_stylesheets_directory_01():
    r'''From material directory.
    '''

    abjad_ide('red~score mm tempi yy q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : tempi',
        'Red Score (2017) : stylesheets',
        ]
    assert '.gitignore' not in transcript


def test_AbjadIDE_go_to_stylesheets_directory_02():
    r'''From segment directory.
    '''

    abjad_ide('red~score gg A yy q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : stylesheets',
        ]


def test_AbjadIDE_go_to_stylesheets_directory_03():
    r'''From score directory.
    '''

    abjad_ide('red~score yy q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [ 
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : stylesheets',
        ]


def test_AbjadIDE_go_to_stylesheets_directory_04():
    r'''Goes from builds directory to stylesheets directory.
    '''

    abjad_ide('red~score bb yy q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds',
        'Red Score (2017) : stylesheets',
        ]
