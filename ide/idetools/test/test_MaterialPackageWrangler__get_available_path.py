# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
configuration = ide.idetools.Configuration()


def test_MaterialPackageWrangler__get_available_path_01():

    session = ide.idetools.Session(is_test=True)
    wrangler = ide.idetools.MaterialPackageWrangler(session=session)

    input_ = 'q'
    wrangler._session._pending_input = input_
    result = wrangler._get_available_path()
    assert result is None

    input_ = 'b'
    wrangler._session._pending_input = input_
    result = wrangler._get_available_path()
    assert result is None

    input_ = 'ss'
    wrangler._session._pending_input = input_
    result = wrangler._get_available_path()
    assert result is None