import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_Path_match_paths_01():
    r'''Handles numeric input.
    '''

    abjad_ide('red~score dd 1 q')
