import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_every_definition_file_01():
    r'''Edits every material definition.
    '''

    abjad_ide('red~score mm df* q')
    transcript = abjad_ide.io_manager.transcript
    for name in [
        'magic_numbers',
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ]:
        path = ide.Path('red_score').materials / name / 'definition.py'
        assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_every_definition_file_02():
    r'''Edits every segment definition.
    '''

    abjad_ide('red~score gg df* q')
    transcript = abjad_ide.io_manager.transcript
    for name in [
        'segment_01',
        'segment_02',
        'segment_03',
        ]:
        path = ide.Path('red_score').segments / name / 'definition.py'
        assert f'Editing {path.trim()} ...' in transcript
