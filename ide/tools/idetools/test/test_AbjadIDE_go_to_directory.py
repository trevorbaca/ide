import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_directory_01():
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


def test_AbjadIDE_go_to_directory_02():
    r'''Goes to assets directory.
    '''

    abjad_ide('red %_ass q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : builds : _assets (empty)' in transcript.titles


def test_AbjadIDE_go_to_directory_03():
    r'''Goes to build directory.
    '''

    abjad_ide('red %ette q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : builds : letter' in transcript.titles


def test_AbjadIDE_go_to_directory_04():
    r'''Goes to distribution directory.
    '''

    abjad_ide('red %istri q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : distribution' in transcript.titles


def test_AbjadIDE_go_to_directory_05():
    r'''Goes to etc directory.
    '''

    abjad_ide('red %etc q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : etc' in transcript.titles


def test_AbjadIDE_go_to_directory_06():
    r'''Goes to material directory.
    '''

    abjad_ide('red %rpc q')
    transcript = abjad_ide.io.transcript 
    line = 'Red Score (2017) : materials : red_pitch_classes'
    assert line in transcript.titles


def test_AbjadIDE_go_to_directory_07():
    r'''Goes to materials directory.
    '''

    abjad_ide('red %erial q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : materials' in transcript.titles


def test_AbjadIDE_go_to_directory_08():
    r'''Goes to segment directory.
    '''

    abjad_ide('red %A q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : segments : A' in transcript.titles


def test_AbjadIDE_go_to_directory_09():
    r'''Goes to segments directory.
    '''

    abjad_ide('red %egmen q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : segments' in transcript.titles


def test_AbjadIDE_go_to_directory_10():
    r'''Goes to stylesheet directory.
    '''

    abjad_ide('red %yles q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : stylesheets' in transcript.titles


def test_AbjadIDE_go_to_directory_11():
    r'''Goes to test directory.
    '''

    abjad_ide('red %est q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : test' in transcript.titles


def test_AbjadIDE_go_to_directory_12():
    r'''Goes to tools directory.
    '''

    abjad_ide('red %ool q')
    transcript = abjad_ide.io.transcript 
    assert 'Red Score (2017) : tools' in transcript.titles


def test_AbjadIDE_go_to_directory_13():
    r'''Handles numeric input.
    '''

    abjad_ide('red gg %0 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '%0' to 0 directories ..." in transcript

    abjad_ide('red gg %1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'segments', '_')
    assert f"Matching '%1' to {path.trim()} ..." in transcript

    abjad_ide('red gg %99 q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '%99' to 0 directories ..." in transcript


def test_AbjadIDE_go_to_directory_14():
    r'''Handles empty input and junk input.
    '''

    abjad_ide('% q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '%' to 0 directories ..." in transcript

    abjad_ide('%asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '%asdf' to 0 directories ..." in transcript


def test_AbjadIDE_go_to_directory_15():
    r'''Handles double input.
    '''

    abjad_ide('%% q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '%%' to 0 directories ..." in transcript

    abjad_ide('%%asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '%%asdf' to 0 directories ..." in transcript
