import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_remove_01():
    r'''In build directory. Removes multiple files.
    '''

    with ide.Test():
        target_1 = ide.Path('red_score').build('letter', 'back-cover.tex')
        assert target_1.is_file()
        target_2 = target_1.with_name('front-cover.tex')
        assert target_2.is_file()
        target_3 = target_1.with_name('music.ly')
        assert target_3.is_file()

        abjad_ide('red %letter rm 1-3 remove~3 q')
        transcript = abjad_ide.io.transcript
        assert not target_1.exists()
        assert not target_2.exists()
        assert not target_3.exists()
        assert 'Select files to remove> 1-3' in transcript
        assert 'Will remove ...' in transcript
        assert f'    {target_1.trim()}' in transcript
        assert f'    {target_2.trim()}' in transcript
        assert f'    {target_3.trim()}' in transcript
        assert "Type 'remove 3' to proceed> remove 3" in transcript
        assert f'Removing {target_1.trim()} ...' in transcript
        assert f'Removing {target_2.trim()} ...' in transcript
        assert f'Removing {target_3.trim()} ...' in transcript

    with ide.Test():
        assert target_1.is_file()
        assert target_2.is_file()
        assert target_3.is_file()

        abjad_ide('red %letter rm 2-1,3 remove~3 q')
        transcript = abjad_ide.io.transcript
        assert not target_1.exists()
        assert not target_2.exists()
        assert not target_3.exists()
        assert 'Select files to remove> 2-1,3' in transcript
        assert 'Will remove ...' in transcript
        assert f'    {target_2.trim()}' in transcript
        assert f'    {target_1.trim()}' in transcript
        assert f'    {target_3.trim()}' in transcript
        assert "Type 'remove 3' to proceed> remove 3" in transcript
        assert f'Removing {target_2.trim()} ...' in transcript
        assert f'Removing {target_1.trim()} ...' in transcript
        assert f'Removing {target_3.trim()} ...' in transcript

    with ide.Test():
        assert target_1.is_file()
        assert target_2.is_file()
        assert target_3.is_file()

        abjad_ide('red %letter rm 2,1,3 remove~3 q')
        transcript = abjad_ide.io.transcript
        assert not target_1.exists()
        assert not target_2.exists()
        assert not target_3.exists()
        assert 'Select files to remove> 2,1,3' in transcript
        assert 'Will remove ...' in transcript
        assert f'    {target_2.trim()}' in transcript
        assert f'    {target_1.trim()}' in transcript
        assert f'    {target_3.trim()}' in transcript
        assert "Type 'remove 3' to proceed> remove 3" in transcript
        assert f'Removing {target_2.trim()} ...' in transcript
        assert f'Removing {target_1.trim()} ...' in transcript
        assert f'Removing {target_3.trim()} ...' in transcript


def test_AbjadIDE_remove_02():
    r'''In library directory.
    '''

    if not abjad.abjad_configuration.composer_library_tools:
        return

    directory = ide.Path(abjad.abjad_configuration.composer_library_tools)
    with abjad.FilesystemState(keep=[directory]):

        abjad_ide('lib new FooCommand.py y q')
        path = directory / 'FooCommand.py'
        assert path.is_file()

        abjad_ide('lib rm FooCommand.py remove q')
        transcript = abjad_ide.io.transcript
        assert not path.exists()
        assert 'Select assets to remove> FooCommand.py'
        assert f'Will remove {path.trim()} ...' in transcript
        assert "Type 'remove' to proceed> remove" in transcript
        assert f'Removing {path.trim()} ...' in transcript

        abjad_ide('lib rm FooCommand.py q')
        transcript = abjad_ide.io.transcript
        assert "Matches no path 'FooCommand.py' ..." in transcript


def test_AbjadIDE_remove_03():
    r'''In scores directory. Removes one package.
    '''

    with ide.Test():

        abjad_ide('new Test~Score~100 q')
        wrapper = ide.Path('test_scores') / 'test_score_100'
        assert wrapper.is_dir()

        abjad_ide('rm Test~Score~100 remove q')
        transcript = abjad_ide.io.transcript
        assert 'Select packages to remove> Test Score 100' in transcript
        assert f'Will remove {wrapper.trim()} ...'
        assert "Type 'remove' to proceed> remove" in transcript
        assert f'Removing {wrapper.trim()} ...' in transcript
        assert not wrapper.exists()


def test_AbjadIDE_remove_04():
    r'''In scores directory. Removes multiple packages.
    '''

    with ide.Test():

        abjad_ide('new test~score~100 new test~score~101 q')
        example_100 = ide.Path('test_scores') / 'test_score_100'
        example_101 = ide.Path('test_scores') / 'test_score_101'
        assert example_100.is_dir()
        assert example_101.is_dir()
        example_100.contents().add_metadatum('title', 'Test Score 100')
        example_101.contents().add_metadatum('title', 'Test Score 101')

        abjad_ide('rm Test~Score~100,Test~Score~101 remove~2 q')
        for line in [
            'Select packages to remove> Test Score 100,Test Score 101',
            'Will remove ...',
            f'    {example_100.trim()}',
            f'    {example_101.trim()}',
            "Type 'remove 2' to proceed> remove 2",
            f'Removing {example_100.trim()} ...',
            f'Removing {example_101.trim()} ...',
            ]:
            assert line in abjad_ide.io.transcript
        assert not example_100.exists()
        assert not example_101.exists()


def test_AbjadIDE_remove_05():
    r'''In stylesheets directory. Works with smart match.
    '''

    with ide.Test():
        path = ide.Path('red_score').stylesheets('stylesheet.ily')

        abjad_ide('red~score yy rm sheet q')
        transcript = abjad_ide.io.transcript
        assert 'Select files to remove> sheet' in transcript
        assert f'Will remove {path.trim()} ...' in transcript

        abjad_ide('red~score yy rm eet.i q')
        transcript = abjad_ide.io.transcript
        assert 'Select files to remove> eet.i' in transcript
        assert f'Will remove {path.trim()} ...' in transcript

        abjad_ide('red~score yy rm sty q')
        transcript = abjad_ide.io.transcript
        assert 'Select files to remove> sty' in transcript
        assert f'Will remove {path.trim()} ...' in transcript
