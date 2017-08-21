import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_remove_01():
    r'''Removes one score directory.
    '''

    outer_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'example_score_100',
        )
    inner_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'example_score_100',
        'example_score_100',
        )

    with abjad.FilesystemState(remove=[outer_path, inner_path]):
        input_ = 'new example~score~100 q'
        abjad_ide._start(input_=input_)
        assert outer_path.is_dir()
        title = 'Example Score 100'
        abjad_ide._add_metadatum(
            inner_path,
            'title',
            title,
            )
        input_ = 'rm Example~Score~100 remove q'
        abjad_ide._start(input_=input_)
        assert not outer_path.exists()


def test_AbjadIDE_remove_02():
    r'''Removes range of score directorys.
    '''

    path_100_outer = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'example_score_100',
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
        'example_score_101',
        )
    path_101_inner = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'example_score_101',
        'example_score_101',
        )
    paths = [path_100_outer, path_100_inner, path_101_outer, path_101_inner]

    with abjad.FilesystemState(remove=paths):
        input_ = 'new example~score~100 q'
        abjad_ide._start(input_=input_)
        assert path_100_outer.is_dir()
        input_ = 'new example~score~101 q'
        abjad_ide._start(input_=input_)
        assert path_101_outer.is_dir()
        title = 'Example Score 100'
        abjad_ide._add_metadatum(
            path_100_inner,
            'title',
            title,
            )
        title = 'Example Score 101'
        abjad_ide._add_metadatum(
            path_101_inner,
            'title',
            title,
            )
        input_ = 'rm Example~Score~100,~Example~Score~101 remove~2 q'
        abjad_ide._start(input_=input_)
        assert not path_100_outer.exists()
        assert not path_101_outer.exists()
