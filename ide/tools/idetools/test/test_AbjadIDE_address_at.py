import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_address_at_01():
    r'''Addresses distribution file.
    '''

    abjad_ide('red~score @ram-not q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').distribution / 'red-score-program-notes.txt'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_02():
    r'''Address etc file.
    '''

    abjad_ide('red~score @notes.txt q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').etc / 'notes.txt'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_03():
    r'''Addresses external file.
    '''

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('cdi @ath q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('/Users/trevorbaca/abjad-ide/ide/tools/idetools/Path.py')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_04():
    r'''Addresses library file.
    '''

    if not abjad_ide._test_external_directory():
        return

    path = ide.Path(abjad.abjad_configuration.composer_library_tools)
    path /= 'PitchArrayCell.py'

    abjad_ide('lib @PAC q')
    transcript = abjad_ide.io.transcript 
    assert f'Editing {path.trim()} ...' in transcript

    abjad_ide('lib @ACel q')
    transcript = abjad_ide.io.transcript 
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_05():
    r'''Addresses material definition file.
    '''

    abjad_ide('red~score @agic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').materials / 'magic_numbers' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_06():
    r'''Addresses material sibling definition file backwards.
    '''

    abjad_ide('red~score %magic @< q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').materials / 'time_signatures'
    path /= 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_07():
    r'''Addresses material sibling definition file forwards.
    '''

    abjad_ide('red~score %magic @> q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').materials / 'performers' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_08():
    r'''Addresses segment definition file.
    '''

    abjad_ide('red~score @1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segments / 'segment_01' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_09():
    r'''Addresses sibling segment definition file backwards.
    '''

    abjad_ide('red~score %A @< q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segments / 'segment_03' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_10():
    r'''Addresses sibling segment definition file forwards.
    '''

    abjad_ide('red~score %A @> q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segments / 'segment_02' / 'definition.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_11():
    r'''Addresses stylesheet.
    '''

    abjad_ide('red~score @ext-def q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').stylesheets / 'context-definitions.ily'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_12():
    r'''Addresses test file.
    '''

    abjad_ide('red~score @tm q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').test / 'test_materials.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_13():
    r'''Addresses tools classfile.
    '''

    abjad_ide('red~score @RM q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'RhythmMaker.py'
    assert f'Editing {path.trim()} ...' in transcript

    abjad_ide('red~score @ScT q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'ScoreTemplate.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_14():
    r'''Addresses tools functionfile.
    '''

    abjad_ide('red~score @ass q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools / 'adjust_spacing_sections.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_15():
    r'''Empty address and junk address.
    '''

    abjad_ide('@ q')
    transcript = abjad_ide.io.transcript 
    assert "Matches no file '@' ..." in transcript

    abjad_ide('@asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matches no file '@asdf' ..." in transcript
