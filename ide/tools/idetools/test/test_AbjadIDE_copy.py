import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_copy_01():
    r'''Into build directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').builds / 'letter'
        source /= 'front-cover.tex'
        target = ide.Path('blue_score').builds / 'letter'
        target /= 'front-cover.tex'
        assert source.is_file()
        target.remove()

        abjad_ide(f'Blue bb letter cp red_score {source.trim()} q')
        assert target.exists()
        transcript = abjad_ide.io_manager.transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_02():
    r'''Into distribution directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').distribution / 'red-score.pdf'
        target = ide.Path('blue_score').distribution / 'red-score.pdf'
        assert source.is_file()
        target.remove()

        abjad_ide(f'Blue dd cp red_score {source.trim()} q')
        assert target.exists()
        transcript = abjad_ide.io_manager.transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_03():
    r'''Into etc directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').etc / 'notes.txt'
        target = ide.Path('blue_score').etc / 'notes.txt'
        assert source.is_file()
        target.remove()

        abjad_ide(f'Blue ee cp red_score {source.trim()} q')
        assert target.exists()
        transcript = abjad_ide.io_manager.transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_04():
    r'''Into tools directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').tools / 'ScoreTemplate.py'
        target = ide.Path('blue_score').tools / 'ScoreTemplate.py'
        assert source.is_file()
        target.remove()

        abjad_ide(f'Blue oo cp red_score {source.trim()} q')
        assert target.exists()
        transcript = abjad_ide.io_manager.transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_05():
    r'''Into material directory.
    '''

    with ide.Test():
        source = ide.Path('red_score')
        source = source.materials / 'magic_numbers' / 'definition.py'
        target = ide.Path('blue_score')
        target = target.materials / 'staccati' / 'definition.py'
        assert source.is_file()
        target.remove()

        abjad_ide(f'Blue mm staccati cp red_score {source.trim()} q')
        assert target.exists()
        transcript = abjad_ide.io_manager.transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_06():
    r'''Into materials directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').materials / 'magic_numbers'
        target = ide.Path('blue_score').materials / 'magic_numbers'
        assert source.is_dir()
        target.remove()

        abjad_ide(f'Blue mm cp red_score {source.trim()} q')
        assert target.exists()
        transcript = abjad_ide.io_manager.transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_07():
    r'''Into segment directory.
    '''

    with ide.Test():
        source = ide.Path('red_score')
        source = source.segments / 'segment_01' / 'definition.py'
        target = ide.Path('blue_score')
        target = target.segments / 'segment_01' / 'definition.py'
        assert source.is_file()
        target.remove()

        abjad_ide(f'Blue gg segment_01 cp red_score {source.trim()} q')
        assert target.exists()
        transcript = abjad_ide.io_manager.transcript
        assert f'Writing {target.trim()} ...' in transcript



def test_AbjadIDE_copy_08():
    r'''Into segments directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments / 'segment_03'
        target = ide.Path('blue_score').segments / 'segment_03'
        assert source.is_dir()
        target.remove()

        abjad_ide(f'Blue gg cp red_score {source.trim()} q')
        assert target.exists()
        transcript = abjad_ide.io_manager.transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_09():
    r'''Preexisting segment directory doesn't break IDE.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments / 'segment_03'
        assert source.is_dir()

        abjad_ide(f'Red gg cp {source.trim()} q')
        transcript = abjad_ide.io_manager.transcript
        assert f'Existing {source.trim()} ...' in transcript
        assert 'Enter new name> ' in transcript


def test_AbjadIDE_copy_10():
    r'''Into stylesheets directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').stylesheets / 'stylesheet.ily'
        target = ide.Path('blue_score').stylesheets / 'stylesheet.ily'
        assert source.is_file()
        target.remove()

        abjad_ide(f'Blue yy cp red_score {source.trim()} q')
        assert target.exists()
        transcript = abjad_ide.io_manager.transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_11():
    r'''Into test directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').test / 'test_dummy.py'
        target = ide.Path('blue_score').test / 'test_dummy.py'
        assert source.is_file()
        target.remove()

        abjad_ide(f'Blue tt cp red_score {source.trim()} q')
        assert target.exists()
        transcript = abjad_ide.io_manager.transcript
        assert f'Writing {target.trim()} ...' in transcript
