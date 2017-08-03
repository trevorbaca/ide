import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_publish_score_pdf_01():

    score_pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'distribution',
        'red-example-score-score.pdf',
        )

    assert os.path.exists(score_pdf_path)

    with abjad.FilesystemState(keep=[score_pdf_path]):
        os.remove(score_pdf_path)
        input_ = 'red~example~score bb letter-portrait spp q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(score_pdf_path)
        contents = abjad_ide._io_manager._transcript.contents

    assert 'Copied' in contents
    assert 'FROM' in contents
    assert 'TO' in contents
