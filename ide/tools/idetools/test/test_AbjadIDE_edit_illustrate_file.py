import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_illustrate_file_01():

    path = ide.PackagePath('red_score').materials / 'magic_numbers'
    path /= '__illustrate__.py'

    input_ = 'red~score %magic~numbers ill q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path.trim()} ...' in abjad_ide._transcript
