import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_run_pytest_01():

    target = ide.PackagePath('red_score')

    input_ = 'red~score pt q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert f'Running pytest on {target} ...' in transcript
