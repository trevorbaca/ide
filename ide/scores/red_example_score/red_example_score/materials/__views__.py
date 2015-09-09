# -*- coding: utf-8 -*-
from abjad import *
from ide.tools import idetools


view_inventory=idetools.ViewInventory(
    [
        (
            'inventories',
            idetools.View(
                ["'inventory' in :ds:"]
                ),
            ),
        (
            'magic',
            idetools.View(
                ["'magic_' in :path:"]
                ),
            ),
        ]
    )