# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_SegmentPackageWrangler__make_asset_menu_section_01():
    r'''Omits score annotation when listing segments in score.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    string = 'Red Example Score (2013) - segments'
    assert string in contents
    assert 'A\n' in contents