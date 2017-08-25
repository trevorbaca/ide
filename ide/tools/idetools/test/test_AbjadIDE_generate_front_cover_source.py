import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_front_cover_source_01():

    with ide.Test():
        path = ide.Path('red_score').build / 'letter' / 'front-cover.tex'
        path.remove()
        input_ = 'red~score bb letter fcg q'
        abjad_ide._start(input_=input_)
        assert path.is_file()
        contents = abjad_ide._io_manager._transcript.contents
        assert f'Removing {abjad_ide._trim(path)} ...' not in contents
        assert f'Writing {abjad_ide._trim(path)} ...' in contents
        input_ = 'red~score bb letter fcg q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert f'Removing {abjad_ide._trim(path)} ...' in contents
        assert f'Writing {abjad_ide._trim(path)} ...' in contents
