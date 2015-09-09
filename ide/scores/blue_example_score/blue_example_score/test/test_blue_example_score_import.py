# -*- coding: utf-8 -*-


def test_blue_example_score_import_01():
    from ide.tools import idetools
    configuration = idetools.AbjadIDEConfiguration()
    configuration._add_example_score_to_sys_path()
    import blue_example_score