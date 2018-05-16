import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_illustration_ly_01():
    r'''In segment directory.
    '''

    abjad_ide('red %A ile q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score', 'segments', 'A', 'illustration.ly')
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_illustration_ly_02():
    r'''In segments directory.
    '''

    abjad_ide('red gg ile q')
    transcript = abjad_ide.io.transcript

    for name in ['_', 'A', 'B']:
        path = ide.Path('red_score', 'segments', name, 'illustration.ly')
        assert f'Editing {path.trim()} ...' in transcript
