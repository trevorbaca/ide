# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import abjadide
pytest.skip('fails when run after __doc__ test file.')


def test_abjadide___import___01():
    r'''Do not import materials because any in-progress code that raises
    exceptions will prevent the entire system from starting.
    '''

    assert 'materials' not in dir(abjadide)