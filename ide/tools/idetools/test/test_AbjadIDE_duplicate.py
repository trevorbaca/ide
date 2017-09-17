import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_duplicate_01():
    r'''In build directory. Directory is empty.
    '''

    abjad_ide(f'blu %letter dup q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('blue_score').build('letter')
    assert f'Missing {path.trim()} files ...' in transcript


def test_AbjadIDE_duplicate_02():
    r'''In distribution directory. Directory is empty.
    '''

    abjad_ide(f'blu dd dup q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('blue_score').distribution
    assert f'Missing {path.trim()} files ...' in transcript


def test_AbjadIDE_duplicate_03():
    r'''In etc directory. Directory is empty.
    '''

    abjad_ide(f'blu ee dup q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('blue_score').etc
    assert f'Missing {path.trim()} files ...' in transcript


def test_AbjadIDE_duplicate_04():
    r'''In external directory.
    '''

    if not abjad_ide._test_external_directory():
        return

    directory = ide.Path('/Users/trevorbaca/baca/baca/tools')
    with abjad.FilesystemState(keep=[directory]):
        source = directory / 'Matrix.py'
        assert source.is_file()
        target = source.with_name('NewMatrix.py')
        target.remove()

        abjad_ide(f'lib dup Matrix.py NewMatrix.py y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert f'Select assets to duplicate> Matrix.py' in transcript
        assert f'Duplicating {source.trim()} ...' in transcript
        assert 'Enter new name> NewMatrix.py' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_duplicate_05():
    r'''In materials directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').material('magic_numbers')
        assert source.is_dir()
        target = source.with_name('magic_values')
        target.remove()

        abjad_ide(f'red mm dup agic magic~values y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert f'Select packages to duplicate> agic' in transcript
        assert f'Duplicating {source.trim()} ...'
        assert 'Enter new name> magic values'
        assert f'Writing {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert "Replacing 'magic_numbers' with 'magic_values' ..." in \
            transcript


def test_AbjadIDE_duplicate_06():
    r'''In scores directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').wrapper 
        assert source.is_dir()
        target = source.with_name('green_score')
        target.remove()

        abjad_ide('dup Red~Score Green~Score y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert 'Select packages to duplicate> Red Score' in transcript
        assert f'Duplicating {source.trim()} ...' in transcript
        assert 'Enter title> Green Score' in transcript 
        assert 'Ok?> y' in transcript
        assert "Replacing 'red_score' with 'green_score' ..." in transcript
        assert "Replacing 'Red Score' with 'Green Score' ..." in transcript


def test_AbjadIDE_duplicate_07():
    r'''In segments directory.
    '''

    with ide.Test():
        source = ide.Path('blue_score').segment('segment_02')
        assert source.is_dir()
        target = source.with_name('segment_03')
        target.remove()

        abjad_ide(f'blu gg dup segment~02 segment~03 y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert f'Select packages to duplicate> segment 02' in transcript
        assert f'Duplicating {source.trim()} ...'
        assert 'Enter new name> segment 03'
        assert f'Writing {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert "Replacing 'segment_02' with 'segment_03' ..." in \
            transcript


def test_AbjadIDE_duplicate_08():
    r'''In stylesheets directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').stylesheets / 'stylesheet.ily'
        assert source.is_file()
        target = source.with_name('new-stylesheet.ily')
        target.remove()

        abjad_ide(f'red yy dup eet.i new~stylesheet y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert f'Select files to duplicate> eet.i' in transcript
        assert f'Duplicating {source.trim()} ...' in transcript
        assert 'Enter new name> new stylesheet' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_duplicate_09():
    r'''In test directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').test / 'test_materials.py'
        assert source.is_file()
        target = source.with_name('test_new_materials.py')
        target.remove()

        abjad_ide(f'red tt dup _mat test~new~materials y q')
        transcript = abjad_ide.io.transcript
        assert target.exists()
        assert f'Select files to duplicate> _mat' in transcript
        assert f'Duplicating {source.trim()} ...' in transcript
        assert 'Enter new name> test new materials' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_duplicate_10():
    r'''In tools directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').tools / 'ScoreTemplate.py'
        assert source.is_file()
        target = source.with_name('ColorSpecifier.py')
        target.remove()

        abjad_ide(f'red oo dup ST Color~specifier y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert f'Select files to duplicate> ST' in transcript
        assert f'Duplicating {source.trim()} ...' in transcript
        assert 'Enter new name> Color specifier' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
