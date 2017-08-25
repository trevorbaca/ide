import abjad
import ide
import pathlib
import shutil
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_rename_01():
    r'''Renames score directory.
    '''

    path_100_wrapper_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'example_score_100',
        )
    path_100_contents_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'example_score_100',
        'example_score_100',
        )
    path_101_wrapper_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'example_score_101',
        )
    path_101_contents_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'example_score_101',
        'example_score_101',
        )

    paths = (
        path_100_wrapper_directory,
        path_100_contents_directory,
        path_101_wrapper_directory,
        path_101_contents_directory,
        )
    for path in paths:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(str(path))

    with ide.Test():
        input_ = 'new example~score~100 q'
        abjad_ide._start(input_=input_)
        assert path_100_wrapper_directory.is_dir()
        assert path_100_contents_directory.is_dir()
        title = 'Example Score 100'
        abjad_ide._add_metadatum(
            path_100_contents_directory,
            'title',
            title,
            )
        input_ = 'ren Example~Score~100 example_score_101 y q'
        abjad_ide._start(input_=input_)
        assert not path_100_wrapper_directory.exists()
        assert path_101_wrapper_directory.is_dir()
        assert path_101_contents_directory.is_dir()


def test_AbjadIDE_rename_02():
    r'''Renames material directory in score.
    '''

    old_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'test_material',
        )
    new_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
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

    with ide.Test():
        input_ = 'red~score mm new test~material q'
        abjad_ide._start(input_=input_)
        assert old_path.is_dir()
        input_ = 'red~score mm ren test~material new~test~material y q'
        abjad_ide._start(input_=input_)
        assert not old_path.exists()
        assert new_path.is_dir()


def test_AbjadIDE_rename_03():
    r'''Renames segment directory.
    '''

    old_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'segments',
        'segment_04',
        )
    new_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'segments',
        'renamed_segment_04',
        )

    new_input = 'red~score gg new segment~04 q'
    rename_input = 'red~score gg ren segment~04 renamed_segment_04 y q'

    paths = (
        old_path,
        new_path,
        )
    for path in paths:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(str(path))

    with ide.Test():
        abjad_ide._start(input_=new_input)
        assert old_path.is_dir()
        abjad_ide._start(input_=rename_input)
        assert not old_path.exists()
        assert new_path.is_dir()


def test_AbjadIDE_rename_04():
    r'''Renames segment directory with name metadatum.
    '''

    old_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'segments',
        'segment_03',
        )
    new_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'segments',
        'renamed_segment_03',
        )

    input_ = 'red~score gg ren C renamed_segment_03 y q'

    with ide.Test():
        assert old_path.is_dir()
        abjad_ide._start(input_=input_)
        assert not old_path.exists()
        assert new_path.is_dir()


def test_AbjadIDE_rename_05():
    r'''Renames build subdirectory.
    '''

    old_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'letter',
        )
    assert old_path.is_dir()
    new_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        'standard-size',
        )

    rename_input = 'red~score bb ren letter standard-size y q'

    if new_path.exists():
        shutil.rmtree(str(new_path))

    with ide.Test():
        assert old_path.is_dir()
        abjad_ide._start(input_=rename_input)
        assert not old_path.exists()
        assert new_path.is_dir()


def test_AbjadIDE_rename_06():
    r'''Renames maker file.
    '''

    old_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'tools',
        'NewMaker.py',
        )
    new_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'tools',
        'RenamedMaker.py',
        )

    new_input = 'red~score oo new NewMaker.py q'
    rename_input = 'red~score oo ren NewMaker.py RenamedMaker.py y q'

    paths = (
        old_path,
        new_path,
        )
    for path in paths:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(str(path))

    with ide.Test():
        abjad_ide._start(input_=new_input)
        assert old_path.is_file()
        abjad_ide._start(input_=rename_input)
        assert not old_path.exists()
        assert new_path.is_file()


def test_AbjadIDE_rename_07():
    r'''Renames stylesheet.
    '''

    old_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'stylesheets',
        'new-stylesheet.ily',
        )
    new_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'stylesheets',
        'renamed-stylesheet.ily',
        )

    new_input = 'red~score yy new new-stylesheet.ily q'
    rename_input = 'red~score yy ren new-stylesheet.ily'
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

    with ide.Test():
        abjad_ide._start(input_=new_input)
        assert old_path.is_file()
        abjad_ide._start(input_=rename_input)
        assert not old_path.exists()
        assert new_path.is_file()
