# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import handlertools
import ide


def test_ReiteratedDynamicHandler_autoedit_01():
    r'''Edits reiterated dynamic handler.
    '''

    session = ide.idetools.Session(is_test=True)
    session._autoadvance_depth = 1
    target = handlertools.ReiteratedDynamicHandler()
    autoeditor = ide.idetools.Autoeditor(
        session=session,
        target=target
        )
    input_ = 'f Duration(1, 8) q'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 8),
        )

    assert autoeditor.target == handler