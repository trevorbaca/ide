# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_check_output_py_01():

    output_py_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        'output.py',
        )
    exception_file = os.path.join(
        abjad_ide._configuration.boilerplate_directory,
        'exception.py',
        )

    with systemtools.FilesystemState(keep=[output_py_path]):
        input_ = 'red~example~score m magic~numbers oc y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        message = '{} OK.'.format(output_py_path)
        assert message in contents
        shutil.copyfile(exception_file, output_py_path)
        input_ = 'red~example~score m magic~numbers oc y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        message = '{} FAILED:'.format(output_py_path)
        assert message in contents
        assert 'Exception' in contents