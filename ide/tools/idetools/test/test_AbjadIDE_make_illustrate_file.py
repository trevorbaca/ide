import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_make_illustrate_file_01():

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        '__illustrate__.py',
        )

    with abjad.FilesystemState(keep=[path]):
        assert os.path.isfile(path)
        os.remove(path)
        assert not os.path.isfile(path)
        input_ = 'red~example~score mm magic~numbers illm q'
        abjad_ide._start(input_=input_)

    assert os.path.isfile(path)
    contents = abjad_ide._io_manager._transcript.contents
    assert '1: __illustrate__.py' in contents


def test_AbjadIDE_make_illustrate_file_02():
    r'''Does not overwrite existing illustrate file.
    '''

    path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        '__illustrate__.py',
        )

    with abjad.FilesystemState(keep=[path]):
        assert os.path.isfile(path)
        input_ = 'red~example~score mm magic~numbers illm q'
        abjad_ide._start(input_=input_)

    assert os.path.isfile(path)
    contents = abjad_ide._io_manager._transcript.contents
    assert 'File already exists:' in contents
