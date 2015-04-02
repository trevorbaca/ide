# -*- encoding: utf-8 -*-
import os
import sys
import traceback
from abjad import persist
from experimental.tools import makertools
from abjad.tools import rhythmmakertools


if __name__ == '__main__':
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_py_path = os.path.join(
        current_directory,
        'output.py',
        )
    _, material_name = os.path.split(current_directory)

    try:
        import definition
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        result = getattr(definition, material_name)
    except AttributeError:
        sys.exit(1)

    try:
        output_material = result()
    except TypeError:
        # ok to swallow this exception; doesn't indicate a problem
        #traceback.print_exc()
        output_material = result

    prototype = (
        rhythmmakertools.RhythmMaker,
        makertools.DivisionMaker,
        )
    if isinstance(result, prototype):
        output_material = result

    try:
        persist(output_material).as_module(
            output_py_path,
            material_name,
            )
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)