import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_quit_abjad_ide_01():

    input_ = 'q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert contents


def test_AbjadIDE_quit_abjad_ide_02():

    input_ = 'red~score bb q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert contents
