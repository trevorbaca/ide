import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_run_tests_01():

    abjad_ide('red ## q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score')
    assert f'Collecting {path.trim()} ...' in transcript
    assert f'Running doctest on 1 module ...' in transcript
    assert f'Running pytest on 1 module ...' in transcript
