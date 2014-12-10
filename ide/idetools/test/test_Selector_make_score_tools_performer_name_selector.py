# -*- encoding: utf-8 -*-
from abjad import *
import abjad_ide
session = abjad_ide.idetools.Session(is_test=True)


def test_Selector_make_score_tools_performer_name_selector_01():

    selector = abjad_ide.idetools.Selector(session=session)
    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    selector._session._pending_input = 'q'
    assert selector._run() is None

    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    selector._session._pending_input = 'b'
    assert selector._run() is None

    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    selector._session._pending_input = 'ss'
    assert selector._run() is None


def test_Selector_make_score_tools_performer_name_selector_02():

    session._reinitialize()
    selector = abjad_ide.idetools.Selector(session=session)
    selector = selector.make_score_tools_performer_name_selector()
    selector._session._is_test = True
    selector._session._pending_input = 'vn'
    assert selector._run() == 'violinist'


def test_Selector_make_score_tools_performer_name_selector_03():

    session._reinitialize()
    selector = abjad_ide.idetools.Selector(session=session)
    selector = selector.make_score_tools_performer_name_selector(
        is_ranged=True)
    selector._session._is_test = True
    result = ['violinist', 'violist']
    selector._session._pending_input = 'vn, va'
    assert selector._run() == result