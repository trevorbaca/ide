import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_address_caret_01():
    r'''In contents directory.
    '''

    abjad_ide('red ^ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^' to no source files ..." in transcript

    abjad_ide('red ^^ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^^' to 11 source files ..." in transcript

    abjad_ide('red ^def q')
    transcript = abjad_ide.io.transcript 
    assert 'No unique match ...' in transcript
    assert "Matching '^def' to 8 source files ..." in transcript

    abjad_ide('red ^^def q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^^def' to 8 source files ..." in transcript

    abjad_ide('red ^magic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').materials('magic_numbers', 'definition.py')
    assert f"Matching '^magic' to {path.trim()} ..." in transcript

    abjad_ide('red ^^magic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').materials('magic_numbers', 'definition.py')
    assert f"Matching '^^magic' to {path.trim()} ..." in transcript

    abjad_ide('red ^A q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segments('A', 'definition.py')
    assert f"Matching '^A' to {path.trim()} ..." in transcript

    abjad_ide('red ^^A q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segments('A', 'definition.py')
    assert f"Matching '^^A' to {path.trim()} ..." in transcript

    abjad_ide('red ^ST q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('ScoreTemplate.py')
    assert f"Matching '^ST' to {path.trim()} ..." in transcript

    abjad_ide('red ^^ST q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('ScoreTemplate.py')
    assert f"Matching '^^ST' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_caret_02():
    r'''In external directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdi ^ath q')
    transcript = abjad_ide.io.transcript 
    path = ide.Configuration().ide_directory
    path = path('tools', 'idetools', 'Path.py')
    assert f"Matching '^ath' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_caret_03():
    r'''In library.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll ^ACel q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path(abjad.abjad_configuration.composer_library_tools)
    path = path('PitchArrayCell.py')
    assert f"Matching '^ACel' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_caret_04():
    r'''In materials directory.
    '''

    abjad_ide('red mm ^ q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '^' to no source files ..." in transcript

    abjad_ide('red mm ^^ q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '^^' to 5 source files ..." in transcript

    abjad_ide('red mm ^def q')
    transcript = abjad_ide.io.transcript 
    assert 'No unique match ...' in transcript
    assert f"Matching '^def' to 8 source files ..." in transcript

    abjad_ide('red mm ^^def q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '^^def' to 5 source files ..." in transcript

    abjad_ide('red mm ^magic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').materials('magic_numbers', 'definition.py')
    assert f"Matching '^magic' to {path.trim()} ..." in transcript

    abjad_ide('red mm ^^magic q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').materials('magic_numbers', 'definition.py')
    assert f"Matching '^^magic' to {path.trim()} ..." in transcript

    abjad_ide('red mm ^ST q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('ScoreTemplate.py')
    assert f"Matching '^ST' to {path.trim()} ..." in transcript

    abjad_ide('red mm ^^ST q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '^^ST' to no source files ..." in transcript


def test_AbjadIDE_address_caret_05():
    r'''In segments directory.
    '''

    abjad_ide('red gg ^ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^' to no source files ..." in transcript

    abjad_ide('red gg ^^ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^^' to 3 source files ..." in transcript

    abjad_ide('red gg ^def q')
    transcript = abjad_ide.io.transcript 
    assert 'No unique match ...' in transcript
    assert "Matching '^def' to 8 source files ..." in transcript

    abjad_ide('red gg ^^def q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^^def' to 3 source files ..." in transcript

    abjad_ide('red gg ^A q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segments('A', 'definition.py')
    assert f"Matching '^A' to {path.trim()} ..." in transcript

    abjad_ide('red gg ^^A q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segments('A', 'definition.py')
    assert f"Matching '^^A' to {path.trim()} ..." in transcript

    abjad_ide('red gg ^ST q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('ScoreTemplate.py')
    assert f"Matching '^ST' to {path.trim()} ..." in transcript

    abjad_ide('red gg ^^ST q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^^ST' to no source files ..." in transcript


def test_AbjadIDE_address_caret_06():
    r'''In test directory.
    '''

    abjad_ide('red tt ^ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^' to no source files ..." in transcript

    abjad_ide('red tt ^^ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^^' to no source files ..." in transcript

    abjad_ide('red tt ^tm q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '^tm' to no source files ..." in transcript


def test_AbjadIDE_address_caret_07():
    r'''In tools directory.
    '''

    abjad_ide('red oo ^ScT q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('ScoreTemplate.py')
    assert f"Matching '^ScT' to {path.trim()} ..." in transcript

    abjad_ide('red oo ^ass q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('adjust_spacing_sections.py')
    assert f"Matching '^ass' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_caret_08():
    r'''Handles single-prefix numeric input.
    '''

    abjad_ide('red oo ^0 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^0' to no source files ..." in transcript

    abjad_ide('red oo ^1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('RhythmMaker.py')
    assert f"Matching '^1' to {path.trim()} ..." in transcript

    abjad_ide('red oo ^99 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^99' to no source files ..." in transcript


def test_AbjadIDE_address_caret_09():
    r'''Handles double-prefix numeric input.
    '''

    abjad_ide('red oo ^^0 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^^0' to no source files ..." in transcript

    abjad_ide('red oo ^^1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('RhythmMaker.py')
    assert f"Matching '^^1' to {path.trim()} ..." in transcript

    abjad_ide('red oo ^^99 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^^99' to no source files ..." in transcript


def test_AbjadIDE_address_caret_10():
    r'''Emtpy and junk addresses.
    '''

    abjad_ide('^ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^' to no source files ..." in transcript

    abjad_ide('^asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^asdf' to no source files ..." in transcript

    abjad_ide('^^asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^^asdf' to no source files ..." in transcript
