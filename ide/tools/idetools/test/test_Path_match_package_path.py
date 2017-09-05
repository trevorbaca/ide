import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_Path_match_package_path_01():
    r'''Handles numeric input.
    '''

    abjad_ide('red~score dd 1 q')


def test_Path_match_package_path_02():
    r'''Handles empty addressing.
    '''

    abjad_ide('@ % ^ * q')
    transcript = abjad_ide.io_manager.transcript
    assert "Matches no path '@' ..." in transcript
    assert "Matches no path '%' ..." in transcript
    assert "Matches no path '^' ..." in transcript
    assert "Matches no path '*' ..." in transcript


def test_Path_match_package_path_03():
    r'''Handles missing addresses.
    '''

    abjad_ide('%letter')
    transcript = abjad_ide.io_manager.transcript
    assert "Matches no path '%letter' ..." in transcript
