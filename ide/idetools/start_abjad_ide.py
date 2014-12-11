# -*- encoding: utf-8 -*-


def start_abjad_ide():
    r'''Starts Abjad IDE.

    Returns none.
    '''
    import sys
    import ide
    abjad_ide = ide.idetools.AbjadIDE(is_test=False)
    input_ = ' '.join(sys.argv[1:])
    abjad_ide._run(input_=input_)