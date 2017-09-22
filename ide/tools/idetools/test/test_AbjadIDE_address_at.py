import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_address_at_01():
    r'''Matches distribution file.
    '''

    abjad_ide('red @ram-not q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').distribution('red-score-program-notes.txt')
    assert f"Matching '@ram-not' to {path.trim()} ..." in transcript


# TODO: make this work again
#def test_AbjadIDE_address_at_02():
#    r'''Address etc file.
#    '''
#
#    abjad_ide('red @notes.txt q')
#    transcript = abjad_ide.io.transcript 
#    path = ide.Path('red_score').etc('notes.txt')
#    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_03():
    r'''Edits external file.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdi @ath q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('/Users/trevorbaca/abjad-ide/ide/tools/idetools/Path.py')
    assert f"Matching '@ath' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_at_04():
    r'''Edits library file.
    '''

    if not abjad_ide.test_baca_directories():
        return

    path = ide.Path(abjad.abjad_configuration.composer_library_tools)
    path_1 = path('PitchArrayCell.py')
    path_2 = path('PitchArrayColumn.py')

    abjad_ide('ll @PAC q')
    transcript = abjad_ide.io.transcript 
    assert 'No unique match ...' in transcript
    assert f"Matching '@PAC' to 2 files ..." in transcript
    assert f'{path_1.trim()} ...' in transcript
    assert f'{path_2.trim()} ...' in transcript

    abjad_ide('ll @ACel q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '@ACel' to {path_1.trim()} ..." in transcript


def test_AbjadIDE_address_at_05():
    r'''Edits material definition files.
    '''

    abjad_ide('red @agic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').materials('magic_numbers', 'definition.py')
    assert f"Matching '@agic' to {path.trim()} ..." in transcript

    abjad_ide('red mm @@fini q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@@fini' to 5 files ..." in transcript
    for name in [
        'magic_numbers',
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ]:
        path = ide.Path('red_score').materials(name, 'definition.py')
        assert f'{path.trim()} ...' in transcript

    abjad_ide('red mm @@ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@@' to 8 files ..." in transcript


def test_AbjadIDE_address_at_06():
    r'''Edits material definition file siblings.
    '''

    abjad_ide('red %magic @< q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').materials('time_signatures', 'definition.py')
    assert f"Matching '@<' to {path.trim()} ..." in transcript

    abjad_ide('red %magic @> q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').materials('performers', 'definition.py')
    assert f"Matching '@>' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_at_07():
    r'''Edits segment definition files.
    '''

    abjad_ide('red @1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segments('segment_01', 'definition.py')
    assert f"Matching '@1' to {path.trim()} ..." in transcript

    abjad_ide('red gg @@efin q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@@efin' to 3 files ..." in transcript
    for name in [
        'segment_01',
        'segment_02',
        'segment_03',
        ]:
        path = ide.Path('red_score').segments(name, 'definition.py')
        assert f'{path.trim()} ...' in transcript

    abjad_ide('red gg @@ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@@' to 6 files ..." in transcript


def test_AbjadIDE_address_at_08():
    r'''Edits sibling segment definition files.
    '''

    abjad_ide('red %A @< q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segments('segment_03', 'definition.py')
    assert f"Matching '@<' to {path.trim()} ..." in transcript

    abjad_ide('red %A @> q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').segments('segment_02', 'definition.py')
    assert f"Matching '@>' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_at_09():
    r'''Edits stylesheet.
    '''

    abjad_ide('red @contexts q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').stylesheets('contexts.ily')
    assert f"Matching '@contexts' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_at_10():
    r'''Edits test file.
    '''

    abjad_ide('red @tm q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').test('test_materials.py')
    assert f"Matching '@tm' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_at_11():
    r'''Edits tools files.
    '''

    abjad_ide('red @RM q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('RhythmMaker.py')
    assert f"Matching '@RM' to {path.trim()} ..." in transcript

    abjad_ide('red @ScT q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('ScoreTemplate.py')
    assert f"Matching '@ScT' to {path.trim()} ..." in transcript

    abjad_ide('red @ass q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('adjust_spacing_sections.py')
    assert f"Matching '@ass' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_at_12():
    r'''Handles empty input, junk input and nonfile input.
    '''

    abjad_ide('@ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@' to no files ..." in transcript

    abjad_ide('@asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@asdf' to no files ..." in transcript

    abjad_ide('@@asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@@asdf' to no files ..." in transcript

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('@aka q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('akasha')
    assert f"Matching '@aka' to {path.trim()} ..." in transcript
    assert f'Not a file {path.trim()} ...' in transcript
