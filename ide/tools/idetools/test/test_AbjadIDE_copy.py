import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_copy_01():
    r'''Into build directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').builds / 'letter'
        source /= 'front-cover.tex'
        target = ide.PackagePath('blue_score').builds / 'letter'
        target /= 'front-cover.tex'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score bb letter cp'
        input_ += f' red_score {source.trim()} q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_02():
    r'''Into distribution directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').distribution / 'red-score.pdf'
        target = ide.PackagePath('blue_score').distribution / 'red-score.pdf'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score dd cp'
        input_ += f' red_score {source.trim()} q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_03():
    r'''Into etc directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').etc / 'notes.txt'
        target = ide.PackagePath('blue_score').etc / 'notes.txt'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score ee cp'
        input_ += f' red_score {source.trim()} q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_04():
    r'''Into tools directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').tools / 'ScoreTemplate.py'
        target = ide.PackagePath('blue_score').tools / 'ScoreTemplate.py'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score oo cp'
        input_ += f' red_score {source.trim()} q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_05():
    r'''Into material directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score')
        source = source.materials / 'magic_numbers' / 'definition.py'
        target = ide.PackagePath('blue_score')
        target = target.materials / 'staccati' / 'definition.py'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score mm staccati cp'
        input_ += f' red_score {source.trim()} q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_06():
    r'''Into materials directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').materials / 'magic_numbers'
        target = ide.PackagePath('blue_score').materials / 'magic_numbers'
        assert source.is_dir()
        target.remove()

        input_ = 'Blue~Score mm cp'
        input_ += f' red_score {source.trim()} q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_07():
    r'''Into segment directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score')
        source = source.segments / 'segment_01' / 'definition.py'
        target = ide.PackagePath('blue_score')
        target = target.segments / 'segment_01' / 'definition.py'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score gg segment~01 cp'
        input_ += f' red_score {source.trim()} q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._transcript
        assert f'Writing {target.trim()} ...' in transcript



def test_AbjadIDE_copy_08():
    r'''Into segments directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').segments / 'segment_03'
        target = ide.PackagePath('blue_score').segments / 'segment_03'
        assert source.is_dir()
        target.remove()

        input_ = 'Blue~Score gg cp'
        input_ += f' red_score {source.trim()} q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_09():
    r'''Preexisting segment directory doesn't break IDE.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').segments / 'segment_03'
        assert source.is_dir()

        input_ = 'Red~Score gg cp'
        input_ += f' {source.trim()} q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert f'Existing {source.trim()} ...' in transcript
        assert 'Enter new name]> ' in transcript


def test_AbjadIDE_copy_10():
    r'''Into stylesheets directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').stylesheets / 'stylesheet.ily'
        target = ide.PackagePath('blue_score').stylesheets / 'stylesheet.ily'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score yy cp'
        input_ += f' red_score {source.trim()} q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_copy_11():
    r'''Into test directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').test / 'test_dummy.py'
        target = ide.PackagePath('blue_score').test / 'test_dummy.py'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score tt cp'
        input_ += f' red_score {source.trim()} q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._transcript
        assert f'Writing {target.trim()} ...' in transcript
