# -*- encoding: utf-8 -*-
import os
from ide.idetools.PackageWrangler import PackageWrangler


class ScorePackageWrangler(PackageWrangler):
    r'''Score package wrangler.

    ..  container:: example

        ::

            >>> session = ide.idetools.Session()
            >>> wrangler = ide.idetools.ScorePackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            ScorePackageWrangler()

    ..  container:: example

        ::

            >>> session = ide.idetools.Session()
            >>> session._set_test_score('red_example_score')
            >>> wrangler_in_score = ide.idetools.ScorePackageWrangler(
            ...     session=session,
            ...     )
            >>> wrangler_in_score
            ScorePackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE METHODS ###

    def _list_asset_paths(
        self,
        example_score_packages=True,
        user_score_packages=True,
        valid_only=True,
        ):
        result = []
        directories = self._list_storehouse_paths(
            example_score_packages=example_score_packages,
            user_score_packages=user_score_packages,
            )
        for directory in directories:
            if not directory:
                continue
            if not os.path.exists(directory):
                continue
            directory_entries = sorted(os.listdir(directory))
            for directory_entry in directory_entries:
                if valid_only:
                    if not self._is_valid_directory_entry(directory_entry):
                        continue
                path = os.path.join(directory, directory_entry)
                # test for installable Python package structure
                outer_init_path = os.path.join(path, '__init__.py')
                inner_directory = os.path.join(path, directory_entry)
                inner_init_path = os.path.join(inner_directory, '__init__.py')
                if not os.path.exists(outer_init_path):
                    if os.path.exists(inner_init_path):
                        path = inner_directory
                result.append(path)
        return result