import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_address_plus_01():
    r'''In contents directory.
    '''

    abjad_ide('red + q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '+' to no test files ..." in transcript

    abjad_ide('red ++ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '++' to 2 test files ..." in transcript

    abjad_ide('red +def q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '+def' to no test files ..." in transcript

    abjad_ide('red ++def q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '++def' to no test files ..." in transcript

    abjad_ide('red +magic q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '+magic' to no test files ..." in transcript

    abjad_ide('red ++magic q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '++magic' to no test files ..." in transcript

    abjad_ide('red +A q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '+A' to no test files ..." in transcript

    abjad_ide('red ++A q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '++A' to no test files ..." in transcript

    abjad_ide('red +ST q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '+ST' to no test files ..." in transcript

    abjad_ide('red ++ST q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '++ST' to no test files ..." in transcript


def test_AbjadIDE_address_plus_02():
    r'''In external directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    path = ide.Configuration().ide_directory
    path = path('tools', 'idetools', 'test', 'test_Path_is_external.py')

    abjad_ide('cdi +ath q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '+ath' to {path.trim()} ..." in transcript

    abjad_ide('cdi ++ath q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '++ath' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_plus_03():
    r'''In library.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll +PAC q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '+PAC' to no test files ..." in transcript


def test_AbjadIDE_address_plus_04():
    r'''In test directory.
    '''

    abjad_ide('red tt + q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '+' to no test files ..." in transcript

    abjad_ide('red tt ++ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '++' to 2 test files ..." in transcript

    abjad_ide('red tt +tm q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').test('test_materials.py')
    assert f"Matching '+tm' to {path.trim()} ..." in transcript


def test_AbjadIDE_address_plus_05():
    r'''Handles single-prefix numeric input.
    '''

    abjad_ide('red tt +0 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '+0' to no test files ..." in transcript

    abjad_ide('red tt +1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').test('test_materials.py')
    assert f"Matching '+1' to {path.trim()} ..." in transcript

    abjad_ide('red tt +99 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '+99' to no test files ..." in transcript


def test_AbjadIDE_address_plus_06():
    r'''Handles double-prefix numeric input.
    '''

    abjad_ide('red tt ++0 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '++0' to no test files ..." in transcript

    abjad_ide('red tt ++1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').test('test_materials.py')
    assert f"Matching '++1' to {path.trim()} ..." in transcript

    abjad_ide('red tt ++99 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '++99' to no test files ..." in transcript


def test_AbjadIDE_address_plus_07():
    r'''Handles empty input and junk input.
    '''

    abjad_ide('+ q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '+' to no test files ..." in transcript

    abjad_ide('+asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '+asdf' to no test files ..." in transcript

    abjad_ide('++asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '++asdf' to no test files ..." in transcript
