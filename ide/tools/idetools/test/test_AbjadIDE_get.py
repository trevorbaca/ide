import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_get_01():
    r'''Into build directory. Directory is empty.
    '''

    with ide.Test():
        source = ide.Path('red_score').builds / 'letter' / 'front-cover.tex'
        assert source.is_file()
        target = ide.Path('blue_score').builds / 'letter' / 'front-cover.tex'
        target.remove()

        abjad_ide(f'Blue %letter get {source.trim()} y q')
        assert target.is_file()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : builds : letter (empty)'
        header += ' - select files to get:'
        assert header in transcript
        assert f'> {source.trim()}' in transcript
        assert f'Copying {source.trim()} ...' in transcript
        assert 'Ok?> y' in transcript

    with ide.Test():
        source_1 = ide.Path('red_score').builds / 'letter' / 'back-cover.tex'
        assert source_1.is_file()
        source_2 = source_1.with_name('front-cover.tex')
        assert source_2.is_file()
        source_3 = source_1.with_name('music.ly')
        assert source_3.is_file()
        target_1 = ide.Path('blue_score').builds / 'letter' / 'back-cover.tex'
        target_1.remove()
        target_2 = target_1.with_name('front-cover.tex')
        target_2.remove()
        target_3 = target_1.with_name('music.ly')
        target_3.remove()

        abjad_ide(f'Blue %letter get 2-3,1 y q')
        assert target.is_file()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : builds : letter (empty)'
        header += ' - select files to get:'
        assert header in transcript
        assert '> 2-3,1' in transcript
        assert 'Copying ...' in transcript
        assert f'    {source_2.trim()}' in transcript
        assert f'    {source_3.trim()}' in transcript
        assert f'    {source_1.trim()}' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_get_02():
    r'''Into distribution directory. Directory is empty.
    '''

    with ide.Test():
        source = ide.Path('red_score').distribution / 'red-score.pdf'
        assert source.is_file()
        target = ide.Path('blue_score').distribution / 'red-score.pdf'
        target.remove()

        abjad_ide(f'Blue dd get {source.trim()} y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : distribution (empty)'
        header += ' - select files to get:'
        assert header in transcript
        assert f'> {source.trim()}' in transcript
        assert f'Copying {source.trim()} ...' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_get_03():
    r'''Into etc directory. Directory is empty.
    '''

    with ide.Test():
        source = ide.Path('red_score').etc / 'notes.txt'
        assert source.is_file()
        target = ide.Path('blue_score').etc / 'notes.txt'
        target.remove()

        abjad_ide(f'Blue ee get {source.trim()} y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : etc (empty) - select files to get:'
        assert header in transcript
        assert f'> {source.trim()}' in transcript
        assert f'Copying {source.trim()} ...' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_get_04():
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

        abjad_ide(f'lib get Matrix.py NewMatrix.py y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert f'Select assets to get> Matrix.py' in transcript
        assert f'Copying {source.trim()} ...' in transcript
        assert f'Existing {source.trim()} ...' in transcript
        assert 'Enter new name> NewMatrix.py' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_get_05():
    r'''Into material directory.
    '''

    with ide.Test():
        source = ide.Path('red_score')
        source = source.materials / 'magic_numbers' / 'definition.py'
        assert source.is_file()
        target = ide.Path('blue_score')
        target = target.materials / 'staccati' / 'definition.py'
        target.remove()

        abjad_ide(f'Blue mm staccati get {source.trim()} y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : materials : staccati (empty)'
        header += ' - select files to get:'
        assert header in transcript
        assert f'> {source.trim()}' in transcript
        assert f'Copying {source.trim()} ...' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_get_06():
    r'''Into materials directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').materials / 'magic_numbers'
        assert source.is_dir()
        target = ide.Path('blue_score').materials / 'magic_numbers'
        target.remove()

        abjad_ide(f'Blue mm get red_score {source.trim()} y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : materials - select packages to get:'
        assert header in transcript
        assert f'> {source.trim()}' in transcript
        assert f'Copying {source.trim()} ...' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_get_07():
    r'''Into scores directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').wrapper 
        assert source.is_dir()
        target = source.with_name('green_score')
        target.remove()

        abjad_ide('get Red~Score Green~Score y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        assert 'Select packages to get> Red Score' in transcript
        assert f'Copying {source.trim()} ...' in transcript
        assert f'Existing {source.trim()} ...' in transcript
        assert 'Enter title> Green Score' in transcript 
        assert 'Ok?> y' in transcript
        assert "Replacing 'red_score' with 'green_score' ..." in transcript
        assert "Replacing 'Red Score' with 'Green Score' ..." in transcript


def test_AbjadIDE_get_08():
    r'''Into segment directory.
    '''

    with ide.Test():
        source = ide.Path('red_score')
        source = source.segments / 'segment_01' / 'definition.py'
        assert source.is_file()
        target = ide.Path('blue_score')
        target = target.segments / 'segment_01' / 'definition.py'
        target.remove()

        abjad_ide(f'Blue gg segment_01 get {source.trim()} y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : segments : segment_01 (empty)'
        header += ' - select files to get:'
        assert header in transcript
        assert f'> {source.trim()}' in transcript
        assert f'Copying {source.trim()} ...' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_get_09():
    r'''Into segments directory from other score.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments / 'segment_03'
        assert source.is_dir()
        target = ide.Path('blue_score').segments / 'segment_03'
        target.remove()

        abjad_ide(f'Blue gg get red_score {source.trim()} y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : segments - select packages to get:'
        assert header in transcript
        assert f'> {source.trim()}' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_get_10():
    r'''Into segments directory from same score.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments / 'segment_03'
        assert source.is_dir()
        target = source.with_name('segment_04')

        abjad_ide(f'Red gg get C segment~04 D y q')
        transcript = abjad_ide.io.transcript
        assert target.is_dir()
        assert 'Select packages to get> C'
        assert f'Copying {source.trim()} ...' in transcript
        assert f'Existing {source.trim()} ...' in transcript
        assert 'Enter new name> segment 04' in transcript
        assert 'Name metadatum> D' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_get_11():
    r'''Into stylesheets directory. Directory is empty.
    '''

    with ide.Test():
        source = ide.Path('red_score').stylesheets / 'stylesheet.ily'
        assert source.is_file()
        target = ide.Path('blue_score').stylesheets / 'stylesheet.ily'
        target.remove()

        abjad_ide(f'Blue yy get {source.trim()} y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : stylesheets (empty)'
        header += ' - select files to get:'
        assert header in transcript
        assert f'> {source.trim()}' in transcript
        assert f'Copying {source.trim()} ...' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_get_12():
    r'''Into test directory. Directory is empty.
    '''

    with ide.Test():
        source = ide.Path('red_score').test / 'test_materials.py'
        assert source.is_file()
        target = ide.Path('blue_score').test / 'test_materials.py'
        target.remove()

        abjad_ide(f'Blue tt get {source.trim()} y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : test (empty) - select files to get:'
        assert header in transcript
        assert f'> {source.trim()}' in transcript
        assert f'Copying {source.trim()} ...' in transcript
        assert 'Ok?> y' in transcript


def test_AbjadIDE_get_13():
    r'''Into tools directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').tools / 'ScoreTemplate.py'
        assert source.is_file()
        target = ide.Path('blue_score').tools / 'ScoreTemplate.py'
        target.remove()

        abjad_ide(f'Blue oo get red_score {source.trim()} y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : tools - select files to get:'
        assert header in transcript
        assert f'> {source.trim()}' in transcript
        assert f'Copying {source.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
