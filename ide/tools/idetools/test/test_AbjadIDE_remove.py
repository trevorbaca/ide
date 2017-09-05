import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_remove_01():
    r'''Removes one score directory.
    '''

    with ide.Test():
        package = ide.Path('test_scores') / 'test_score_100'
        contents = package / package.name

        abjad_ide('new test~score~100 q')
        assert package.is_dir()
        title = 'Test Score 100'
        contents.add_metadatum('title', title)

        abjad_ide('rm Test~Score~100 remove q')
        transcript = abjad_ide.io_manager.transcript
        assert 'Enter package(s) to remove> Test Score 100' in transcript
        assert f'Confirming {package} ...'
        assert "Type 'remove' to proceed> remove" in transcript
        assert f'emoving {package} ...' in transcript
        assert not package.exists()


def test_AbjadIDE_remove_02():
    r'''Removes range of score directories.
    '''

    with ide.Test():
        example_100_package = ide.Path('test_scores') / 'test_score_100'
        example_100_contents = example_100_package / example_100_package.name
        example_101_package = ide.Path('test_scores') / 'test_score_101'
        example_101_contents = example_101_package / example_101_package.name
        paths = (
            example_100_package,
            example_100_contents,
            example_101_package,
            example_101_contents,
            )

        abjad_ide('new test~score~100 new test~score~101 q')
        assert example_100_package.is_dir()
        assert example_101_package.is_dir()
        title = 'Test Score 100'
        example_100_contents.add_metadatum('title', title)
        title = 'Test Score 101'
        example_101_contents.add_metadatum('title', title)

        abjad_ide('rm Test~Score~100,Test~Score~101 remove~2 q')
        for line in [
            'Enter package(s) to remove> Test Score 100,Test Score 101',
            'Confirming ...',
            f'    {example_100_package}',
            f'    {example_101_package}',
            "Type 'remove 2' to proceed> remove 2",
            f'Removing {example_100_package} ...',
            f'Removing {example_101_package} ...',
            ]:
            assert line in abjad_ide.io_manager.transcript
        assert not example_100_package.exists()
        assert not example_101_package.exists()


def test_AbjadIDE_remove_03():
    r'''Works with smart match.
    '''

    with ide.Test():
        path = ide.Path('red_score').stylesheets / 'stylesheet.ily'

        abjad_ide('red~score yy rm sheet q')
        transcript = abjad_ide.io_manager.transcript
        assert 'Enter file(s) to remove> sheet' in transcript
        assert f'Confirming {path.trim()} ...' in transcript

        abjad_ide('red~score yy rm eet.i q')
        transcript = abjad_ide.io_manager.transcript
        assert 'Enter file(s) to remove> eet.i' in transcript
        assert f'Confirming {path.trim()} ...' in transcript

        abjad_ide('red~score yy rm sty q')
        transcript = abjad_ide.io_manager.transcript
        assert 'Enter file(s) to remove> sty' in transcript
        assert f'Confirming {path.trim()} ...' in transcript
