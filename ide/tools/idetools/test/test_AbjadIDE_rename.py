import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_rename_01():
    r'''Renames score directory.
    '''

    with ide.Test():
        example_100_package = ide.PackagePath('test_scores') / 'test_score_100'
        example_100_contents = example_100_package / example_100_package.name
        example_101_package = ide.PackagePath('test_scores') / 'test_score_101'
        example_101_contents = example_101_package / example_101_package.name
        paths = (
            example_100_package,
            example_100_contents,
            example_101_package,
            example_101_contents,
            )
        for path in paths:
            path.remove()

        input_ = 'new test~score~100 q'
        abjad_ide._start(input_=input_)
        assert example_100_package.is_dir()
        assert example_100_contents.is_dir()
        title = 'Test Score 100'
        example_100_contents.add_metadatum('title', title)

        input_ = 'ren Test~Score~100 test_score_101 y q'
        abjad_ide._start(input_=input_)
        assert not example_100_package.exists()
        assert example_101_package.is_dir()
        assert example_101_contents.is_dir()


def test_AbjadIDE_rename_02():
    r'''Renames material directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').materials / 'test_material'
        target = ide.PackagePath('red_score').materials / 'new_test_material'
        paths = (source, target)
        for path in paths:
            path.remove()

        input_ = 'red~score mm new test~material q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Enter package name]> test material' in transcript
        assert source.is_dir()

        input_ = 'red~score mm ren test~material new~test~material y q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Enter package to rename]> test material' in transcript
        assert f'Renaming {source.trim()} ...' in transcript
        assert 'New name or return to cancel]> new test material' in transcript
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
        source = ide.PackagePath('red_score').segments / 'segment_04'
        target = source.with_name('renamed_segment_04')
        for path in [source, target]:
            path.remove()

        input_ = 'red~score gg new segment~04 q'
        abjad_ide._start(input_=input_)
        assert source.is_dir()

        input_ = 'red~score gg ren segment~04 renamed_segment_04 y q'
        abjad_ide._start(input_=input_)
        assert not source.exists()
        assert target.is_dir()


def test_AbjadIDE_rename_04():
    r'''Renames segment directory with name metadatum.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').segments / 'segment_03'
        target = source.with_name('renamed_segment_03')
        assert source.is_dir()
        assert not target.exists()

        input_ = 'red~score gg ren C renamed_segment_03 y q'
        abjad_ide._start(input_=input_)
        assert not source.exists()
        assert target.is_dir()


def test_AbjadIDE_rename_05():
    r'''Renames build directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').builds / 'letter'
        target = source.with_name('standard-size')
        assert source.is_dir()
        target.remove()

        input_ = 'red~score bb ren letter standard-size y q'
        abjad_ide._start(input_=input_)
        assert not source.exists()
        assert target.is_dir()


def test_AbjadIDE_rename_06():
    r'''Renames tools file.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').tools / 'NewMaker.py'
        target = source.with_name('RenamedMaker.py')
        for path in [source, target]:
            path.remove()

        input_ = 'red~score oo new NewMaker.py q'
        abjad_ide._start(input_=input_)
        assert source.is_file()

        input_ = 'red~score oo ren NewMaker.py RenamedMaker.py y q'
        abjad_ide._start(input_=input_)
        assert not source.exists()
        assert target.is_file()


def test_AbjadIDE_rename_07():
    r'''Renames stylesheet.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').stylesheets
        source /= 'new-stylesheet.ily'
        target = source.with_name('renamed-stylesheet.ily')
        for path in [source, target]:
            path.remove()

        input_ = 'red~score yy new new-stylesheet.ily q'
        abjad_ide._start(input_=input_)
        assert source.is_file()

        input_ = 'red~score yy ren new-stylesheet.ily'
        input_ += ' renamed-stylesheet.ily y q'
        abjad_ide._start(input_=input_)
        assert not source.exists()
        assert target.is_file()
