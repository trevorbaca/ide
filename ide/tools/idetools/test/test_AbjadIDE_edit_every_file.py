import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_every_file_01():

    abjad_ide('red~score mm ff* definition.py q')
    transcript = abjad_ide.io.transcript
    for name in (
        'magic_numbers', 
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ):
        path = ide.Path('red_score').materials / name / 'definition.py'
        assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_every_file_02():

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('cdk ff* _foo.txt q')
    transcript = abjad_ide.io.transcript
    assert "Missing '_foo.txt' files ..." in transcript
