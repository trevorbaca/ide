import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_run_tests_01():

    abjad_ide('red~score tests q')
    transcript = abjad_ide.io.transcript
    assert f'Running doctest on red_score ...' in transcript
    assert f'Running pytest on red_score ...' in transcript
