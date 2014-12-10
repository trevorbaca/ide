# -*- encoding: utf-8 -*-
from abjadide.idetools.FileWrangler import FileWrangler


class DistributionFileWrangler(FileWrangler):
    r'''Distribution wrangler.

    ..  container:: example

        ::

            >>> session = abjadide.idetools.Session()
            >>> wrangler = abjadide.idetools.DistributionFileWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            DistributionFileWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from abjadide import idetools
        superclass = super(DistributionFileWrangler, self)
        superclass.__init__(session=session)
        self._basic_breadcrumb = 'distribution'
        self._score_storehouse_path_infix_parts = ('distribution',)

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_distribution_files = False