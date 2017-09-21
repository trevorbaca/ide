import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_illustrate_file_01():

    abjad_ide('red~score %magic ill q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').materials('magic_numbers')
    path /= '__illustrate__.py'
    assert f'Editing {path.trim()} ...' in transcript
