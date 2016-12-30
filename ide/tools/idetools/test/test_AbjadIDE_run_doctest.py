# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_run_doctest_01():
    r'''In score directory.

    Output paths listed from score directory.
    '''

    input_ = 'red~example~score dt q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    # control characters format blue text
    assert '__metadata__.py \x1b[94mOK\x1b[0m' in contents
    # FIX: make doctest include the build/ directory in output
    #assert 'build/__metadata__.py \x1b[94mOK\x1b[0m' in contents
    #assert 'build/__views__.py \x1b[94mOK\x1b[0m' in contents
    assert 'tools/ScoreTemplate.py \x1b[94mOK\x1b[0m' in contents
    assert '4 of 4 tests pass in 33 modules.'


def test_AbjadIDE_run_doctest_02():
    r'''In tools directory.

    Output paths listed from score directory.
    '''

    input_ = 'red~example~score oo dt q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    # control characters format blue text
    assert '__metadata__.py \x1b[94mOK\x1b[0m' in contents
    # FIX: make doctest include the build/ directory in output
    #assert 'build/__metadata__.py \x1b[94mOK\x1b[0m' in contents
    #assert 'build/__views__.py \x1b[94mOK\x1b[0m' in contents
    assert 'tools/ScoreTemplate.py \x1b[94mOK\x1b[0m' in contents
    assert '4 of 4 tests pass in 33 modules.'


def test_AbjadIDE_run_doctest_03():
    r'''With caret-navigation to doctest a single file.

    Output paths listed from score directory.
    '''

    score_template_path = os.path.join(
        'red_example_score',
        'red_example_score',
        'tools',
        'ScoreTemplate.py',
        )
    input_ = 'red~example~score ^ST q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    line = 'Running doctest on {} ...'.format(score_template_path)
    assert line in contents
    assert 'tools/ScoreTemplate.py \x1b[94mOK\x1b[0m' in contents
    assert '4 passed, 0 failed out of 4 tests in 1 module.' in contents
