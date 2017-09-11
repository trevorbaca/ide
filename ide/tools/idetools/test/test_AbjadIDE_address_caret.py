import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_address_caret_01():
    r'''Library file.
    '''

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('lib ^PAC q')
    transcript = abjad_ide.io.transcript 
    path = abjad_ide._get_library() / 'PitchArrayCell.py'
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_02():
    r'''Material definition file.
    '''

    abjad_ide('red~score ^agic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').materials / 'magic_numbers' / 'definition.py'
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_03():
    r'''Segment definition file.
    '''

    abjad_ide('red~score ^1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segments / 'segment_01' / 'definition.py'
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_04():
    r'''Test file.
    '''

    abjad_ide('red~score ^tm q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').test / 'test_materials.py'
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_05():
    r'''Tools classfile.
    '''

    abjad_ide('red~score ^ScT q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'ScoreTemplate.py'
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_06():
    r'''Tools functionfile.
    '''

    abjad_ide('red~score ^ass q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'adjust_spacing_sections.py'
    assert f'Running doctest on {path.trim()} ...' in transcript


def test_AbjadIDE_address_caret_07():
    r'''Emtpy address.
    '''

    abjad_ide('^ q')
    transcript = abjad_ide.io.transcript 
    assert "Matches no Python file '^' ..." in transcript


def test_AbjadIDE_address_caret_08():
    r'''Unknown address.
    '''

    abjad_ide('^asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matches no Python file '^asdf' ..." in transcript
