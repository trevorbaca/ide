import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_smart_doctest_01():
    r'''In contents directory.
    '''

    abjad_ide('red ^ q')
    transcript = abjad_ide.io.transcript 
    assert "Missing '^' pattern ..." in transcript

    abjad_ide('red ^def q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^def' to 0 files ..." in transcript

    abjad_ide('red ^rpc q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path(
        'red_score', 'materials', 'red_pitch_classes', 'definition.py')
    assert f"Matching '^rpc' to {path.trim()} ..." in transcript

    abjad_ide('red ^A q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'segments', 'A', 'definition.py')
    assert f"Matching '^A' to {path.trim()} ..." in transcript

    abjad_ide('red ^ST q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'tools', 'ScoreTemplate.py')
    assert f"Matching '^ST' to {path.trim()} ..." in transcript


def test_AbjadIDE_smart_doctest_02():
    r'''In external directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdi ^ath q')
    transcript = abjad_ide.io.transcript 
    path = ide.Configuration().ide_directory
    path = path('tools', 'Path.py')
    assert f"Matching '^ath' to {path.trim()} ..." in transcript


def test_AbjadIDE_smart_doctest_03():
    r'''In library.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll ^ACel q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path(abjad.abjad_configuration.composer_library_tools)
    path = path('PitchArrayCell.py')
    assert f"Matching '^ACel' to {path.trim()} ..." in transcript


def test_AbjadIDE_smart_doctest_04():
    r'''In materials directory.
    '''

    abjad_ide('red mm ^ q')
    transcript = abjad_ide.io.transcript 
    assert "Missing '^' pattern ..." in transcript

    abjad_ide('red mm ^def q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '^def' to 0 files ..." in transcript

    abjad_ide('red mm ^rpc q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path(
        'red_score', 'materials', 'red_pitch_classes', 'definition.py')
    assert f"Matching '^rpc' to {path.trim()} ..." in transcript

    abjad_ide('red mm ^ST q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'tools', 'ScoreTemplate.py')
    assert f"Matching '^ST' to {path.trim()} ..." in transcript


def test_AbjadIDE_smart_doctest_05():
    r'''In segments directory.
    '''

    abjad_ide('red gg ^ q')
    transcript = abjad_ide.io.transcript 
    assert "Missing '^' pattern ..." in transcript

    abjad_ide('red gg ^def q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^def' to 0 files ..." in transcript

    abjad_ide('red gg ^A q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segments('A', 'definition.py')
    assert f"Matching '^A' to {path.trim()} ..." in transcript

    abjad_ide('red gg ^ST q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('ScoreTemplate.py')
    assert f"Matching '^ST' to {path.trim()} ..." in transcript


def test_AbjadIDE_smart_doctest_06():
    r'''In tools directory.
    '''

    abjad_ide('red oo ^ScT q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('ScoreTemplate.py')
    assert f"Matching '^ScT' to {path.trim()} ..." in transcript

    abjad_ide('red oo ^spacing q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'tools', 'adjust_spacing_sections.py')
    assert f"Matching '^spacing' to {path.trim()} ..." in transcript


def test_AbjadIDE_smart_doctest_07():
    r'''Handles numbers.
    '''

    abjad_ide('red oo ^0 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^0' to 0 files ..." in transcript

    abjad_ide('red oo ^1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').tools('RhythmMaker.py')
    assert f"Matching '^1' to {path.trim()} ..." in transcript

    abjad_ide('red oo ^99 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^99' to 0 files ..." in transcript


def test_AbjadIDE_smart_doctest_08():
    r'''Missing pattern.
    '''

    abjad_ide('^ q')
    transcript = abjad_ide.io.transcript 
    assert "Missing '^' pattern ..." in transcript


def test_AbjadIDE_smart_doctest_09():
    r'''Unmatched pattern.
    '''

    abjad_ide('^asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '^asdf' to 0 files ..." in transcript
