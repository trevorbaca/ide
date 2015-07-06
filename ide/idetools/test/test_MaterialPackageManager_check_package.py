# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_check_package_01():
    r'''Displays problems only.
    '''

    input_ = 'red~example~score m tempo~inventory ck y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    assert 'Top level (6 assets): OK' in contents
    assert 'found' not in contents
    assert 'missing' not in contents


def test_MaterialPackageManager_check_package_02():
    r'''Displays everything.
    '''

    input_ = 'red~example~score m tempo~inventory ck n q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    lines = [
        '3 of 3 required files found:',
        '3 optional files found:',
        ]
    for line in lines:
        assert line in contents
    assert 'No problem assets found.' not in contents


def test_MaterialPackageManager_check_package_03():
    r'''Supplies missing directory and missing file.
    '''

    material_directory = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        )
    initializer = os.path.join(material_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[initializer]):
        os.remove(initializer)
        input_ = 'red~example~score m tempo~inventory ck y y q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(initializer)