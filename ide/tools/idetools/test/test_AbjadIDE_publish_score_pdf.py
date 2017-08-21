import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_publish_score_pdf_01():

    score_pdf_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'distribution',
        'red-example-score-score.pdf',
        )

    assert score_pdf_path.exists()

    with abjad.FilesystemState(keep=[score_pdf_path]):
        score_pdf_path.unlink()
        input_ = 'red~example~score bb letter-portrait spp q'
        abjad_ide._start(input_=input_)
        assert score_pdf_path.exists()
        contents = abjad_ide._io_manager._transcript.contents

    assert 'Copied' in contents
    assert 'FROM' in contents
    assert 'TO' in contents
