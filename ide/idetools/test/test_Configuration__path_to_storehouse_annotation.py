# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
configuration = ide.idetools.Configuration()


def test_Configuration__path_to_storehouse_annotation_01():
    r'''Score paths annotate score title.
    '''

    path = os.path.join(
        configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        )
    annotation = configuration._path_to_storehouse_annotation(path)
    assert annotation == 'Red Example Score'