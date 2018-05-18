import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_smart_edit_01():
    """
    Edits etc file.
    """

    abjad_ide('red @notes.txt q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'etc', 'notes.txt')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_smart_edit_02():
    """
    Edits external file.
    """

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdi @ath q')
    transcript = abjad_ide.io.transcript 
    directory = ide.Configuration().ide_directory
    path = directory / 'Path.py'
    assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_smart_edit_03():
    """
    Edits library file.
    """

    if not abjad_ide.test_baca_directories():
        return

    path = ide.Path(abjad.abjad_configuration.composer_library_tools)
    path_1 = path('PitchArrayCell.py')
    path_2 = path('PitchArrayColumn.py')

    abjad_ide('ll @PAC q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '@PAC' to 3 files ..." in transcript
    assert path_1.trim() in transcript.lines
    assert path_2.trim() in transcript.lines

    abjad_ide('ll @ACel q')
    transcript = abjad_ide.io.transcript 
    assert f'Editing {path_1.trim()} ...' in transcript


def test_AbjadIDE_smart_edit_04():
    """
    Edits material definition file.
    """

    abjad_ide('red @rpc q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path(
        'red_score', 'materials', 'red_pitch_classes', 'definition.py')
    assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_smart_edit_05():
    """
    Edits segment definition file.
    """

    abjad_ide('red @A q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'segments', 'A', 'definition.py')
    assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_smart_edit_06():
    """
    Edits stylesheet.
    """

    abjad_ide('red @contexts q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'stylesheets', 'contexts.ily')
    assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_smart_edit_07():
    """
    Edits tools files.
    """

    abjad_ide('red @RM q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'tools', 'RhythmMaker.py')
    assert f"Editing {path.trim()} ..." in transcript

    abjad_ide('red @ScT q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'tools', 'ScoreTemplate.py')
    assert f"Editing {path.trim()} ..." in transcript

    abjad_ide('red @spacing q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'tools', 'adjust_spacing_sections.py')
    assert f"Editing {path.trim()} ..." in transcript


def test_AbjadIDE_smart_edit_08():
    """
    Handles single-prefix numeric input.
    """

    abjad_ide('red mm @0 q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '@0' to 0 files ..." in transcript

    abjad_ide('red mm @1 q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('red_score', 'materials', 'instruments', 'definition.py')
    assert f"Editing {path.trim()} ..." in transcript

    abjad_ide('red mm @99 q')
    transcript = abjad_ide.io.transcript 
    assert f"Matching '@99' to 0 files ..." in transcript


def test_AbjadIDE_smart_edit_09():
    """
    Missing pattern.
    """

    abjad_ide('@ q')
    transcript = abjad_ide.io.transcript 
    assert "Missing '@' pattern ..." in transcript


def test_AbjadIDE_smart_edit_10():
    """
    Unmatched pattern.
    """

    abjad_ide('@asdf q')
    transcript = abjad_ide.io.transcript 
    assert "Matching '@asdf' to 0 files ..." in transcript


def test_AbjadIDE_smart_edit_11():
    """
    Matches file alias.
    """

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('@LAF q')
    transcript = abjad_ide.io.transcript 
    path = abjad.abjad_configuration.composer_library_tools
    path = ide.Path(path) / 'LibraryAF.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_smart_edit_12():
    """
    Matches directory alias.
    """

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('@aka q')
    transcript = abjad_ide.io.transcript 
    path = ide.Path('akasha')
    assert "Matching '@aka' to " in transcript
