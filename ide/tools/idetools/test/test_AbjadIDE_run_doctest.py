import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_run_doctest_01():
    r'''In score directory.
    '''

    abjad_ide('red~score dt q')
    transcript = abjad_ide.io.transcript
    target = ide.Path('red_score')
    assert f'Running doctest on {target} ...' in transcript


def test_AbjadIDE_run_doctest_02():
    r'''In tools directory.
    '''

    abjad_ide('red~score oo dt q')
    transcript = abjad_ide.io.transcript
    target = ide.Path('red_score').tools
    assert f'Running doctest on {target.trim()} ...' in transcript


def test_AbjadIDE_run_doctest_03():
    r'''With caret-navigation to doctest a single file.
    '''

    abjad_ide('red~score ^ST q')
    transcript = abjad_ide.io.transcript
    target = ide.Path('red_score').tools / 'ScoreTemplate.py'
    assert f'Running doctest on {target.trim()} ...' in transcript
