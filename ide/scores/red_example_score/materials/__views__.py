# -*- encoding: utf-8 -*-
from abjad import *
from abjad_ide import idetools


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