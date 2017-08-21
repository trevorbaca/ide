import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_replace_01():
    r'''In score directory.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'tools',
        'RhythmMaker.py',
        )

    with abjad.FilesystemState(keep=[path]):
        input_ = 'red~example~score sr RhythmMaker q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert 'class RhythmMaker(abjad.rhythmmakertools.RhythmMaker):' in contents
        input_ = 'red~example~score rp RhythmMaker FooMaker y q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert 'Replaced 2 instances over 1 line in 1 file.' in contents
        input_ = 'red~example~score rp FooMaker RhythmMaker y q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert 'Replaced 2 instances over 1 line in 1 file.' in contents
