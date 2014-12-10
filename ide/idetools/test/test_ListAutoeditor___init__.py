# -*- encoding: utf-8 -*-
import os
from abjad import *
import abjad_ide
configuration = abjad_ide.idetools.Configuration()


def test_ListAutoeditor___init___01():
    r'''Initializes correctly when current working directory is the score
    manager directory.
    '''

    os.chdir(configuration.score_manager_directory)
    session = abjad_ide.idetools.Session()
    autoeditor = abjad_ide.idetools.ListAutoeditor(session=session)
    assert isinstance(autoeditor, abjad_ide.idetools.ListAutoeditor)


def test_ListAutoeditor___init___02():
    r'''Initializes correctly when current working directory is a directory
    other than the Abjad IDE directory.
    '''

    os.chdir(configuration.abjad_directory)
    session = abjad_ide.idetools.Session()
    autoeditor = abjad_ide.idetools.ListAutoeditor(session=session)
    assert isinstance(autoeditor, abjad_ide.idetools.ListAutoeditor)