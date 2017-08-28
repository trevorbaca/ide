import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_remove_01():
    r'''Removes one score directory.
    '''

    with ide.Test():
        package = ide.Path('example_scores') / 'example_score_100'
        contents = package / package.name

        input_ = 'new example~score~100 q'
        abjad_ide._start(input_=input_)
        assert package.is_dir()
        title = 'Example Score 100'
        contents._add_metadatum('title', title)

        input_ = 'rm Example~Score~100 remove q'
        abjad_ide._start(input_=input_)
        assert not package.exists()


def test_AbjadIDE_remove_02():
    r'''Removes range of score directories.
    '''

    with ide.Test():
        example_100_package = ide.Path('example_scores') / 'example_score_100'
        example_100_contents = example_100_package / example_100_package.name
        example_101_package = ide.Path('example_scores') / 'example_score_101'
        example_101_contents = example_101_package / example_101_package.name
        paths = (
            example_100_package,
            example_100_contents,
            example_101_package,
            example_101_contents,
            )

        input_ = 'new example~score~100 q'
        abjad_ide._start(input_=input_)
        assert example_100_package.is_dir()

        input_ = 'new example~score~101 q'
        abjad_ide._start(input_=input_)
        assert example_101_package.is_dir()
        title = 'Example Score 100'
        example_100_contents._add_metadatum('title', title)
        title = 'Example Score 101'
        example_101_contents._add_metadatum('title', title)

        input_ = 'rm Example~Score~100,Example~Score~101 remove~2 q'
        abjad_ide._start(input_=input_)
        assert not example_100_package.exists()
        assert not example_101_package.exists()
