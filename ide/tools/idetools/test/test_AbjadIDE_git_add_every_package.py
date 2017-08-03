import ide


def test_AbjadIDE_git_add_every_package_01():
    r'''Flow control reaches add.
    '''

    abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
    input_ = 'add* q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._session._attempted_method == 'git_add_every_package'
