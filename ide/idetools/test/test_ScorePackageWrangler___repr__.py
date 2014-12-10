# -*- encoding: utf-8 -*-
import shutil
from abjad import *
import abjad_ide


def test_ScorePackageWrangler___repr___01():

    session = abjad_ide.idetools.Session(is_test=True)
    wrangler = abjad_ide.idetools.ScorePackageWrangler(session=session)

    assert repr(wrangler) == 'ScorePackageWrangler()'