# -*- encoding: utf-8 -*-
from abjad import *
import ide


def test_MaterialPackageWrangler_go_to_next_package_01():

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m > > > > > > q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - magic numbers',
        'Red Example Score (2013) - materials directory - performer inventory',
        'Red Example Score (2013) - materials directory - pitch range inventory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - materials directory - time signatures',
        'Red Example Score (2013) - materials directory - magic numbers',
        ]
    assert abjad_ide._transcript.titles == titles


def test_MaterialPackageWrangler_go_to_next_package_02():
    r'''State is maintained cleanly moving between different types of sibling
    asset.
    '''

    abjad_ide = ide.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m > > g > > q'
    abjad_ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - magic numbers',
        'Red Example Score (2013) - materials directory - performer inventory',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013) - segments directory - B',
        ]
    assert abjad_ide._transcript.titles == titles