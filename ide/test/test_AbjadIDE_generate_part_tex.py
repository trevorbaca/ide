import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_generate_part_tex_01():
    
    with ide.Test():
        parts = ide.Path('green_score', 'builds', 'arch-a-parts')
        assert not parts.exists()

        abjad_ide('gre bb new parts arch-a-parts arch~a ARCH-A y q')
        path = parts / 'bass-clarinet' / 'bass-clarinet-part.tex'
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-parts ptg bass q')
        transcript = abjad_ide.io.transcript
        assert f'Writing {path.trim()} ...' in transcript
        assert path.is_file()

        """
        Works when part.tex is missing, too.
        """

        path.remove()
        assert not path.exists()

        abjad_ide('gre bb arch-a-parts ptg bass q')
        transcript = abjad_ide.io.transcript
        assert f'Writing {path.trim()} ...' in transcript
        assert path.is_file()
