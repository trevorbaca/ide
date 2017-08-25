import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_interpret_back_cover_01():

    with ide.Test():
        tex = ide.Path('red_score').build / 'letter' / 'back-cover.tex'
        pdf = ide.Path('red_score').build / 'letter' / 'back-cover.pdf'
        pdf.unlink()
        assert not pdf.exists()
        input_ = 'red~score bb letter bci q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert pdf.is_file()
        assert f'Removing {abjad_ide._trim(pdf)} ...' not in contents
        assert f'Interpreting {abjad_ide._trim(tex)} ...' in contents
        assert f'Writing {abjad_ide._trim(pdf)} ...' in contents
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert pdf.is_file()
        assert f'Removing {abjad_ide._trim(pdf)} ...' in contents
        assert f'Interpreting {abjad_ide._trim(tex)} ...' in contents
        assert f'Writing {abjad_ide._trim(pdf)} ...' in contents
