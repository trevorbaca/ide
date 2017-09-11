import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_run_tests_01():

    abjad_ide('red~score tests q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score')
    assert f'Running doctest on {path} ...' in transcript
    assert f'Running pytest on {path} ...' in transcript
