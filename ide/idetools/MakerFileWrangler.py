# -*- encoding: utf-8 -*-
import os
from abjad.tools import documentationtools
from abjad.tools import stringtools
from ide.idetools.FileWrangler import FileWrangler


class MakerFileWrangler(FileWrangler):
    r'''Maker file wrangler.

    ..  container:: example

        ::

            >>> session = ide.idetools.Session()
            >>> wrangler = ide.idetools.MakerFileWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            MakerFileWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(MakerFileWrangler, self)
        superclass.__init__(session=session)
        self._asset_identifier = 'maker'
        self._basic_breadcrumb = 'makers'
        self._extension = '.py'
        self._force_lowercase = False
        self._in_library = True
        self._score_storehouse_path_infix_parts = ('makers',)
        self._user_storehouse_path = self._configuration.makers_library

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_maker_files = False

    @staticmethod
    def _file_name_callback(file_name):
        base_name, extension = os.path.splitext(file_name)
        base_name = stringtools.to_upper_camel_case(base_name)
        file_name = base_name + extension
        return file_name

    def _is_valid_directory_entry(self, directory_entry):
        name, extension = os.path.splitext(directory_entry)
        if stringtools.is_upper_camel_case(name):
            if extension == '.py':
                return True
        return False

    ### PUBLIC METHODS ###

    def make_file(self):
        r'''Makes empty file with Unicode header.

        Returns none.
        '''
        self._make_file(
            contents=self._configuration.unicode_directive,
            message='file name',
            )