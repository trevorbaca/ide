import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_IOManager_open_file_01():
    r'''@-addressing to distribution file.
    '''

    abjad_ide('red~score @program-notes.txt q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').distribution
    path /= 'red-score-program-notes.txt'
    assert f'Editing {path.trim()} ...' in transcript


def test_IOManager_open_file_02():
    r'''@-addressing to etc file.
    '''

    abjad_ide('red~score @notes.txt q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').etc / 'notes.txt'
    assert f'Editing {path.trim()} ...' in transcript


def test_IOManager_open_file_03():
    r'''@-addressing to tools file.
    '''

    abjad_ide('red~score @RM q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').tools / 'RhythmMaker.py'
    assert f'Editing {path.trim()} ...' in transcript


def test_IOManager_open_file_04():
    r'''@-addressing to stylesheet.
    '''

    abjad_ide('red~score @style q')
    transcript = abjad_ide.io_manager.transcript
    path = ide.Path('red_score').stylesheets / 'stylesheet.ily'
    assert f'Editing {path.trim()} ...' in transcript
