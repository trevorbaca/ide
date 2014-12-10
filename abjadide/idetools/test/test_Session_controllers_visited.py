# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import abjadide
configuration = abjadide.idetools.Configuration()

score_path = os.path.join(
    configuration.example_score_packages_directory,
    'red_example_score',
    )
tempo_inventory_path = os.path.join(
    score_path,
    'tempo_inventory',
    )
segment_path = os.path.join(
    score_path,
    'segments',
    'segment_01',
    )


def test_Session_controllers_visited_01():
    r'''Abjad IDE.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    input_ = 'q'
    ide._run(input_=input_)

    session = abjadide.idetools.Session(is_test=True)
    controllers = [
        abjadide.idetools.AbjadIDE(session=session, is_test=True),
        abjadide.idetools.ScorePackageWrangler(session=session),
        abjadide.idetools.Menu(session=session),
        ]
    assert ide._session.controllers_visited == controllers


def test_Session_controllers_visited_02():
    r'''Score package manager.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score q'
    ide._run(input_=input_)

    session = abjadide.idetools.Session(is_test=True)
    controllers = [
        abjadide.idetools.AbjadIDE(session=session, is_test=True),
        abjadide.idetools.ScorePackageWrangler(session=session),
        abjadide.idetools.Menu(session=session),
        abjadide.idetools.ScorePackageManager(
            path=score_path,
            session=session,
            ),
        ]
    assert ide._session.controllers_visited == controllers


def test_Session_controllers_visited_03():
    r'''Build file wrangler.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score u q'
    ide._run(input_=input_)

    session = abjadide.idetools.Session(is_test=True)
    controllers = [
        abjadide.idetools.AbjadIDE(session=session, is_test=True),
        abjadide.idetools.ScorePackageWrangler(session=session),
        abjadide.idetools.Menu(session=session),
        abjadide.idetools.ScorePackageManager(
            session=session,
            path=score_path,
            ),
        abjadide.idetools.BuildFileWrangler(session=session),
        ]
    assert ide._session.controllers_visited == controllers


def test_Session_controllers_visited_04():
    r'''Material package manager.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m q'
    ide._run(input_=input_)

    session = abjadide.idetools.Session(is_test=True)
    controllers = [
        abjadide.idetools.AbjadIDE(session=session, is_test=True),
        abjadide.idetools.ScorePackageWrangler(session=session),
        abjadide.idetools.Menu(session=session),
        abjadide.idetools.ScorePackageManager(
            path=score_path,
            session=session,
            ),
        abjadide.idetools.MaterialPackageWrangler(session=session),
        ]
    assert ide._session.controllers_visited == controllers


def test_Session_controllers_visited_05():
    r'''Material package manager.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory q'
    ide._run(input_=input_)

    session = abjadide.idetools.Session(is_test=True)
    controllers = [
        abjadide.idetools.AbjadIDE(session=session, is_test=True),
        abjadide.idetools.ScorePackageWrangler(session=session),
        abjadide.idetools.Menu(session=session),
        abjadide.idetools.ScorePackageManager(
            path=score_path,
            session=session,
            ),
        abjadide.idetools.MaterialPackageWrangler(session=session),
        abjadide.idetools.MaterialPackageManager(
            path=tempo_inventory_path,
            session=session,
            ),
        ]
    assert ide._session.controllers_visited == controllers


def test_Session_controllers_visited_06():
    r'''Segment wrangler.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g q'
    ide._run(input_=input_)

    session = abjadide.idetools.Session(is_test=True)
    controllers = [
        abjadide.idetools.AbjadIDE(session=session, is_test=True),
        abjadide.idetools.ScorePackageWrangler(session=session),
        abjadide.idetools.Menu(session=session),
        abjadide.idetools.ScorePackageManager(
            path=score_path,
            session=session,
            ),
        abjadide.idetools.SegmentPackageWrangler(session=session),
        ]
    assert ide._session.controllers_visited == controllers


def test_Session_controllers_visited_07():
    r'''Segment package manager.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g 1 q'
    ide._run(input_=input_)

    session = abjadide.idetools.Session(is_test=True)
    controllers = [
        abjadide.idetools.AbjadIDE(session=session, is_test=True),
        abjadide.idetools.ScorePackageWrangler(session=session),
        abjadide.idetools.Menu(session=session),
        abjadide.idetools.ScorePackageManager(
            path=score_path,
            session=session,
            ),
        abjadide.idetools.SegmentPackageWrangler(session=session),
        abjadide.idetools.SegmentPackageManager(
            path=segment_path,
            session=session,
            ),
        ]
    assert ide._session.controllers_visited == controllers


def test_Session_controllers_visited_08():
    r'''Stylesheet file wrangler.
    '''

    ide = abjadide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score y q'
    ide._run(input_=input_)

    session = abjadide.idetools.Session(is_test=True)
    controllers = [
        abjadide.idetools.AbjadIDE(session=session, is_test=True),
        abjadide.idetools.ScorePackageWrangler(session=session),
        abjadide.idetools.Menu(session=session),
        abjadide.idetools.ScorePackageManager(
            path=score_path,
            session=session,
            ),
        abjadide.idetools.StylesheetWrangler(session=session),
        ]
    assert ide._session.controllers_visited == controllers