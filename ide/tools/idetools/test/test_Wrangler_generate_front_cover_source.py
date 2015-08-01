# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_Wrangler_generate_front_cover_source_01():
    r'''Works when front cover source already exists.

    (Front cover source already exists in Red Example Score.)
    '''

    cover_path = os.path.join(
        abjad_ide._session._configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'front-cover.tex',
        )

    with systemtools.FilesystemState(keep=[cover_path]):
        input_ = 'red~example~score u fcg y q'
        abjad_ide._run(input_=input_)
        assert filecmp.cmp(cover_path, cover_path + '.backup')

    contents = abjad_ide._session._transcript.contents
    assert 'The files ...' in contents
    assert '... compare the same.' in contents
    assert 'Preserved' in contents


def test_Wrangler_generate_front_cover_source_02():
    r'''Works when front cover source doesn't exist.

    (Front cover source does exist in Red Example Score.)
    '''

    cover_path = os.path.join(
        abjad_ide._session._configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'front-cover.tex',
        )

    with systemtools.FilesystemState(keep=[cover_path]):
        os.remove(cover_path)
        assert not os.path.exists(cover_path)
        input_ = 'red~example~score u fcg q'
        abjad_ide._run(input_=input_)
        assert filecmp.cmp(cover_path, cover_path + '.backup')

    contents = abjad_ide._session._transcript.contents
    assert 'Wrote' in contents