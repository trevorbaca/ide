import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_copy_01():
    r'''Into build subdirectory.
    '''

    with ide.Test():
        source = ide.Path('red_score')
        source = source / 'build' / 'letter' / 'front-cover.tex'
        target = ide.Path('blue_score')
        target = target / 'build' / 'letter' / 'front-cover.tex'
        assert source.is_file()
        assert not target.exists()
        input_ = 'Blue~Score bb letter cp more'
        input_ += ' {} y q'.format(abjad_ide._trim(source))
        abjad_ide._start(input_=input_)
        assert target.exists()
        contents = abjad_ide._io_manager._transcript.contents
        header = 'Blue Score (2017) - build directory'
        header += ' - letter - select:'
        assert header in contents


def test_AbjadIDE_copy_02():
    r'''Into distribution directory.
    '''

    with ide.Test():
        source = ide.Path('red_score')
        source = source / 'distribution' / 'red-score-score.pdf'
        target = ide.Path('blue_score')
        target = target / 'distribution' / 'red-score-score.pdf'
        assert not target.exists()
        input_ = 'Blue~Score dd cp more'
        input_ += ' {} y q'.format(abjad_ide._trim(source))
        abjad_ide._start(input_=input_)
        assert target.exists()
        contents = abjad_ide._io_manager._transcript.contents
        string = 'Blue Score (2017) - distribution directory - select:'
        assert string in contents


def test_AbjadIDE_copy_03():
    r'''Into etc directory.
    '''

    with ide.Test():
        source = ide.Path('red_score') / 'etc' / 'notes.txt'
        target = ide.Path('blue_score') / 'etc' / 'notes.txt'
        assert not target.exists()
        input_ = 'Blue~Score ee cp more'
        input_ += ' {} y q'.format(abjad_ide._trim(source))
        abjad_ide._start(input_=input_)
        assert target.exists()
        contents = abjad_ide._io_manager._transcript.contents
        string = 'Blue Score (2017) - etc directory - select:'
        assert string in contents


def test_AbjadIDE_copy_04():
    r'''Into tools directory.
    '''

    with ide.Test():
        source = ide.Path('red_score') / 'tools' / 'ScoreTemplate.py'
        target = ide.Path('blue_score') / 'tools' / 'ScoreTemplate.py'
        assert not target.exists()
        input_ = 'Blue~Score oo cp more'
        input_ += ' {} y q'.format(abjad_ide._trim(source))
        abjad_ide._start(input_=input_)
        assert target.exists()
        contents = abjad_ide._io_manager._transcript.contents
        string = 'Blue Score (2017) - tools directory - select:'
        assert string in contents


def test_AbjadIDE_copy_05():
    r'''Into material directory.
    '''

    with ide.Test():
        source = ide.Path('red_score')
        source = source / 'materials' / 'magic_numbers' / 'definition.py'
        target = ide.Path('blue_score')
        target = target / 'materials' / 'staccati' / 'definition.py'
        target.unlink()
        assert not target.exists()
        input_ = 'Blue~Score mm staccati cp more'
        input_ += ' {} y q'.format(abjad_ide._trim(source))
        abjad_ide._start(input_=input_)
        assert target.exists()
        contents = abjad_ide._io_manager._transcript.contents
        string = 'Blue Score (2017) - materials directory - staccati - select:'
        assert string in contents


def test_AbjadIDE_copy_06():
    r'''Into materials directory.
    '''

    with ide.Test():
        source = ide.Path('red_score') / 'materials' / 'magic_numbers'
        target = ide.Path('blue_score') / 'materials' / 'magic_numbers'
        assert source.is_dir()
        assert not target.exists()
        input_ = 'Blue~Score mm cp more'
        input_ += ' {} y q'.format(abjad_ide._trim(source))
        abjad_ide._start(input_=input_)
        assert target.exists()
        contents = abjad_ide._io_manager._transcript.contents
        string = 'Blue Score (2017) - materials directory - select:'
        assert string in contents


def test_AbjadIDE_copy_07():
    r'''Into segment directory.
    '''

    with ide.Test():
        source = ide.Path('red_score')
        source = source / 'segments' / 'segment_01' / 'definition.py'
        target = ide.Path('blue_score')
        target = target / 'segments' / 'segment_01' / 'definition.py'
        target.unlink()
        assert not target.exists()
        input_ = 'Blue~Score gg segment~01 cp more'
        input_ += ' {} y q'.format(abjad_ide._trim(source))
        abjad_ide._start(input_=input_)
        assert target.exists()
        contents = abjad_ide._io_manager._transcript.contents
        string = 'Blue Score (2017) - segments directory - segment 01 - select:'
        assert string in contents


def test_AbjadIDE_copy_08():
    r'''Into segments directory.
    '''

    with ide.Test():
        source = ide.Path('red_score') / 'segments' / 'segment_03'
        target = ide.Path('blue_score') / 'segments' / 'segment_03'
        assert source.is_dir()
        assert not target.exists()
        input_ = 'Blue~Score gg cp more'
        input_ += ' {} y q'.format(abjad_ide._trim(source))
        abjad_ide._start(input_=input_)
        assert target.exists()
        contents = abjad_ide._io_manager._transcript.contents
        string = 'Blue Score (2017) - segments directory - select:'
        assert string in contents


def test_AbjadIDE_copy_09():
    r'''Preexisting segment directory doesn't break IDE.
    '''

    with ide.Test():
        source = ide.Path('red_score') / 'segments' / 'segment_03'
        assert source.is_dir()
        input_ = 'Red~Score gg cp more'
        input_ += ' {} q'.format(abjad_ide._trim(source))
        abjad_ide._start(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'already exists' in contents


def test_AbjadIDE_copy_10():
    r'''Into stylesheets directory.
    '''

    with ide.Test():
        source = ide.Path('red_score') / 'stylesheets' / 'stylesheet.ily'
        target = ide.Path('blue_score') / 'stylesheets' / 'stylesheet.ily'
        assert not target.exists()
        input_ = 'Blue~Score yy cp more'
        input_ += ' {} y q'.format(abjad_ide._trim(source))
        abjad_ide._start(input_=input_)
        assert target.exists()
        contents = abjad_ide._io_manager._transcript.contents
        string = 'Blue Score (2017) - stylesheets directory - select:'
        assert string in contents


def test_AbjadIDE_copy_11():
    r'''Into test directory.
    '''

    with ide.Test():
        source = ide.Path('red_score') / 'test' / 'test_dummy.py'
        target = ide.Path('blue_score') / 'test' / 'test_dummy.py'
        assert not target.exists()
        input_ = 'Blue~Score tt cp more'
        input_ += ' {} y q'.format(abjad_ide._trim(source))
        abjad_ide._start(input_=input_)
        assert target.exists()
        contents = abjad_ide._io_manager._transcript.contents
        assert 'Blue Score (2017) - test directory - select:' in contents
