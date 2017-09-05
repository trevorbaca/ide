import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_every_file_01():

    abjad_ide('red~score mm ff* definition.py q')
    transcript = abjad_ide.io_manager.transcript
    for name in (
        'magic_numbers', 
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ):
        path = ide.Path('red_score').materials / name / 'definition.py'
        assert f'Editing {path.trim()} ...' in transcript
