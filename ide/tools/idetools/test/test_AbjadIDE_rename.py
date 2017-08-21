import abjad
import ide
import pathlib
import shutil
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_rename_01():
    r'''Renames score directory.
    '''

    path_100_outer = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'example_score_100',
        )
    path_100_inner = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'example_score_100',
        'example_score_100',
        )
    path_101_outer = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'example_score_101',
        )
    path_101_inner = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'example_score_101',
        'example_score_101',
        )

    paths = (
        path_100_outer,
        path_100_inner,
        path_101_outer,
        path_101_inner,
        )
    for path in paths:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(str(path))

    with abjad.FilesystemState(remove=[path_100_outer, path_101_outer]):
        input_ = 'new example~score~100 q'
        abjad_ide._start(input_=input_)
        assert path_100_outer.is_dir()
        assert path_100_inner.is_dir()
        title = 'Example Score 100'
        abjad_ide._add_metadatum(
            path_100_inner,
            'title',
            title,
            )
        input_ = 'ren Example~Score~100 example_score_101 y q'
        abjad_ide._start(input_=input_)
        assert not path_100_outer.exists()
        assert path_101_outer.is_dir()
        assert path_101_inner.is_dir()


def test_AbjadIDE_rename_02():
    r'''Renames material directory in score.
    '''

    old_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'test_material',
        )
    new_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'new_test_material',
        )

    paths = (
        old_path,
        new_path,
        )
    for path in paths:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(str(path))

    with abjad.FilesystemState(remove=[old_path, new_path]):
        input_ = 'red~example~score mm new test~material q'
        abjad_ide._start(input_=input_)
        assert old_path.is_dir()
        input_ = 'red~example~score mm ren test~material new~test~material y q'
        abjad_ide._start(input_=input_)
        assert not old_path.exists()
        assert new_path.is_dir()


def test_AbjadIDE_rename_03():
    r'''Renames segment directory.
    '''

    old_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_04',
        )
    new_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'renamed_segment_04',
        )

    new_input = 'red~example~score gg new segment~04 q'
    rename_input = 'red~example~score gg ren segment~04 renamed_segment_04 y q'

    paths = (
        old_path,
        new_path,
        )
    for path in paths:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(str(path))

    with abjad.FilesystemState(remove=[old_path, new_path]):
        abjad_ide._start(input_=new_input)
        assert old_path.is_dir()
        abjad_ide._start(input_=rename_input)
        assert not old_path.exists()
        assert new_path.is_dir()


def test_AbjadIDE_rename_04():
    r'''Renames segment directory with name metadatum.
    '''

    old_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_03',
        )
    new_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'renamed_segment_03',
        )

    input_ = 'red~example~score gg ren C renamed_segment_03 y q'

    with abjad.FilesystemState(keep=[old_path], remove=[new_path]):
        assert old_path.is_dir()
        abjad_ide._start(input_=input_)
        assert not old_path.exists()
        assert new_path.is_dir()


def test_AbjadIDE_rename_05():
    r'''Renames build subdirectory.
    '''

    old_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        )
    assert old_path.is_dir()
    new_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'standard-size',
        )

    rename_input = 'red~example~score bb ren letter-portrait standard-size y q'

    if new_path.exists():
        shutil.rmtree(str(new_path))

    with abjad.FilesystemState(keep=[old_path], remove=[new_path]):
        assert old_path.is_dir()
        abjad_ide._start(input_=rename_input)
        assert not old_path.exists()
        assert new_path.is_dir()


def test_AbjadIDE_rename_06():
    r'''Renames maker file.
    '''

    old_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'tools',
        'NewMaker.py',
        )
    new_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'tools',
        'RenamedMaker.py',
        )

    new_input = 'red~example~score oo new NewMaker.py q'
    rename_input = 'red~example~score oo ren NewMaker.py RenamedMaker.py y q'

    paths = (
        old_path,
        new_path,
        )
    for path in paths:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(str(path))

    with abjad.FilesystemState(remove=[old_path, new_path]):
        abjad_ide._start(input_=new_input)
        assert old_path.is_file()
        abjad_ide._start(input_=rename_input)
        assert not old_path.exists()
        assert new_path.is_file()


def test_AbjadIDE_rename_07():
    r'''Renames stylesheet.
    '''

    old_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'stylesheets',
        'new-stylesheet.ily',
        )
    new_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'stylesheets',
        'renamed-stylesheet.ily',
        )

    new_input = 'red~example~score yy new new-stylesheet.ily q'
    rename_input = 'red~example~score yy ren new-stylesheet.ily'
    rename_input += ' renamed-stylesheet.ily y q'

    paths = (
        old_path,
        new_path,
        )
    for path in paths:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(str(path))

    with abjad.FilesystemState(remove=[old_path, new_path]):
        abjad_ide._start(input_=new_input)
        assert old_path.is_file()
        abjad_ide._start(input_=rename_input)
        assert not old_path.exists()
        assert new_path.is_file()
