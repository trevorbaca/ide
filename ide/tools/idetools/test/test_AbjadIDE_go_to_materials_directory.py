# -*- coding: utf-8 -*-
import abjad
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_materials_directory_01():
    r'''From build directory.
    '''

    input_ = 'red~example~score bb mm q'
    abjad_ide._start(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - materials directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_materials_directory_02():
    r'''Makes sure 'inventories first' view is in effect.
    '''

    input_ = 'red~example~score mm q'
    abjad_ide._start(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert '5: performer inventory' in contents
    assert '6: pitch range inventory' in contents
    assert '7: tempo inventory' in contents
    assert '8: magic numbers' in contents
    assert '9: time signatures' in contents