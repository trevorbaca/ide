import ide
import shutil
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_go_to_test_directory_01():
    r'''From material directory.
    '''

    abjad_ide('red mm tempi tt q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : materials',
        'Red Score (2017) : materials : tempi',
        'Red Score (2017) : test',
        ]
    assert '.gitignore' not in transcript


def test_AbjadIDE_go_to_test_directory_02():
    r'''From segment directory.
    '''

    abjad_ide('red gg A tt q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : segments',
        'Red Score (2017) : segments : A',
        'Red Score (2017) : test',
        ]


def test_AbjadIDE_go_to_test_directory_03():
    r'''From builds directory to test directory.
    '''

    abjad_ide('red bb tt q')
    transcript = abjad_ide.io.transcript
    assert transcript.titles == [
        'Abjad IDE : scores',
        'Red Score (2017)',
        'Red Score (2017) : builds',
        'Red Score (2017) : test',
        ]


def test_AbjadIDE_go_to_test_directory_04():
    r'''No explosions if test directory is missing.
    '''

    with ide.Test():
        test_directory = ide.Path('red_score').test()
        shutil.rmtree(str(test_directory))

        abjad_ide('red tt q')
        transcript = abjad_ide.io.transcript
        assert f'Missing {test_directory.trim()} ...' in transcript


def test_AbjadIDE_go_to_test_directory_05():
    r'''Filenames appear correctly.
    '''

    abjad_ide('red tt q')
    transcript = abjad_ide.io.transcript
    assert '1: test_materials.py' in transcript
    assert '2: test_segments.py' in transcript
