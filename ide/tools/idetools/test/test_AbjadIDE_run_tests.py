import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_run_tests_01():

    path = ide.PackagePath('red_score')

    input_ = 'red~score tests q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert f'Running doctest on {path} ...' in transcript
    assert f'Running pytest on {path} ...' in transcript
