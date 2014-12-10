from abjad.tools.datastructuretools.TypedOrderedDict import TypedOrderedDict


class ViewInventory(TypedOrderedDict):
    r'''View inventory.

    .. todo:: add examples.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjadide import idetools
        return idetools.View