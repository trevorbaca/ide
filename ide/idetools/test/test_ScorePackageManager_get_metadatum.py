# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True) 
metadata_py_path = os.path.join(
    abjad_ide._configuration.example_score_packages_directory,
    'red_example_score',
    '__metadata__.py',
    )


def test_ScorePackageManager_get_metadatum_01():


    with systemtools.FilesystemState(keep=[metadata_py_path]):
        # make sure no flavor_type metadatum found
        input_ = 'red~example~score mdg flavor_type q'
        abjad_ide._run(input_=input_)
        assert 'None' in abjad_ide._transcript.contents

        # add flavor_type metadatum
        input_ = 'red~example~score mda flavor_type cherry q'
        abjad_ide._run(input_=input_)

        # maker sure flavor_type metadatum now equal to 'cherry'
        input_ = 'red~example~score mdg flavor_type q'
        abjad_ide._run(input_=input_)
        assert "'cherry'" in abjad_ide._transcript.contents