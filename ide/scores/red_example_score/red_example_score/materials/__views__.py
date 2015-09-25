# -*- coding: utf-8 -*-
from abjad import *
from ide.tools import idetools


view_inventory=idetools.ViewInventory(
    [
        (
            'inventories first',
            idetools.View([
                "'inventory' in :ds:",
                "'inventory' not in :ds:",
                ]),
            ),
        ]
    )