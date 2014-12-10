# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)
views_file = os.path.join(
    abjad_ide._configuration.wrangler_views_directory,
    '__AbjadIDE_views__.py',
    )


def test_AbjadIDE_autoedit_views_01():

    with systemtools.FilesystemState(keep=[views_file]):
        os.remove(views_file)
        input_ = "hh wa add _test add 'clean-letter'~in~:ds:"
        input_ += " add 'rhythm-letter'~in~:ds: done"
        input_ += " ren _test _new_test"
        input_ += " _new_test rm 'clean-letter done"
        input_ += " rm _new_test done q"
        abjad_ide._run(input_=input_)
        transcript = abjad_ide._transcript

    lines = [
        'Abjad IDE - views - _test (EDIT)',
        '',
        '      elements - add (add)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - views - _test (EDIT+)',
        '',
        "   1: 'clean-letter' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - views - _test (EDIT+)',
        '',
        "   1: 'clean-letter' in :ds:",
        "   2: 'rhythm-letter' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - views (EDIT+)',
        '',
        "   1: _test: 'clean-letter' in :ds:, 'rhythm-letter' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - views (EDIT+)',
        '',
        "   1: _new_test: 'clean-letter' in :ds:, 'rhythm-letter' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - views - _new_test (EDIT)',
        '',
        "   1: 'clean-letter' in :ds:",
        "   2: 'rhythm-letter' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - views - _new_test (EDIT+)',
        '',
        "   1: 'rhythm-letter' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - views (EDIT+)',
        '',
        "   1: _new_test: 'rhythm-letter' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - views (EDIT)',
        '',
        '      elements - add (add)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)