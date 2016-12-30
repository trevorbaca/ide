# -*- coding: utf-8 -*-
import abjad
import os


def make_lilypond_file():
    r'''Reimplement for material-specific illustration logic.
    '''
    import definition
    material_directory_path = os.path.dirname(os.path.abspath(__file__))
    material_name = os.path.basename(material_directory_path)
    title = material_name.replace('_', ' ').capitalize()
    title = abjad.markuptools.Markup(title)
    title = title.override(('font-name', 'Palatino'))
    material = getattr(definition, material_name)
    try:
        lilypond_file = material.__illustrate__(title=title)
    except TypeError:
        lilypond_file = material.__illustrate__()
    return lilypond_file


lilypond_file = make_lilypond_file()