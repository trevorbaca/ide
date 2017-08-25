import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE__make_asset_menu_section_01():
    r'''Behaves gracefully when no assets are found.
    '''

    abjad_ide = ide.AbjadIDE(is_test=True)
    input_ = 'blue~score gg segment~01 q'
    abjad_ide._start(input_=input_)
    titles = [
        'Abjad IDE - scores directory',
        'Blue Score (2017)',
        'Blue Score (2017) - segments directory',
        'Blue Score (2017) - segments directory - segment 01',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE__make_asset_menu_section_02():
    r'''Omits score annotation when listing segments in score.
    '''

    abjad_ide = ide.AbjadIDE(is_test=True)
    input_ = 'red~score gg q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    string = 'Red Score (2017) - segments'
    assert string in contents
    assert 'A\n' in contents


def test_AbjadIDE__make_asset_menu_section_03():
    r'''Behaves gracefully when no materials are found.
    '''

    input_ = 'blue~score mm q'
    abjad_ide._start(input_=input_)
    titles = [
        'Abjad IDE - scores directory',
        'Blue Score (2017)',
        'Blue Score (2017) - materials directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE__make_asset_menu_section_04():
    r'''Omits score annotation inside score.
    '''

    input_ = 'red~score mm q'
    abjad_ide._start(input_=input_)
    assert '(Red Score)' not in abjad_ide._io_manager._transcript.contents
