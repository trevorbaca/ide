import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_address_at_01():
    r'''Edits etc file.
    '''

    abjad_ide('red @notes.txt q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'etc', 'notes.txt')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_address_at_02():
    r'''Edits external file.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdi @ath q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('/Users/trevorbaca/abjad-ide/ide/tools/idetools/Path.py')
    assert f"Matching '@ath' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_at_03():
    r'''Edits library file.
    '''

    if not abjad_ide.test_baca_directories():
        return

    path = ide.Path(abjad.abjad_configuration.composer_library_tools)
    path_1 = path('PitchArrayCell.py')
    path_2 = path('PitchArrayColumn.py')

    abjad_ide('ll @PAC q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '@PAC' to 2 files ..." in transcript
    assert path_1.trim() in transcript.lines
    assert path_2.trim() in transcript.lines
    assert f'Editing {path_1.trim()} ...' in transcript

    abjad_ide('ll @ACel q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '@ACel' to {path_1.trim()} ..." in transcript
    assert f'Editing {path_1.trim()} ...' in transcript


def test_AbjadIDE_address_at_04():
    r'''Edits material definition file.
    '''

    abjad_ide('red @agic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'materials', 'magic_numbers', 'definition.py')
    assert f"Matching '@agic' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_at_05():
    r'''Edits segment definition file.
    '''

    abjad_ide('red @A q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segments('A', 'definition.py')
    assert f"Matching '@A' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_at_06():
    r'''Edits stylesheet.
    '''

    abjad_ide('red @contexts q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').stylesheets('contexts.ily')
    assert f"Matching '@contexts' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_at_07():
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


def test_AbjadIDE_address_at_08():
    r'''Handles single-prefix numeric input.
    '''

    abjad_ide('red mm @0 q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '@0' to 0 files ..." in transcript

    abjad_ide('red mm @1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').materials('magic_numbers', 'definition.py')
    assert f"Matching '@1' to {path.trim()} ..." in transcript

    abjad_ide('red mm @99 q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '@99' to 0 files ..." in transcript


def test_AbjadIDE_address_at_09():
    r'''Handles empty input, junk input and nonfile input.
    '''

    abjad_ide('@ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@' to 0 files ..." in transcript

    abjad_ide('@asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@asdf' to 0 files ..." in transcript

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('@aka q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('akasha')
    assert f"Matching '@aka' to {path.trim()} ..." in transcript
    assert f'Not a file {path.trim()} ...' in transcript
