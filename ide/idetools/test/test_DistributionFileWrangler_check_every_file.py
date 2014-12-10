# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_check_every_file_01():
    r'''Works in distribution directory.
    '''

    input_ = 'red~example~score d ck* y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Distribution directory (2 files): OK' in contents


def test_DistributionFileWrangler_check_every_file_02():
    r'''Works in distribution depot.
    '''

    input_ = 'dd ck* q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Distribution depot' in contents


def test_DistributionFileWrangler_check_every_file_03():
    r'''Reports unrecognized file. Distribution files must be dash case.
    '''

    false_file = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'distribution',
        'false_file.txt',
        )

    with systemtools.FilesystemState(remove=[false_file]):
        with open(false_file, 'w') as file_pointer:
            file_pointer.write('')
        input_ = 'red~example~score d ck* y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents

    assert '1 unrecognized file found:' in contents