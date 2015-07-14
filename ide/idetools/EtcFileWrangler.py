# -*- encoding: utf-8 -*-
from ide.idetools.FileWrangler import FileWrangler


class EtcFileWrangler(FileWrangler):
    r'''Etc file wrangler.

    ..  container:: example

        ::

            >>> session = ide.idetools.Session()
            >>> wrangler = ide.idetools.EtcFileWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            EtcFileWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(EtcFileWrangler, self)
        superclass.__init__(session=session)
        self._basic_breadcrumb = 'etc'
        self._score_storehouse_path_infix_parts = ('etc',)

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_etc_files = False