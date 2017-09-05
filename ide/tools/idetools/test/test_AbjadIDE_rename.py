import ide
abjad_ide = ide.AbjadIDE(is_test=True)

# TODO: add transcript asserts to each test

def test_AbjadIDE_rename_01():
    r'''Renames score directory.
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
        for path in paths:
            path.remove()

        abjad_ide('new test~score~100 q')
        assert example_100_package.is_dir()
        assert example_100_contents.is_dir()
        title = 'Test Score 100'
        example_100_contents.add_metadatum('title', title)

        abjad_ide('ren Test~Score~100 test_score_101 y q')
        assert not example_100_package.exists()
        assert example_101_package.is_dir()
        assert example_101_contents.is_dir()


def test_AbjadIDE_rename_02():
    r'''Renames material directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').materials / 'test_material'
        target = ide.Path('red_score').materials / 'new_test_material'
        paths = (source, target)
        for path in paths:
            path.remove()

        abjad_ide('red mm new test_material q')
        transcript = abjad_ide.io_manager.transcript
        assert 'Enter package name> test_material' in transcript
        assert source.is_dir()

        abjad_ide('red mm ren test_material new~test~material y q')
        transcript = abjad_ide.io_manager.transcript
        assert 'Enter package to rename> test_material' in transcript
        assert f'Renaming {source.trim()} ...' in transcript
        assert 'New name> new test material' in transcript
        assert 'Renaming ...' in transcript
        assert f' FROM: {source.trim()}' in transcript
        assert f'   TO: {target.trim()}' in transcript
        assert 'Ok?' in transcript
        assert not source.exists()
        assert target.is_dir()


def test_AbjadIDE_rename_03():
    r'''Renames segment directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments / 'segment_04'
        target = source.with_name('renamed_segment_04')
        for path in [source, target]:
            path.remove()

        abjad_ide('red gg new segment_04 q')
        assert source.is_dir()

        abjad_ide('red gg ren segment_04 renamed_segment_04 y q')
        assert not source.exists()
        assert target.is_dir()


def test_AbjadIDE_rename_04():
    r'''Renames segment directory with name metadatum.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments / 'segment_03'
        target = source.with_name('renamed_segment_03')
        assert source.is_dir()
        assert not target.exists()

        abjad_ide('red gg ren C renamed_segment_03 y q')
        assert not source.exists()
        assert target.is_dir()


def test_AbjadIDE_rename_05():
    r'''Renames build directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').builds / 'letter'
        target = source.with_name('standard-size')
        assert source.is_dir()
        target.remove()

        abjad_ide('red bb ren letter standard-size y q')
        assert not source.exists()
        assert target.is_dir()


def test_AbjadIDE_rename_06():
    r'''Renames tools file.
    '''

    with ide.Test():
        source = ide.Path('red_score').tools / 'NewMaker.py'
        target = source.with_name('RenamedMaker.py')
        for path in [source, target]:
            path.remove()

        abjad_ide('red oo new NewMaker.py q')
        assert source.is_file()

        abjad_ide('red oo ren NewMaker.py RenamedMaker.py y q')
        assert not source.exists()
        assert target.is_file()


def test_AbjadIDE_rename_07():
    r'''Renames stylesheet.
    '''

    with ide.Test():
        source = ide.Path('red_score').stylesheets
        source /= 'new-stylesheet.ily'
        target = source.with_name('renamed-stylesheet.ily')
        for path in [source, target]:
            path.remove()

        abjad_ide('red yy new new-stylesheet.ily q')
        assert source.is_file()

        abjad_ide('red yy ren new-stylesheet.ily renamed-stylesheet.ily y q')
        assert not source.exists()
        assert target.is_file()
