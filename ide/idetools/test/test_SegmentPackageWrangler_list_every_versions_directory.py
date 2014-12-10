# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_list_every_versions_directory_01():

    input_ = 'red~example~score g vl* q'
    abjad_ide._run(input_=input_)
    transcript_lines = abjad_ide._transcript.lines

    lines = [
        '> vl*',
        'A:',
        '    definition_0001.py illustration_0001.ly illustration_0001.pdf',
        'B:',
        '    definition_0001.py illustration_0001.ly illustration_0001.pdf',
        'C:',
        '    definition_0001.py illustration_0001.ly illustration_0001.pdf',
        ]
    for line in lines:
        assert line in transcript_lines