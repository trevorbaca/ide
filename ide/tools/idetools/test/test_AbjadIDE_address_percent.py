import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_address_percent_01():
    r'''Goes to aliased directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('ll %sti q')
    transcript = abjad_ide.io.transcript 
    assert 'Abjad IDE : library' in transcript.titles
    assert 'Stirrings Still (2017)' in transcript.titles

    abjad_ide('ll %fab q')
    transcript = abjad_ide.io.transcript 
    assert 'Abjad IDE : library' in transcript.titles
    assert 'Fabergé Investigations (2016)' in transcript.titles


def test_AbjadIDE_address_percent_02():
    r'''Goes to build directory.
    '''

    abjad_ide('red %ette q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : builds : letter' in transcript.titles


def test_AbjadIDE_address_percent_03():
    r'''Goes to builds segments directory.
    '''

    abjad_ide('red %_seg q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : builds : _segments' in transcript.titles


def test_AbjadIDE_address_percent_04():
    r'''Goes to distribution directory.
    '''

    abjad_ide('red %istri q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : distribution' in transcript.titles


def test_AbjadIDE_address_percent_05():
    r'''Goes to etc directory.
    '''

    abjad_ide('red %etc q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : etc' in transcript.titles


def test_AbjadIDE_address_percent_06():
    r'''Goes to material directory.
    '''

    abjad_ide('red %agic q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : materials : magic_numbers' in transcript.titles

    abjad_ide('red %mn q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : materials : magic_numbers' in transcript.titles


def test_AbjadIDE_address_percent_07():
    r'''Goes to materials directory.
    '''

    abjad_ide('red %erial q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : materials' in transcript.titles


def test_AbjadIDE_address_percent_08():
    r'''Goes to segment directory.
    '''

    abjad_ide('red %A q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : segments : A' in transcript.titles


def test_AbjadIDE_address_percent_09():
    r'''Goes to segments directory.
    '''

    abjad_ide('red %egmen q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : segments' in transcript.titles


def test_AbjadIDE_address_percent_10():
    r'''Goes to stylesheet directory.
    '''

    abjad_ide('red %yles q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : stylesheets' in transcript.titles


def test_AbjadIDE_address_percent_11():
    r'''Goes to test directory.
    '''

    abjad_ide('red %est q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : test' in transcript.titles


def test_AbjadIDE_address_percent_12():
    r'''Goes to tools directory.
    '''

    abjad_ide('red %ool q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : tools' in transcript.titles


def test_AbjadIDE_address_percent_13():
    r'''Handles numeric input.
    '''

    abjad_ide('red gg %0 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '%0' to no directories ..." in transcript

    abjad_ide('red gg %1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score').segments('A')
    assert f"Matching '%1' to {path.trim()} ..." in transcript

    abjad_ide('red gg %99 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '%99' to no directories ..." in transcript


def test_AbjadIDE_address_percent_14():
    r'''Handles empty input and junk input.
    '''

    abjad_ide('% q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '%' to no directories ..." in transcript

    abjad_ide('%% q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '%%' to no directories ..." in transcript

    abjad_ide('%asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '%asdf' to no directories ..." in transcript

    abjad_ide('%%asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '%%asdf' to no directories ..." in transcript
