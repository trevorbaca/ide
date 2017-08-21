import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()
scores_directory = configuration.abjad_ide_example_scores_directory


def test_AbjadIDE_copy_01():
    r'''Into build subdirectory.
    '''

    source_file = pathlib.Path(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'front-cover.tex',
        )
    assert source_file.is_file()
    target_file = pathlib.Path(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'build',
        'letter-portrait',
        'front-cover.tex',
        )
    assert not target_file.exists()
    trimmed_source_file = abjad_ide._trim(source_file)

    with abjad.FilesystemState(keep=[scores_directory]):
        input_ = 'Blue~Example~Score bb letter-portrait cp more'
        input_ += ' {!s}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert target_file.exists()

    contents = abjad_ide._io_manager._transcript.contents
    header = 'Blue Example Score (2013) - build directory'
    header += ' - letter-portrait - select:'
    assert header in contents


def test_AbjadIDE_copy_02():
    r'''Into distribution directory.
    '''

    source_file = pathlib.Path(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'distribution',
        'red-example-score-score.pdf',
        )
    target_file = pathlib.Path(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'distribution',
        'red-example-score-score.pdf',
        )
    trimmed_source_file = abjad_ide._trim(source_file)

    with abjad.FilesystemState(keep=[scores_directory]):
        assert not target_file.exists()
        input_ = 'Blue~Example~Score dd cp more'
        input_ += ' {}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert target_file.exists()

    contents = abjad_ide._io_manager._transcript.contents
    string = 'Blue Example Score (2013) - distribution directory - select:'
    assert string in contents


def test_AbjadIDE_copy_03():
    r'''Into etc directory.
    '''

    source_file = pathlib.Path(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'etc',
        'notes.txt',
        )
    target_file = pathlib.Path(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'etc',
        'notes.txt',
        )
    trimmed_source_file = abjad_ide._trim(source_file)

    with abjad.FilesystemState(keep=[scores_directory]):
        assert not target_file.exists()
        input_ = 'Blue~Example~Score ee cp more'
        input_ += ' {!s}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert target_file.exists()

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - etc directory - select:' in contents


def test_AbjadIDE_copy_04():
    r'''Into tools directory.
    '''

    source_file = pathlib.Path(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'tools',
        'ScoreTemplate.py',
        )
    target_file = pathlib.Path(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'tools',
        'ScoreTemplate.py',
        )
    trimmed_source_file = abjad_ide._trim(source_file)

    with abjad.FilesystemState(keep=[scores_directory]):
        assert not target_file.exists()
        input_ = 'Blue~Example~Score oo cp more'
        input_ += ' {!s}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert target_file.exists()

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - tools directory - select:' in contents


def test_AbjadIDE_copy_05():
    r'''Into material directory.
    '''

    source_file = pathlib.Path(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        'definition.py',
        )
    target_file = pathlib.Path(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'materials',
        'articulation_handler',
        'definition.py',
        )
    trimmed_source_file = abjad_ide._trim(source_file)

    with abjad.FilesystemState(keep=[scores_directory]):
        target_file.unlink()
        assert not target_file.exists()
        input_ = 'Blue~Example~Score mm articulation~handler cp more'
        input_ += ' {!s}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert target_file.exists()

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - materials directory - articulation handler - select:' in contents


def test_AbjadIDE_copy_06():
    r'''Into materials directory.
    '''

    source_package = pathlib.Path(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    target_package = pathlib.Path(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'materials',
        'magic_numbers',
        )
    trimmed_source_package = abjad_ide._trim(source_package)

    with abjad.FilesystemState(keep=[scores_directory]):
        assert source_package.is_dir()
        assert not target_package.exists()
        input_ = 'Blue~Example~Score mm cp more'
        input_ += ' {!s}'.format(trimmed_source_package)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert target_package.exists()

    contents = abjad_ide._io_manager._transcript.contents
    string = 'Blue Example Score (2013) - materials directory - select:'
    assert string in contents


def test_AbjadIDE_copy_07():
    r'''Into segment directory.
    '''

    source_file = pathlib.Path(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        'definition.py',
        )
    target_file = pathlib.Path(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'segments',
        'segment_01',
        'definition.py',
        )
    trimmed_source_file = abjad_ide._trim(source_file)

    with abjad.FilesystemState(keep=[scores_directory]):
        target_file.unlink()
        assert not target_file.exists()
        input_ = 'Blue~Example~Score gg segment~01 cp more'
        input_ += ' {!s}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert target_file.exists()

    contents = abjad_ide._io_manager._transcript.contents
    string = 'Blue Example Score (2013) - segments directory - segment 01 - select:'
    assert string in contents


def test_AbjadIDE_copy_08():
    r'''Into segments directory.
    '''

    source_package = pathlib.Path(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_03',
        )
    target_package = pathlib.Path(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'segments',
        'segment_03',
        )
    trimmed_source_package = abjad_ide._trim(source_package)

    with abjad.FilesystemState(keep=[scores_directory]):
        assert source_package.is_dir()
        assert not target_package.exists()
        input_ = 'Blue~Example~Score gg cp more'
        input_ += ' {!s}'.format(trimmed_source_package)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert target_package.exists()

    contents = abjad_ide._io_manager._transcript.contents
    string = 'Blue Example Score (2013) - segments directory - select:'
    assert string in contents


def test_AbjadIDE_copy_09():
    r'''Preexisting segment directory doesn't break IDE.
    '''

    source_package = pathlib.Path(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_03',
        )
    trimmed_source_package = abjad_ide._trim(source_package)

    with abjad.FilesystemState(keep=[scores_directory]):
        assert source_package.is_dir()
        input_ = 'Red~Example~Score gg cp more'
        input_ += ' {!s}'.format(trimmed_source_package)
        input_ += ' q'
        abjad_ide._start(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'already exists' in contents


def test_AbjadIDE_copy_10():
    r'''Into stylesheets directory.
    '''

    source_file = pathlib.Path(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'stylesheets',
        'stylesheet.ily',
        )
    target_file = pathlib.Path(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'stylesheets',
        'stylesheet.ily',
        )
    trimmed_source_file = abjad_ide._trim(source_file)

    with abjad.FilesystemState(keep=[scores_directory]):
        assert not target_file.exists()
        input_ = 'Blue~Example~Score yy cp more'
        input_ += ' {!s}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert target_file.exists()

    contents = abjad_ide._io_manager._transcript.contents
    string = 'Blue Example Score (2013) - stylesheets directory - select:'
    assert string in contents


def test_AbjadIDE_copy_11():
    r'''Into test directory.
    '''

    source_file = pathlib.Path(
        scores_directory,
        'red_example_score',
        'red_example_score',
        'test',
        'test_dummy.py',
        )
    target_file = pathlib.Path(
        scores_directory,
        'blue_example_score',
        'blue_example_score',
        'test',
        'test_dummy.py',
        )
    trimmed_source_file = abjad_ide._trim(source_file)

    with abjad.FilesystemState(keep=[scores_directory]):
        assert not target_file.exists()
        input_ = 'Blue~Example~Score tt cp more'
        input_ += ' {!s}'.format(trimmed_source_file)
        input_ += ' y q'
        abjad_ide._start(input_=input_)
        assert target_file.exists()

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Blue Example Score (2013) - test directory - select:' in contents
