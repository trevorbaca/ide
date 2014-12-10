# -*- encoding: utf-8 -*-
import shutil
from abjad import *
import abjadide


def test_ScorePackageWrangler___repr___01():

    session = abjadide.idetools.Session(is_test=True)
    wrangler = abjadide.idetools.ScorePackageWrangler(session=session)

    assert repr(wrangler) == 'ScorePackageWrangler()'