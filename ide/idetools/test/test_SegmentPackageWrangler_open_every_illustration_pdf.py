# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_open_every_illustration_pdf_01():

    input_ = 'red~example~score g io* y q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file