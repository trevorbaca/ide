# -*- coding: utf-8 -*-
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_search_01():
    r'''In scores directory.
    '''

    input_ = 'sr RhythmMaker q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    ack_line = 'blue_example_score/blue_example_score/materials/talea_rhythm_maker/definition.py:5:'
    ack_line += 'talea_rhythm_maker = rhythmmakertools.TaleaRhythmMaker('
    grep_line = 'blue_example_score/blue_example_score/materials/talea_rhythm_maker/definition.py:'
    grep_line += 'talea_rhythm_maker = rhythmmakertools.TaleaRhythmMaker('
    assert ack_line in contents or grep_line in contents
    ack_line = 'red_example_score/red_example_score/makers/RhythmMaker.py:5:'
    ack_line += 'class RhythmMaker(rhythmmakertools.RhythmMaker):'
    grep_line = 'red_example_score/red_example_score/makers/RhythmMaker.py:'
    grep_line += 'class RhythmMaker(rhythmmakertools.RhythmMaker):'
    assert ack_line in contents or grep_line in contents


def test_AbjadIDE_search_02():
    r'''In score directory.
    '''

    input_ = 'red~example~score sr RhythmMaker q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    ack_line = 'blue_example_score/blue_example_score/materials/talea_rhythm_maker/definition.py:5:'
    ack_line += 'talea_rhythm_maker = rhythmmakertools.TaleaRhythmMaker('
    grep_line = 'blue_example_score/blue_example_score/materials/talea_rhythm_maker/definition.py:'
    grep_line += 'talea_rhythm_maker = rhythmmakertools.TaleaRhythmMaker('
    assert not ack_line in contents and not grep_line in contents
    ack_line = 'makers/RhythmMaker.py:5:'
    ack_line += 'class RhythmMaker(rhythmmakertools.RhythmMaker):'
    grep_line = 'makers/RhythmMaker.py:'
    grep_line += 'class RhythmMaker(rhythmmakertools.RhythmMaker):'
    assert ack_line in contents or grep_line in contents