# -*- encoding: utf-8 -*-
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_write_cache_01():
    r'''Not necessary to keep cache path with FilesystemState.
    AbjadIDE._run() always preserves cache during tests.
    '''

    input_ = 'cw q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents
    assert 'Wrote' in contents