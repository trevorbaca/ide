# -*- encoding: utf-8 -*-
import shutil
from abjad import *
import ide


def test_ScorePackageWrangler___repr___01():

    session = ide.idetools.Session(is_test=True)
    wrangler = ide.idetools.ScorePackageWrangler(session=session)

    assert repr(wrangler) == 'ScorePackageWrangler()'