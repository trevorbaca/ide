import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_address_percent_01():
    r'''To alias.
    '''

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('lib %sti q')
    transcript = abjad_ide.io.transcript 
    assert 'Abjad IDE : library' in transcript.titles
    assert 'Stirrings Still (2017)' in transcript.titles

    abjad_ide('lib %fab q')
    transcript = abjad_ide.io.transcript 
    assert 'Abjad IDE : library' in transcript.titles
    assert 'Fabergé Investigations (2016)' in transcript.titles


def test_AbjadIDE_address_percent_02():
    r'''To build directory.
    '''

    abjad_ide('red~score %ette q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : builds : letter' in transcript.titles


def test_AbjadIDE_address_percent_03():
    r'''To builds segments directory.
    '''

    abjad_ide('red~score %_seg q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : builds : _segments' in transcript.titles


def test_AbjadIDE_address_percent_04():
    r'''To distribution directory.
    '''

    abjad_ide('red~score %istri q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : distribution' in transcript.titles


def test_AbjadIDE_address_percent_05():
    r'''To etc directory.
    '''

    abjad_ide('red~score %etc q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : etc' in transcript.titles


def test_AbjadIDE_address_percent_06():
    r'''To material directory.
    '''

    abjad_ide('red~score %agic q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : materials : magic_numbers' in transcript.titles

    abjad_ide('red~score %mn q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : materials : magic_numbers' in transcript.titles


def test_AbjadIDE_address_percent_07():
    r'''To materials directory.
    '''

    abjad_ide('red~score %erial q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : materials' in transcript.titles


def test_AbjadIDE_address_percent_08():
    r'''To segment directory.
    '''

    abjad_ide('red~score %A q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : segments : A' in transcript.titles


def test_AbjadIDE_address_percent_09():
    r'''To segments directory.
    '''

    abjad_ide('red~score %egmen q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : segments' in transcript.titles


def test_AbjadIDE_address_percent_10():
    r'''To stylesheet directory.
    '''

    abjad_ide('red~score %yles q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : stylesheets' in transcript.titles


def test_AbjadIDE_address_percent_11():
    r'''To test directory.
    '''

    abjad_ide('red~score %est q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : test' in transcript.titles


def test_AbjadIDE_address_percent_12():
    r'''To tools directory.
    '''

    abjad_ide('red~score %ool q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : tools' in transcript.titles


def test_AbjadIDE_address_percent_13():
    r'''Empty address.
    '''

    abjad_ide('% q')
    transcript = abjad_ide.io.transcript 
    assert "Matches no directory '%' ..." in transcript


def test_AbjadIDE_address_percent_14():
    r'''Junk address.
    '''

    abjad_ide('%asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matches no directory '%asdf' ..." in transcript
