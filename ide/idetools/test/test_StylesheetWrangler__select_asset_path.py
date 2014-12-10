# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide


def test_StylesheetWrangler__select_asset_path_01():

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    wrangler = abjad_ide._stylesheet_wrangler
    input_ = 'clean'
    wrangler._session._pending_input = input_
    path = wrangler._select_asset_path()

    assert path == os.path.join(
        abjad_ide._configuration.example_stylesheets_directory,
        'clean-letter-14.ily',
        )