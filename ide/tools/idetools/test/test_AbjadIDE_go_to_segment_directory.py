import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_segment_directory_01():
    r'''%-navigation.
    '''

    abjad_ide('red~score %A q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments : A',
        ]
    assert '.gitignore' not in transcript


def test_AbjadIDE_go_to_segment_directory_02():

    abjad_ide('red~score %X q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        ]
    assert "Matches no directory '%X' ..." in transcript


def test_AbjadIDE_go_to_segment_directory_03():
    r'''The %a should not catch tools/adjust_spacing_sections.py.
    '''

    abjad_ide('red~score %a q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        ]
    assert "Matches no directory '%a' ..." in transcript
