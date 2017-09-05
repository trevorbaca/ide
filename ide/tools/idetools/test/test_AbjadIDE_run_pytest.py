import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_run_pytest_01():

    abjad_ide('red~score pt q')
    transcript = abjad_ide.io_manager.transcript
    target = ide.Path('red_score')
    assert f'Running pytest on {target} ...' in transcript
