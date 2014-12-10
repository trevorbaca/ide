# -*- encoding: utf-8 -*-
from abjad import *
import ide
session = abjad_ide.idetools.Session(is_test=True)


def test_ScorePackageWrangler__list_storehouse_paths_01():
    r'''Lists example score packages directory.
    '''

    wrangler = abjad_ide.idetools.ScorePackageWrangler(session=session)
    result = wrangler._list_storehouse_paths(
        abjad_material_packages_and_stylesheets=False,
        example_score_packages=True,
        library=False,
        user_score_packages=False,
        )

    paths = [
        wrangler._configuration.example_score_packages_directory,
        ]
    assert result == paths