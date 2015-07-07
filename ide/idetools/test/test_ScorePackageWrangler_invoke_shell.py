# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_invoke_shell_01():
    r'''Outside of score package.
    '''

    input_ = '!pwd q'
    abjad_ide._run(input_=input_)

    path = os.path.join(
        abjad_ide._configuration.abjad_ide_directory,
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._transcript.contents