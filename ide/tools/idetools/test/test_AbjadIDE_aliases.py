import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_aliases_01():
    r'''From material directory.
    '''
    
    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('fab mm tempi sti q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Fabergé Investigations (2016)',
        'Fabergé Investigations (2016) : materials',
        'Fabergé Investigations (2016) : materials : tempi',
        'Stirrings Still (2017)'
        ]


def test_AbjadIDE_aliases_02():
    r'''From scores directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('sti q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Stirrings Still (2017)'
        ]
