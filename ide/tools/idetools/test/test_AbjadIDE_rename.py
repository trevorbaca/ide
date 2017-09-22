import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_rename_01():
    r'''Renames score package.
    '''

    with ide.Test():
        test_score_100 = ide.Path('test_scores') / 'test_score_100'
        test_score_100.remove()
        test_score_101 = ide.Path('test_scores') / 'test_score_101'
        test_score_101.remove()

        abjad_ide('new Test~Score~100 q')
        assert test_score_100.is_dir()

        abjad_ide('ren Test~Score~100 test_score_101 y q')
        assert not test_score_100.exists()
        assert test_score_101.is_dir()


def test_AbjadIDE_rename_02():
    r'''Renames material directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').materials('test_material')
        source.remove()
        target = ide.Path('red_score').materials('new_test_material')
        target.remove()

        abjad_ide('red mm new test_material q')
        transcript = abjad_ide.io.transcript
        assert source.is_dir()

        abjad_ide('red mm ren test_material new~test~material y q')
        transcript = abjad_ide.io.transcript
        assert not source.exists()
        assert target.is_dir()
        assert 'Select package to rename> test_material' in transcript
        assert f'Renaming {source.trim()} ...' in transcript
        assert 'New name> new test material' in transcript
        assert 'Renaming ...' in transcript
        assert f' FROM: {source.trim()}' in transcript
        assert f'   TO: {target.trim()}' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_rename_03():
    r'''Renames segment directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments('D')
        source.remove()
        target = source.with_name('E')
        target.remove()

        abjad_ide('red gg new D q')
        assert source.is_dir()

        abjad_ide('red gg ren D E y q')
        transcript = abjad_ide.io.transcript
        assert not source.exists()
        assert target.is_dir()
        assert 'Select package to rename> D' in transcript
        assert f'Renaming {source.trim()} ...' in transcript
        assert 'New name> E' in transcript
        assert 'Renaming ...' in transcript
        assert f' FROM: {source.trim()}' in transcript
        assert f'   TO: {target.trim()}' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_rename_04():
    r'''Renames named segment.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments('C')
        assert source.is_dir()
        target = source.with_name('D')
        target.remove()

        abjad_ide('red gg ren C D y q')
        transcript = abjad_ide.io.transcript
        assert not source.exists()
        assert target.is_dir()
        assert 'Select package to rename> C' in transcript
        assert f'Renaming {source.trim()} ...' in transcript
        assert 'New name> D' in transcript
        assert 'Renaming ...' in transcript
        assert f' FROM: {source.trim()}' in transcript
        assert f'   TO: {target.trim()}' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_rename_05():
    r'''Renames build directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').builds('letter')
        assert source.is_dir()
        target = source.with_name('standard-size')
        target.remove()

        abjad_ide('red bb ren letter standard~size y q')
        transcript = abjad_ide.io.transcript
        assert not source.exists()
        assert target.is_dir()
        assert 'Select directory to rename> letter' in transcript
        assert f'Renaming {source.trim()} ...' in transcript
        assert 'New name> standard size' in transcript
        assert 'Renaming ...' in transcript
        assert f' FROM: {source.trim()}' in transcript
        assert f'   TO: {target.trim()}' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_rename_06():
    r'''Renames tools file.
    '''

    with ide.Test():
        source = ide.Path('red_score').tools('NewMaker.py')
        source.remove()
        target = source.with_name('RenamedMaker.py')
        target.remove()

        abjad_ide('red oo new NewMaker.py y q')
        assert source.is_file()

        abjad_ide('red oo ren NM RenamedMaker.py y q')
        transcript = abjad_ide.io.transcript
        assert not source.exists()
        assert target.is_file()
        assert 'Select file to rename> NM' in transcript
        assert f'Renaming {source.trim()} ...' in transcript
        assert 'New name> RenamedMaker.py' in transcript
        assert 'Renaming ...' in transcript
        assert f' FROM: {source.trim()}' in transcript
        assert f'   TO: {target.trim()}' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_rename_07():
    r'''Renames stylesheet.
    '''

    with ide.Test():
        source = ide.Path('red_score').stylesheets('new-stylesheet.ily')
        source.remove()
        target = source.with_name('renamed-stylesheet.ily')
        target.remove()

        abjad_ide('red yy new new-stylesheet.ily y q')
        assert source.is_file()

        abjad_ide('red yy ren new- renamed-stylesheet y q')
        assert not source.exists()
        assert target.is_file()
        transcript = abjad_ide.io.transcript
        assert not source.exists()
        assert target.is_file()
        assert 'Select file to rename> new-' in transcript
        assert f'Renaming {source.trim()} ...' in transcript
        assert 'New name> renamed-stylesheet' in transcript
        assert 'Renaming ...' in transcript
        assert f' FROM: {source.trim()}' in transcript
        assert f'   TO: {target.trim()}' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_rename_08():
    r'''In library.
    '''

    if not abjad.abjad_configuration.composer_library_tools:
        return

    directory = ide.Path(abjad.abjad_configuration.composer_library_tools)
    with abjad.FilesystemState(keep=[directory]):
        source = directory / 'FooCommand.py'
        source.remove()
        target = source.with_name('NewFooCommand.py')
        target.remove()

        abjad_ide('ll new FooCommand.py y q')
        assert source.is_file()

        abjad_ide('ll ren FooCommand.py NewFooCommand.py y q')
        transcript = abjad_ide.io.transcript
        assert not source.exists()
        assert target.is_file()
        assert 'Select assets to rename> FooCommand.py'
        assert f'Renaming {source.trim()} ...' in transcript
        assert 'New name> NewFooCommand.py' in transcript
        assert 'Renaming ...' in transcript
        assert f' FROM: {source.trim()}' in transcript
        assert f'   TO: {target.trim()}' in transcript
        assert 'Ok?> y' in transcript
