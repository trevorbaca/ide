import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_preface_source_01():

    with ide.Test():
        source = ide.Path('boilerplate') / 'preface.tex'
        text = source.read_text()
        assert 'paper_size' in text
        assert '{8.5in, 11in}' not in text
        target = ide.Path('blue_score').build / 'letter' / 'preface.tex'
        input_ = 'blue~score bb letter pg q'
        abjad_ide._start(input_=input_)
        assert target.is_file()
        text = target.read_text()
        assert 'paper_size' not in text
        assert '{8.5in, 11in}' in text
        contents = abjad_ide._io_manager._transcript.contents
        assert f'Writing {abjad_ide._trim(target)} ...' in contents
