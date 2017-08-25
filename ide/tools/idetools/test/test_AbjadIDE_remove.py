import abjad
import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_remove_01():
    r'''Removes one score directory.
    '''

    wrapper_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'example_score_100',
        )
    contents_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'example_score_100',
        'example_score_100',
        )

    with ide.Test():
        input_ = 'new example~score~100 q'
        abjad_ide._start(input_=input_)
        assert wrapper_directory.is_dir()
        title = 'Example Score 100'
        abjad_ide._add_metadatum(
            contents_directory,
            'title',
            title,
            )
        input_ = 'rm Example~Score~100 remove q'
        abjad_ide._start(input_=input_)
        assert not wrapper_directory.exists()


def test_AbjadIDE_remove_02():
    r'''Removes range of score directorys.
    '''

    path_100_wrapper_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'example_score_100',
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
        'example_score_101',
        )
    path_101_contents_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'example_score_101',
        'example_score_101',
        )
    paths = [path_100_wrapper_directory, path_100_contents_directory, path_101_wrapper_directory, path_101_contents_directory]

    with ide.Test():
        input_ = 'new example~score~100 q'
        abjad_ide._start(input_=input_)
        assert path_100_wrapper_directory.is_dir()
        input_ = 'new example~score~101 q'
        abjad_ide._start(input_=input_)
        assert path_101_wrapper_directory.is_dir()
        title = 'Example Score 100'
        abjad_ide._add_metadatum(
            path_100_contents_directory,
            'title',
            title,
            )
        title = 'Example Score 101'
        abjad_ide._add_metadatum(
            path_101_contents_directory,
            'title',
            title,
            )
        input_ = 'rm Example~Score~100,Example~Score~101 remove~2 q'
        abjad_ide._start(input_=input_)
        assert not path_100_wrapper_directory.exists()
        assert not path_101_wrapper_directory.exists()
