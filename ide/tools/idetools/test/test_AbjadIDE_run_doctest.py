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
    assert abjad_ide._io_manager._session._attempted_method == '_run_doctest'


def test_AbjadIDE_run_doctest_02():
    r'''In tools directory.

    Output paths listed from score directory.
    '''

    input_ = 'red~example~score oo dt q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._session._attempted_method == '_run_doctest'


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
    assert abjad_ide._io_manager._session._attempted_method == '_run_doctest'
