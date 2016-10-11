# -*- coding: utf-8 -*-
import ide
import os
from abjad import *
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_generate_front_cover_source_01():
    r'''Works when front cover source already exists.

    (Front cover source already exists in Red Example Score.)
    '''

    cover_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'front-cover.tex',
        )

    with systemtools.FilesystemState(keep=[cover_path]):
        os.remove(cover_path)
        # generate first time
        input_ = 'red~example~score bb letter-portrait fcg q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(cover_path)
        # attempt to generate second time
        input_ = 'red~example~score bb letter-portrait fcg q'
        abjad_ide._start(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Preserving' in contents


def test_AbjadIDE_generate_front_cover_source_02():
    r'''Works when front cover source doesn't exist.

    (Front cover source does exist in Red Example Score.)
    '''

    cover_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'front-cover.tex',
        )

    with systemtools.FilesystemState(keep=[cover_path]):
        os.remove(cover_path)
        assert not os.path.exists(cover_path)
        input_ = 'red~example~score bb letter-portrait fcg q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(cover_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Writing' in contents