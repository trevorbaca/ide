import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_every_definition_file_01():
    r'''Edits every material definition.
    '''

    input_ = 'red~score mm df* q'
    abjad_ide._start(input_=input_)
    names = [
        'magic_numbers',
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ]
    for name in names:
        path = ide.PackagePath('red_score').materials / name / 'definition.py'
        assert f'Opening {path.trim()} ...' in abjad_ide._transcript


def test_AbjadIDE_edit_every_definition_file_02():
    r'''Edits every segment definition.
    '''

    input_ = 'red~score gg df* q'
    abjad_ide._start(input_=input_)
    names = [
        'segment_01',
        'segment_02',
        'segment_03',
        ]
    for name in names:
        path = ide.PackagePath('red_score').segments / name / 'definition.py'
        assert f'Opening {path.trim()} ...' in abjad_ide._transcript
