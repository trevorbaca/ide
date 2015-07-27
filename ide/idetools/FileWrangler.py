# -*- encoding: utf-8 -*-
import glob
import os
import shutil
from abjad.tools import lilypondfiletools
from abjad.tools import stringtools
from abjad.tools import systemtools
from ide.idetools.Wrangler import Wrangler


class FileWrangler(Wrangler):
    r'''File wrangler.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    def check_every_file(self):
        r'''Checks every file.

        Returns none.
        '''
        paths = self._list_asset_paths(valid_only=False)
        paths = [_ for _ in paths if os.path.basename(_)[0].isalpha()]
        paths = [_ for _ in paths if not _.endswith('.pyc')]
        current_directory = self._get_current_directory()
        if current_directory:
            paths = [_ for _ in paths if _.startswith(current_directory)]
        invalid_paths = []
        for path in paths:
            file_name = os.path.basename(path)
            if not self._is_valid_directory_entry(file_name):
                invalid_paths.append(path)
        messages = []
        if not invalid_paths:
            count = len(paths)
            message = '{} ({} files): OK'.format(self._breadcrumb, count)
            messages.append(message)
        else:
            message = '{}:'.format(self._breadcrumb)
            messages.append(message)
            identifier = 'file'
            count = len(invalid_paths)
            identifier = stringtools.pluralize(identifier, count)
            message = '{} unrecognized {} found:'
            message = message.format(count, identifier)
            tab = self._io_manager._tab
            message = tab + message
            messages.append(message)
            for invalid_path in invalid_paths:
                message = tab + tab + invalid_path
                messages.append(message)
        self._io_manager._display(messages)
        missing_files, missing_directories = [], []
        return messages, missing_files, missing_directories

    def collect_segment_lilypond_files(self):
        r'''Copies ``illustration.ly`` files from segment packages to build 
        directory.

        Trims top-level comments, includes and directives from each
        ``illustration.ly`` file.

        Trims header and paper block from each ``illustration.ly`` file.

        Leaves score block in each ``illustration.ly`` file.

        Returns none.
        '''
        pairs = self._collect_segment_files('illustration.ly')
        if not pairs:
            return
        for source_file_path, target_file_path in pairs:
            candidate_file_path = target_file_path.replace(
                '.ly',
                '.candidate.ly',
                )
            with systemtools.FilesystemState(remove=[candidate_file_path]):
                shutil.copyfile(source_file_path, candidate_file_path)
                self._trim_lilypond_file(candidate_file_path)
                self._handle_candidate(candidate_file_path, target_file_path)
                self._io_manager._display('')

    def collect_segment_pdfs(self):
        r'''Copies ``illustration.pdf`` files from segment packages to build 
        directory.

        Returns none.
        '''
        pairs = self._collect_segment_files('illustration.pdf')
        if not pairs:
            return
        for source_file_path, target_file_path in pairs:
            self._handle_candidate(source_file_path, target_file_path)
            self._io_manager._display('')

    def generate_back_cover_source(self):
        r'''Generates ``back-cover.tex``.

        Returns none.
        '''
        replacements = {}
        manager = self._session.current_score_package_manager
        catalog_number = manager._get_metadatum('catalog_number')
        if catalog_number:
            old = 'CATALOG NUMBER'
            new = str(catalog_number)
            replacements[old] = new
        composer_website = self._configuration.composer_website
        if self._session.is_test:
            composer_website = 'www.composer-website.com'
        if composer_website:
            old = 'COMPOSER WEBSITE'
            new = str(composer_website)
            replacements[old] = new
        price = manager._get_metadatum('price')
        if price:
            old = 'PRICE'
            new = str(price)
            replacements[old] = new
        self._copy_boilerplate('back-cover.tex', replacements=replacements)

    def generate_front_cover_source(self):
        r'''Generates ``front-cover.tex``.

        Returns none.
        '''
        file_name = 'front-cover.tex'
        replacements = {}
        manager = self._session.current_score_package_manager
        score_title = manager._get_title()
        if score_title:
            old = 'TITLE'
            new = str(score_title.upper())
            replacements[old] = new
        forces_tagline = manager._get_metadatum('forces_tagline')
        if forces_tagline:
            old = 'FOR INSTRUMENTS'
            new = str(forces_tagline)
            replacements[old] = new
        year = manager._get_metadatum('year')
        if year:
            old = 'YEAR'
            new = str(year)
            replacements[old] = new
        composer = self._configuration.upper_case_composer_full_name
        if self._session.is_test:
            composer = 'EXAMPLE COMPOSER NAME'
        if composer:
            old = 'COMPOSER'
            new = str(composer)
            replacements[old] = new
        self._copy_boilerplate(file_name, replacements=replacements)

    def generate_interpret_open_front_cover(self):
        r'''Generates ``front-cover.tex``.

        Then interprets ``front-cover.tex``.

        Then opens ``front-cover.pdf``.

        Returns none.
        '''
        self.generate_front_cover_source()
        self.interpret_front_cover()
        self.open_front_cover_pdf()
        
    def generate_music_source(self):
        r'''Generates ``music.ly``.

        Returns none.
        '''
        result = self._confirm_segment_names()
        if self._session.is_backtracking or not isinstance(result, list):
            return
        segment_names = result
        lilypond_names = [_.replace('_', '-') for _ in segment_names]
        source_path = os.path.join(
            self._configuration.abjad_ide_directory,
            'boilerplate',
            'music.ly',
            )
        manager = self._session.current_score_package_manager
        destination_path = os.path.join(
            manager._path,
            'build',
            'music.ly',
            )
        candidate_path = os.path.join(
            manager._path,
            'build',
            'music.candidate.ly',
            )
        with systemtools.FilesystemState(remove=[candidate_path]):
            shutil.copyfile(source_path, candidate_path)
            width, height, unit = manager._parse_paper_dimensions()
            old = '{PAPER_SIZE}'
            new = '{{{}{}, {}{}}}'
            new = new.format(width, unit, height, unit)
            self._replace_in_file(candidate_path, old, new)
            lines = []
            for lilypond_name in lilypond_names:
                file_name = lilypond_name + '.ly'
                tab = 4 * ' '
                line = tab + r'\include "{}"'
                line = line.format(file_name)
                lines.append(line)
            if lines:
                new = '\n'.join(lines)
                old = '%%% SEGMENTS %%%'
                self._replace_in_file(candidate_path, old, new)
            else:
                line_to_remove = '%%% SEGMENTS %%%\n'
                self._remove_file_line(candidate_path, line_to_remove)
            stylesheet_path = self._session.current_stylesheet_path
            if stylesheet_path:
                old = '% STYLESHEET_INCLUDE_STATEMENT'
                new = r'\include "../stylesheets/stylesheet.ily"'
                self._replace_in_file(candidate_path, old, new)
            language_token = lilypondfiletools.LilyPondLanguageToken()
            lilypond_language_directive = format(language_token)
            old = '% LILYPOND_LANGUAGE_DIRECTIVE'
            new = lilypond_language_directive
            self._replace_in_file(candidate_path, old, new)
            version_token = lilypondfiletools.LilyPondVersionToken()
            lilypond_version_directive = format(version_token)
            old = '% LILYPOND_VERSION_DIRECTIVE'
            new = lilypond_version_directive
            self._replace_in_file(candidate_path, old, new)
            score_title = manager._get_title()
            if score_title:
                old = 'SCORE_NAME'
                new = score_title
                self._replace_in_file(candidate_path, old, new)
            annotated_title = manager._get_title(year=True)
            if annotated_title:
                old = 'SCORE_TITLE'
                new = annotated_title
                self._replace_in_file(candidate_path, old, new)
            forces_tagline = manager._get_metadatum('forces_tagline')
            if forces_tagline:
                old = 'FORCES_TAGLINE'
                new = forces_tagline
                self._replace_in_file(candidate_path, old, new)
            self._handle_candidate(candidate_path, destination_path)

    def generate_preface_source(self):
        r'''Generates ``preface.tex``.

        Returns none.
        '''
        self._copy_boilerplate('preface.tex')

    def generate_score_source(self):
        r'''Generates ``score.tex``.

        Returns none.
        '''
        self._copy_boilerplate('score.tex')

    def interpret_back_cover(self):
        r'''Interprets ``back-cover.tex``.

        Returns none.
        '''
        self._interpret_file_ending_with('back-cover.tex')

    def interpret_front_cover(self):
        r'''Interprets ``front-cover.tex``.

        Returns none.
        '''
        self._interpret_file_ending_with('front-cover.tex')

    def interpret_music(self):
        r'''Interprets ``music.ly``.

        Returns none.
        '''
        self._call_lilypond_on_file_ending_with('music.ly')

    def interpret_open_front_cover(self):
        r'''Interprets ``front-cover.tex`` and then opens ``front-cover.pdf``.

        Returns none.
        '''
        self.interpret_front_cover()
        self.open_front_cover_pdf()
        
    def interpret_preface(self):
        r'''Interprets ``preface.tex``.

        Returns none.
        '''
        self._interpret_file_ending_with('preface.tex')

    def interpret_score(self):
        r'''Interprets ``score.tex``.

        Returns none.
        '''
        self._interpret_file_ending_with('score.tex')

    def push_score_pdf_to_distribution_directory(self):
        r'''Pushes ``score.pdf`` to distribution directory.

        Returns none.
        '''
        path = self._session.current_build_directory
        build_score_path = os.path.join(path, 'score.pdf')
        if not os.path.exists(build_score_path):
            message = 'does not exist: {!r}.'
            message = message.format(build_score_path)
            self._io_manager._display(message)
            return
        score_package_name = self._session.current_score_package_name
        score_package_name = score_package_name.replace('_', '-')
        distribution_file_name = '{}-score.pdf'.format(score_package_name)
        distribution_directory = self._session.current_distribution_directory
        distribution_score_path = os.path.join(
            distribution_directory,
            distribution_file_name,
            )
        shutil.copyfile(build_score_path, distribution_score_path)
        messages = []
        messages.append('Copied')
        message = ' FROM: {}'.format(build_score_path)
        messages.append(message)
        message = '   TO: {}'.format(distribution_score_path)
        messages.append(message)
        self._io_manager._display(messages)