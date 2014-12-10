# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_MaterialPackageWrangler_display_every_asset_status_01():
    r'''Work with Git outside of score.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'mm rst* q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MaterialPackageWrangler_display_every_asset_status_02():
    r'''Work with Git inside score.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m rst* q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MaterialPackageWrangler_display_every_asset_status_03():
    r'''Work with Subversion outside of score.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    wrangler = abjad_ide._material_package_wrangler
    manager = wrangler._find_svn_manager(inside_score=False)
    if not manager:
        return
    manager.display_status()
    contents = manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MaterialPackageWrangler_display_every_asset_status_04():
    r'''Work with Subversion inside score.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    wrangler = abjad_ide._material_package_wrangler
    manager = wrangler._find_svn_manager(inside_score=True)
    if not manager:
        return
    manager.display_status()
    contents = manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents