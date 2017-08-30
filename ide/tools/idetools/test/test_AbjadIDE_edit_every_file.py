import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_edit_every_file_01():

    input_ = 'red~score mm ff* definition.py q'
    abjad_ide._start(input_=input_)
