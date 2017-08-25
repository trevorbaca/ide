import abjad
import pathlib


def make_lilypond_file():
    r'''Reimplement for material-specific illustration logic.
    '''
    import definition
    material_directory = pathlib.Path(__file__).parent
    material_name = material_directory.name
    title = material_name.replace('_', ' ').capitalize()
    title = abjad.Markup(title)
    title = title.override(('font-name', 'Palatino'))
    material = getattr(definition, material_name)
    try:
        lilypond_file = material.__illustrate__(title=title)
    except TypeError:
        lilypond_file = material.__illustrate__()
    return lilypond_file


lilypond_file = make_lilypond_file()
