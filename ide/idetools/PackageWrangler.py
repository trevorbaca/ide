# -*- encoding: utf-8 -*-
import os
import time
from abjad.tools import stringtools
from ide.idetools.Wrangler import Wrangler


class PackageWrangler(Wrangler):
    r'''Package wrangler.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _command_to_method(self):
        superclass = super(PackageWrangler, self)
        result = superclass._command_to_method
        result = result.copy()
        result.update({
            'ck*': self.check_every_package,
            })
        return result

    ### PUBLIC METHODS ###

    def check_every_package(
        self, 
        indent=0,
        problems_only=None, 
        supply_missing=None,
        ):
        r'''Checks every package.

        Returns none.
        '''
        messages = []
        missing_directories, missing_files = [], []
        supplied_directories, supplied_files = [], []
        tab = indent * self._io_manager._tab
        if problems_only is None:
            prompt = 'show problem assets only?'
            result = self._io_manager._confirm(prompt)
            if self._session.is_backtracking or result is None:
                return messages, missing_directories, missing_files
            problems_only = bool(result)
        managers = self._list_visible_asset_managers()
        found_problem = False
        for manager in managers:
            with self._io_manager._silent():
                result = manager.check_package(
                    return_messages=True,
                    problems_only=problems_only,
                    )
            messages_, missing_directories_, missing_files_ = result
            missing_directories.extend(missing_directories_)
            missing_files.extend(missing_files_)
            messages_ = [stringtools.capitalize_start(_) for _ in messages_]
            messages_ = [tab + _ for _ in messages_]
            if messages_:
                found_problem = True
                messages.extend(messages_)
            else:
                message = 'No problem assets found.'
                message = tab + tab + message
                messages.append(message)
        found_problems = bool(messages)
        if self._session.is_in_score:
            path = self._get_current_directory()
            name = os.path.basename(path)
            count = len(managers)
            message = '{} directory ({} packages):'.format(name, count)
            if not found_problems:
                message = '{} OK'.format(message)
            messages.insert(0, message)
        self._io_manager._display(messages)
        if not found_problem:
            return messages, missing_directories, missing_files
        if supply_missing is None:
            prompt = 'supply missing directories and files?'
            result = self._io_manager._confirm(prompt)
            if self._session.is_backtracking or result is None:
                return messages, missing_directories, missing_files
            supply_missing = bool(result)
        if not supply_missing:
            return messages, missing_directories, missing_files
        messages = []
        for manager in managers:
            with self._io_manager._silent():
                result = manager.check_package(
                    return_supply_messages=True,
                    supply_missing=True,
                    )
            messages_, supplied_directories_, supplied_files_ = result
            supplied_directories.extend(supplied_directories_)
            supplied_files.extend(supplied_files_)
            if messages_:
                messages_ = [tab + tab + _ for _ in messages_]
                messages.extend(messages_)
        self._io_manager._display(messages)
        return messages, supplied_directories, supplied_files