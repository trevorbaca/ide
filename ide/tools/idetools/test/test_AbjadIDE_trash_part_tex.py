import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_trash_part_tex_01():

    with ide.Test():
        parts = ide.Path('green_score', 'builds', 'arch-a-parts')
        path = parts('bass-clarinet-part.tex')
        assert not parts.exists()

        abjad_ide('gre bb parts arch-a-parts arch~a ARCH-A y q')
        assert path.is_file()

        abjad_ide('gre bb arch-a-parts ptt bass q')
        transcript = abjad_ide.io.transcript
        assert f'Trashing {path.trim()} ...' in transcript
        assert not path.exists()
