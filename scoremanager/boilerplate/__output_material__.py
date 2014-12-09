# -*- encoding: utf-8 -*-


if __name__ == '__main__':
    from abjad import persist
    import definition
    import os
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_py_path = os.path.join(
        current_directory,
        'output.py',
        )
    _, material_name = os.path.split(current_directory)
    material_object = getattr(definition, material_name)
    persist(material_object).as_module(
        output_py_path,
        material_name,
        )