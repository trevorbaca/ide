# -*- coding: utf-8 -*-
from abjad import *
from ide.tools import idetools


view_inventory=idetools.ViewInventory(
    [
        (
            'reverse',
            idetools.View([
                'segment 02',
                'segment 01',
                ]),
            ),
        ]
    )