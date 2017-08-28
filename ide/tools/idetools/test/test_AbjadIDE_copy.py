import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_copy_01():
    r'''Into build subdirectory.
    '''

    with ide.Test():
        source = ide.Path('red_score').build / 'letter' / 'front-cover.tex'
        target = ide.Path('blue_score').build / 'letter' / 'front-cover.tex'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score bb letter cp more'
        input_ += f' {abjad_ide._trim(source)} y q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._io_manager._transcript.contents
        header = 'Blue Score (2017) - build directory'
        header += ' - letter - select:'
        assert header in transcript


def test_AbjadIDE_copy_02():
    r'''Into distribution directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').distribution / 'red-score.pdf'
        target = ide.Path('blue_score').distribution / 'red-score.pdf'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score dd cp more'
        input_ += f' {abjad_ide._trim(source)} y q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._io_manager._transcript.contents
        header = 'Blue Score (2017) - distribution directory - select:'
        assert header in transcript


def test_AbjadIDE_copy_03():
    r'''Into etc directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').etc / 'notes.txt'
        target = ide.Path('blue_score').etc / 'notes.txt'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score ee cp more'
        input_ += f' {abjad_ide._trim(source)} y q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Blue Score (2017) - etc directory - select:' in transcript


def test_AbjadIDE_copy_04():
    r'''Into tools directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').tools / 'ScoreTemplate.py'
        target = ide.Path('blue_score').tools / 'ScoreTemplate.py'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score oo cp more'
        input_ += f' {abjad_ide._trim(source)} y q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._io_manager._transcript.contents
        header = 'Blue Score (2017) - tools directory - select:'
        assert header in transcript


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

        input_ = 'Blue~Score mm staccati cp more'
        input_ += f' {abjad_ide._trim(source)} y q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._io_manager._transcript.contents
        header = 'Blue Score (2017) - materials directory - staccati - select:'
        assert header in transcript


def test_AbjadIDE_copy_06():
    r'''Into materials directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').materials / 'magic_numbers'
        target = ide.Path('blue_score').materials / 'magic_numbers'
        assert source.is_dir()
        target.remove()

        input_ = 'Blue~Score mm cp more'
        input_ += f' {abjad_ide._trim(source)} y q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._io_manager._transcript.contents
        header = 'Blue Score (2017) - materials directory - select:'
        assert header in transcript


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

        input_ = 'Blue~Score gg segment~01 cp more'
        input_ += f' {abjad_ide._trim(source)} y q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._io_manager._transcript.contents
        header = 'Blue Score (2017)'
        header += ' - segments directory - segment 01 - select:'
        assert header in transcript


def test_AbjadIDE_copy_08():
    r'''Into segments directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments / 'segment_03'
        target = ide.Path('blue_score').segments / 'segment_03'
        assert source.is_dir()
        target.remove()

        input_ = 'Blue~Score gg cp more'
        input_ += f' {abjad_ide._trim(source)} y q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._io_manager._transcript.contents
        header = 'Blue Score (2017) - segments directory - select:'
        assert header in transcript


def test_AbjadIDE_copy_09():
    r'''Preexisting segment directory doesn't break IDE.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments / 'segment_03'
        assert source.is_dir()

        input_ = 'Red~Score gg cp'
        input_ += f' {abjad_ide._trim(source)} q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert f'{abjad_ide._trim(source)} already exists.' in transcript
        assert 'Enter new name]> ' in transcript


def test_AbjadIDE_copy_10():
    r'''Into stylesheets directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').stylesheets / 'stylesheet.ily'
        target = ide.Path('blue_score').stylesheets / 'stylesheet.ily'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score yy cp more'
        input_ += f' {abjad_ide._trim(source)} y q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._io_manager._transcript.contents
        header = 'Blue Score (2017) - stylesheets directory - select:'
        assert header in transcript


def test_AbjadIDE_copy_11():
    r'''Into test directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').test / 'test_dummy.py'
        target = ide.Path('blue_score').test / 'test_dummy.py'
        assert source.is_file()
        target.remove()

        input_ = 'Blue~Score tt cp more'
        input_ += f' {abjad_ide._trim(source)} y q'
        abjad_ide._start(input_=input_)
        assert target.exists()
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Blue Score (2017) - test directory - select:' in transcript
