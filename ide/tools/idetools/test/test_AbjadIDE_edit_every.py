import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_every_01():
    r'''Works in scores directory.
    '''

    input_ = 'ee* foo q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert 'Enter search string]> foo' in transcript


def test_AbjadIDE_edit_every_02():
    r'''Works in score directory.
    '''

    input_ = 'red~score ee* foo q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._transcript
    assert 'Enter search string]> foo' in transcript
