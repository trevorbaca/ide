import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_Path_match_package_path_01():
    r'''Handles numeric input.
    '''

    abjad_ide('red~score dd 1 q')
