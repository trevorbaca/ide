import abjad
import baca
import collections
import datetime
import importlib
import inspect
import io
import os
import pathlib
import platform
import re
import shutil
import subprocess
from .Command import Command
from .Configuration import Configuration
from .Interaction import Interaction
from .IO import IO
from .Menu import Menu
from .MenuSection import MenuSection
from .Path import Path
from .Response import Response


class AbjadIDE(abjad.AbjadObject):
    r'''Abjad IDE.

    ..  container:: example

        >>> ide.AbjadIDE()
        AbjadIDE()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_aliases',
        '_clipboard',
        '_commands',
        '_current_directory',
        '_example',
        '_io',
        '_navigation',
        '_navigations',
        '_previous_directory',
        '_redraw',
        '_test',
        )

    _black_and_white_metronome_mark_tags = {
        'activate': (
            baca.tags.EXPLICIT_METRONOME_MARK,
            baca.tags.REDUNDANT_METRONOME_MARK,
            ),
        'deactivate': (
            baca.tags.EXPLICIT_METRONOME_MARK_WITH_COLOR,
            baca.tags.REAPPLIED_METRONOME_MARK,
            baca.tags.REAPPLIED_METRONOME_MARK_WITH_COLOR,
            baca.tags.REDUNDANT_METRONOME_MARK_WITH_COLOR,
            ),
        }

    _color_clef_tags = (
        baca.tags.DEFAULT_CLEF_COLOR,
        baca.tags.DEFAULT_CLEF_REDRAW_COLOR,
        baca.tags.EXPLICIT_CLEF_COLOR,
        baca.tags.EXPLICIT_CLEF_REDRAW_COLOR,
        baca.tags.REAPPLIED_CLEF_COLOR,
        baca.tags.REAPPLIED_CLEF_REDRAW_COLOR,
        baca.tags.REDUNDANT_CLEF_COLOR,
        baca.tags.REDUNDANT_CLEF_REDRAW_COLOR,
        )

    _color_dynamic_tags = (
        baca.tags.EXPLICIT_DYNAMIC_COLOR,
        baca.tags.EXPLICIT_DYNAMIC_REDRAW_COLOR,
        baca.tags.REAPPLIED_DYNAMIC,
        baca.tags.REAPPLIED_DYNAMIC_COLOR,
        baca.tags.REAPPLIED_DYNAMIC_REDRAW_COLOR,
        baca.tags.REDUNDANT_DYNAMIC_COLOR,
        baca.tags.REDUNDANT_DYNAMIC_REDRAW_COLOR,
        )

    _color_instrument_tags = {
        'activate': (
            baca.tags.DEFAULT_INSTRUMENT_ALERT_WITH_COLOR,
            baca.tags.DEFAULT_INSTRUMENT_COLOR,
            baca.tags.REDRAWN_DEFAULT_INSTRUMENT_COLOR,
            baca.tags.EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR,
            baca.tags.EXPLICIT_INSTRUMENT_COLOR,
            baca.tags.REDRAWN_EXPLICIT_INSTRUMENT_COLOR,
            baca.tags.REAPPLIED_INSTRUMENT_ALERT_WITH_COLOR,
            baca.tags.REAPPLIED_INSTRUMENT_COLOR,
            baca.tags.REDRAWN_REAPPLIED_INSTRUMENT_COLOR,
            baca.tags.REDUNDANT_INSTRUMENT_ALERT_WITH_COLOR,
            baca.tags.REDUNDANT_INSTRUMENT_COLOR,
            baca.tags.REDRAWN_REDUNDANT_INSTRUMENT_COLOR,
            ),
        'deactivate': (
            ),
        }

    _color_margin_markup_tags = {
        'activate': (
            baca.tags.DEFAULT_MARGIN_MARKUP_ALERT_WITH_COLOR,
            baca.tags.DEFAULT_MARGIN_MARKUP_COLOR,
            baca.tags.REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR,
            baca.tags.EXPLICIT_MARGIN_MARKUP_ALERT_WITH_COLOR,
            baca.tags.EXPLICIT_MARGIN_MARKUP_COLOR,
            baca.tags.REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR,
            baca.tags.REAPPLIED_MARGIN_MARKUP_ALERT_WITH_COLOR,
            baca.tags.REAPPLIED_MARGIN_MARKUP_COLOR,
            baca.tags.REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR,
            baca.tags.REDUNDANT_MARGIN_MARKUP_ALERT_WITH_COLOR,
            baca.tags.REDUNDANT_MARGIN_MARKUP_COLOR,
            baca.tags.REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR,
            ),
        'deactivate': (
            ),
        }

    _color_metronome_mark_tags = {
        'activate': (
            baca.tags.EXPLICIT_METRONOME_MARK_WITH_COLOR,
            baca.tags.REAPPLIED_METRONOME_MARK_WITH_COLOR,
            baca.tags.REDUNDANT_METRONOME_MARK_WITH_COLOR,
            ),
        'deactivate': (
            baca.tags.EXPLICIT_METRONOME_MARK,
            baca.tags.REAPPLIED_METRONOME_MARK,
            baca.tags.REDUNDANT_METRONOME_MARK,
            ),
        }

    _color_staff_line_tags = (
        baca.tags.EXPLICIT_STAFF_LINES_COLOR,
        baca.tags.REAPPLIED_STAFF_LINES_COLOR,
        baca.tags.REDUNDANT_STAFF_LINES_COLOR,
        )

    _color_time_signature_tags = (
        baca.tags.EXPLICIT_TIME_SIGNATURE_COLOR,
        baca.tags.REAPPLIED_TIME_SIGNATURE_COLOR,
        baca.tags.REDUNDANT_TIME_SIGNATURE_COLOR,
        )

    configuration = Configuration()

    # lilypond.org/doc/v2.19/Documentation/notation/predefined-paper-sizes
    paper_size_to_paper_dimensions = {
        'a3': '297 x 420 mm',
        'a4': '210 x 297 mm',
        'arch a': '9 x 12 in',
        'arch b': '12 x 18 in',
        'arch c': '18 x 24 in',
        'arch d': '24 x 36 in',
        'arch e': '36 x 48 in',
        'legal': '8.5 x 14 in',
        'ledger': '17 x 11 in',
        'letter': '8.5 x 11 in',
        'tabloid': '11 x 17 in',
        }

    known_paper_sizes = list(paper_size_to_paper_dimensions.keys())

    ### INITIALIZER ###

    def __init__(self, example=None, test=None):
        self._aliases = dict(self.configuration.aliases)
        self._clipboard = []
        self._current_directory = None
        self._example = example
        self._navigation = None
        self._previous_directory = None
        self._redraw = None
        self._test = test
        self._io = IO()
        self._check_test_scores_directory(example or test)
        self._cache_commands()

    ### SPECIAL METHODS ###

    def __call__(self, string=None):
        r'''Calls IDE on `string`.

        Returns none.
        '''
        if self.test and not string.endswith('q'):
            raise Exception(f"Test input must end with 'q': {string!r}.")
        self.__init__(example=self.example, test=self.test)
        self.io.pending_input(string)
        scores = self._get_scores_directory()
        self._manage_directory(scores)
        self.io.transcript.trim()
        last_line = self.io.transcript.lines[-1]
        assert last_line == '', repr(last_line)
        abjad.IOManager.clear_terminal()

    ### PRIVATE METHODS ###

    def _activate_tag(self, directory, tag, name=None):
        if directory.is_build() or directory.is__segments():
            count = self._activate_tag_in_build_lys(
                directory,
                tag,
                name=name,
                )
        elif directory.is_segment():
            count = self._activate_tag_in_segment_ly(
                directory,
                tag,
                name=name,
                )
        elif directory.is_segments():
            count = 0
            for segment in directory.list_paths():
                count += self._activate_tag_in_segment_ly(
                    segment,
                    tag,
                    name=name,
                    )
        elif directory.is_file():
            count = self._activate_tag_in_file(directory, tag, name=name)
        else:
            raise ValueError(directory)
        if not count:
            name = name or tag
            self.io.display(f'no {name} tags to activate ...')

    def _activate_tag_in_build_lys(self, directory, tag, name=None):
        assert directory.is_score_package_path()
        if not directory._segments.is_dir():
            self.io.display('no _segments directory found ...')
            return
        names = []
        for path in directory._segments.list_paths():
            if not path.name.startswith('segment'):
                continue
            names.append(path.name)
        first_segment_name = 'segment-_.ly'
        if first_segment_name in names:
            names.remove(first_segment_name)
            names.insert(0, first_segment_name)
        lys = [directory._segments(_) for _ in names]
        total = 0
        for ly in lys:
            text, count = ly.activate_tag(tag)
            if count:
                messages = self._message_activate(ly, tag, count, name=name)
                self.io.display(messages)
            ly.write_text(text)
            total += count
        return total

    def _activate_tag_in_file(self, path, tag, name=None):
        if not path.is_file():
            self.io.display(f'missing {path.trim()} ...')
            return
        text, count = path.activate_tag(tag)
        if count:
            messages = self._message_activate(path, tag, count, name=name)
            self.io.display(messages)
        path.write_text(text)
        return count

    def _activate_tag_in_segment_ly(self, directory, tag, name=None):
        ly = directory('illustration.ly')
        if not ly.is_file():
            self.io.display(f'missing {ly.trim()} ...')
            return
        text, count = ly.activate_tag(tag)
        if count:
            messages = self._message_activate(ly, tag, count, name=name)
            self.io.display(messages)
        ly.write_text(text)
        return count

    def _cache_commands(self):
        commands = {}
        for name in dir(self):
            if name.startswith('_'):
                continue
            try:
                command = getattr(self, name)
            except AttributeError:
                command = None
            if not inspect.ismethod(command):
                continue
            if not hasattr(command, 'command_name'):
                continue
            commands[command.command_name] = command
        self._commands = commands

    def _check_test_scores_directory(self, check=False):
        if not check:
            return
        directory = self.configuration.test_scores_directory
        names = [_.name for _ in directory.iterdir()]
        if 'red_score' not in names:
            message = f'Empty test scores directory {directory} ...'
            raise Exception(message)

    def _collect_segment_lys(self, directory):
        paths = sorted(directory.segments.iterdir())
        names = [_.name for _ in paths]
        if '_' in names:
            names.remove('_')
            names.insert(0, '_')
        sources, targets = [], []
        for name in names:
            source = directory.segments(name, 'illustration.ly')
            if not source.is_file():
                continue
            if name == '_':
                name = 'segment-_.ly'
            else:
                name = 'segment-' + name.replace('_', '-') + '.ly'
            target = directory._segments(name)
            sources.append(source)
            targets.append(target)
        if not directory.builds.is_dir():
            directory.builds.mkdir()
        return zip(sources, targets)

    def _copy_boilerplate(
        self,
        directory,
        source_name,
        target_name=None,
        values=None,
        ):
        target_name = target_name or source_name
        target = directory / target_name
        if target.exists():
            self.io.display(f'removing {target.trim()} ...')
        self.io.display(f'writing {target.trim()} ...')
        values = values or {}
        boilerplate = Path(abjad.abjad_configuration.boilerplate_directory)
        source = boilerplate / source_name
        target_name = target_name or source_name
        target = directory / target_name
        shutil.copyfile(str(source), str(target))
        if not values:
            return
        template = target.read_text()
        template = template.format(**values)
        target.write_text(template)

    def _deactivate_bar_line_adjustment_after_noneol_fermata(self, directory):
        # activate all tags:
        tag = baca.tags.BAR_LINE_ADJUSTMENT_AFTER_EOL_FERMATA
        self._activate_tag(directory, tag)
        # then deactivate non-EOL tags:
        bol_measure_numbers = directory.get_metadatum('bol_measure_numbers')
        if not bol_measure_numbers:
            return
        eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
        # don't need to worry about last measure in score
        # because segment-maker preserves barline after score-final fermata:
        eol_measure_numbers = [f'MEASURE_{_}' for _ in eol_measure_numbers]
        match = baca.Match(
            match_all=[baca.tags.BAR_LINE_ADJUSTMENT_AFTER_EOL_FERMATA],
            forbid_any=eol_measure_numbers,
            )
        name = baca.tags.BAR_LINE_ADJUSTMENT_AFTER_EOL_FERMATA
        self._deactivate_tag(directory, match, name=name)

    def _deactivate_shifted_clef_at_bol(self, directory):
        # activate all shifted clefs (to undo segment deactivations):
        self._activate_tag(directory, baca.tags.SHIFTED_CLEF)
        # then deactivate shifted clefs at BOL:
        bol_measure_numbers = directory.get_metadatum('bol_measure_numbers')
        if not bol_measure_numbers:
            return
        bol_measure_numbers = [f'MEASURE_{_}' for _ in bol_measure_numbers]
        match = baca.Match(
            match_all=[baca.tags.SHIFTED_CLEF],
            match_any=bol_measure_numbers,
            )
        self._deactivate_tag(directory, match, name=baca.tags.SHIFTED_CLEF)

    def _deactivate_tag(self, directory, tag, name=None):
        if directory.is_build() or directory.is__segments():
            count = self._deactivate_tag_in_build_lys(
                directory,
                tag,
                name=name,
                )
        elif directory.is_segment():
            count = self._deactivate_tag_in_segment_ly(
                directory,
                tag,
                name=name,
                )
        elif directory.is_segments():
            count = 0
            for segment in directory.list_paths():
                count += self._deactivate_tag_in_segment_ly(
                    segment,
                    tag,
                    name=name,
                    )
        elif directory.is_file():
            count = self._deactivate_tag_in_file( directory, tag, name=name)
        else:
            raise ValueError(directory)
        if not count:
            name = name or tag
            self.io.display(f'no {name} tags to deactivate ...')

    def _deactivate_tag_in_build_lys(self, directory, tag, name=None):
        assert directory.is_score_package_path()
        if not directory._segments.is_dir():
            self.io.display('no _segments directory found ...')
            return
        names = []
        for path in directory._segments.list_paths():
            if not path.name.startswith('segment'):
                continue
            names.append(path.name)
        first_segment_name = 'segment-_.ly'
        if first_segment_name in names:
            names.remove(first_segment_name)
            names.insert(0, first_segment_name)
        lys = [directory._segments(_) for _ in names]
        total = 0
        for ly in lys:
            text, count = ly.deactivate_tag(tag)
            if count:
                messages = self._message_deactivate(ly, tag, count, name=name)
                self.io.display(messages)
            ly.write_text(text)
            total += count
        return total

    def _deactivate_tag_in_file(self, path, tag, name=None):
        if not path.is_file():
            self.io.display(f'missing {path.trim()} ...')
            return
        text, count = path.deactivate_tag(tag)
        if count:
            messages = self._message_deactivate(path, tag, count, name=name)
            self.io.display(messages)
        path.write_text(text)
        return count


    def _deactivate_tag_in_segment_ly(self, directory, tag, name=None):
        ly = directory('illustration.ly')
        if not ly.is_file():
            self.io.display(f'missing {ly.trim()} ...')
            return
        text, count = ly.deactivate_tag(tag)
        if count:
            messages = self._message_deactivate(ly, tag, count, name=name)
            self.io.display(messages)
        ly.write_text(text)
        return count

    @staticmethod
    def _filter_files(files, strings, pattern):
        if isinstance(pattern, str):
            indices = abjad.String.match_strings(strings, pattern)
            files = abjad.Sequence(files).retain(indices)
        return files

    def _generate_back_cover(self, path, price=None):
        assert path.build.exists(), repr(path)
        assert path.name.endswith('back-cover.tex')
        directory = path.build
        values = {}
        string = 'catalog_number'
        catalog_number = directory.contents.get_metadatum(string, r'\null')
        if catalog_number:
            suffix = directory.get_metadatum('catalog_number_suffix')
            if suffix:
                catalog_number = f'{catalog_number} / {suffix}'
        values['catalog_number'] = catalog_number
        composer_website = abjad.abjad_configuration.composer_website or ''
        if self.test or self.example:
            composer_website = 'www.composer-website.com'
        values['composer_website'] = composer_website
        if price is None:
            price = directory.get_metadatum('price', r'\null')
            if '$' in price and r'\$' not in price:
                price = price.replace('$', r'\$')
        values['price'] = price
        paper_size = directory.get_metadatum('paper_size', 'letter')
        if paper_size not in self.known_paper_sizes:
            self.io.display(f'unknown paper size {paper_size} ...')
            return
        orientation = directory.get_metadatum('orientation')
        dimensions = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = dimensions
        paper_size = f'{{{width}{unit}, {height}{unit}}}'
        values['paper_size'] = paper_size
        target_name = path.name
        self._copy_boilerplate(
            directory,
            'back-cover.tex',
            target_name=target_name,
            values=values,
            )

    def _generate_document(self, directory, name='score.tex', prefix=None):
        values = {}
        paper_size = directory.get_metadatum('paper_size', 'letter')
        orientation = directory.get_metadatum('orientation')
        paper_size = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f'{{{width}{unit}, {height}{unit}}}'
        values['paper_size'] = paper_size
        target_name = name
        if prefix is not None:
            target_name = f'{prefix}-{target_name}'
        self._copy_boilerplate(
            directory,
            'score.tex',
            target_name=target_name,
            values=values,
            )

    def _generate_front_cover(self, path, forces_tagline=None):
        assert path.build.exists(), repr(path)
        directory = path.build
        name = 'front-cover.tex'
        local_template = directory._assets(name)
        if local_template.is_file():
            self.io.display(f'removing {path.trim()} ...')
            path.remove()
            self.io.display(f'copying {local_template.trim()} ...')
            self.io.display(f'writing {path.trim()} ...')
            shutil.copyfile(str(local_template), str(path))
            if forces_tagline is not None:
                text = path.read_text()
                if 'FORCES_TAGLINE' in text:
                    text = text.replace('FORCES_TAGLINE', forces_tagline)
                path.write_text(text)
            return
        values = {}
        score_title = directory.contents.get_title(year=False)
        score_title = score_title.upper()
        values['score_title'] = score_title
        if not forces_tagline:
            string = 'forces_tagline'
            forces_tagline = directory.contents.get_metadatum(string, '')
        if forces_tagline:
            forces_tagline = forces_tagline.replace('\\', '')
        values['forces_tagline'] = forces_tagline
        year = directory.contents.get_metadatum('year', '')
        values['year'] = str(year)
        composer = abjad.abjad_configuration.composer_uppercase_name
        if (self.test or self.example):
            composer = 'COMPOSER'
        values['composer'] = str(composer)
        paper_size = directory.get_metadatum('paper_size', 'letter')
        orientation = directory.get_metadatum('orientation')
        paper_size = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f'{{{width}{unit}, {height}{unit}}}'
        values['paper_size'] = paper_size
        target_name = None
        target_name = path
        self._copy_boilerplate(
            directory,
            name,
            target_name=target_name,
            values=values,
            )

    def _generate_music(
        self,
        path,
        forces_tagline=None,
        keep_with_tag=None,
        silent=None,
        ):
        assert path.build.exists(), repr(path)
        target = path
        target_name = path.name
        directory = path.build
        if target.exists():
            self.io.display(f'removing {target.trim()} ...')
            target.remove()
        paths = directory.segments.list_paths()
        if not silent:
            if paths:
                view = directory.segments.get_metadatum('view')
                if bool(view):
                    self.io.display(f'examining segments in view order ...')
                else:
                    self.io.display('examining segments alphabetically ...')
            else:
                self.io.display('no segments found ...')
            for path in paths:
                self.io.display(f'examining {path.trim()} ...')
        names = []
        for path in paths:
            name = path.stem
            if path.stem != '_':
                name = name.replace('_', '-')
            names.append(name)
        self._copy_boilerplate(directory, 'music.ly', target_name=target_name)
        lines = []
        segment_include_statements = ''
        for i, name in enumerate(names):
            name = 'segment-' + name + '.ly'
            path = directory._segments(name)
            if path.is_file():
                line = rf'\include "_segments/{name}"'
            else:
                line = rf'%\include "_segments/{name}"'
            if 0 < i:
                line = 8 * ' ' + line
            lines.append(line)
        if lines:
            new = '\n'.join(lines)
            segment_include_statements = new
        language_token = abjad.LilyPondLanguageToken()
        lilypond_language_directive = format(language_token)
        version_token = abjad.LilyPondVersionToken()
        lilypond_version_directive = format(version_token)
        annotated_title = directory.contents.get_title(year=True)
        if annotated_title:
            score_title = annotated_title
        else:
            score_title = directory.contents.get_title(year=False)
        if forces_tagline is None:
            string = 'forces_tagline'
            forces_tagline = directory.contents.get_metadatum(string, '')
        if forces_tagline:
            forces_tagline = forces_tagline.replace('\\', '')
        if keep_with_tag:
            keep_with_tag_command = rf'\keepWithTag {keep_with_tag} '
        else:
            keep_with_tag_command = ''
        template = target.read_text()
        template = template.format(
            forces_tagline=forces_tagline,
            keep_with_tag_command=keep_with_tag_command,
            lilypond_language_directive=lilypond_language_directive,
            lilypond_version_directive=lilypond_version_directive,
            score_title=score_title,
            segment_include_statements=segment_include_statements,
            )
        target.write_text(template)

    def _generate_part(self, path, dashed_part_name):
        assert path.build.exists(), repr(path)
        assert path.build.is_parts(), repr(path)
        name = 'part.tex'
        directory = path.build
        values = {}
        values['dashed_part_name'] = dashed_part_name
        paper_size = directory.get_metadatum('paper_size', 'letter')
        orientation = directory.get_metadatum('orientation')
        paper_size = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f'{{{width}{unit}, {height}{unit}}}'
        values['paper_size'] = paper_size
        target_name = path.name
        self._copy_boilerplate(
            directory,
            name,
            target_name=target_name,
            values=values,
            )

    def _generate_preface(self, path):
        assert path.build.exists(), repr(path)
        directory = path.build
        name = 'preface.tex'
        local_template = directory._assets(name)
        if local_template.is_file():
            self.io.display(f'removing {path.trim()} ...')
            path.remove()
            self.io.display(f'copying {local_template.trim()} ...')
            self.io.display(f'writing {path.trim()} ...')
            shutil.copyfile(str(local_template), str(path))
            return
        values = {}
        paper_size = directory.get_metadatum('paper_size', 'letter')
        orientation = directory.get_metadatum('orientation')
        paper_size = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f'{{{width}{unit}, {height}{unit}}}'
        values['paper_size'] = paper_size
        target_name = path.name
        self._copy_boilerplate(
            directory,
            name,
            target_name=target_name,
            values=values,
            )

    def _get_dimensions(self):
        dimensions = None
        if self.test is True:
            dimensions = False
        if isinstance(self.test, str) and self.test.startswith('dimensions'):
            dimensions = eval(self.test.strip('dimensions='))
        return dimensions

    def _get_persistent_indicator_color_expression_tags(self, directory):
        tags = self._color_clef_tags
        if directory.is_build():
            tags += (baca.tags.REAPPLIED_CLEF,)
        tags += self._color_dynamic_tags
        tags += self._color_instrument_tags['activate']
        tags += self._color_margin_markup_tags['activate']
        tags += self._black_and_white_metronome_mark_tags['deactivate']
        tags += self._color_staff_line_tags
        tags += self._color_time_signature_tags
        return tags

    def _get_persistent_indicator_color_suppression_tags(self, directory):
        tags = self._color_instrument_tags['deactivate']
        if directory.is_build():
            tags += (baca.tags.REAPPLIED_INSTRUMENT,)
        tags += self._black_and_white_metronome_mark_tags['activate']
        return tags

    def _get_score_names(self):
        scores = self._get_scores_directory()
        names = [_.name for _ in scores.list_paths()]
        return names

    def _get_scores_directory(self):
        if (self.test or self.example):
            return self.configuration.test_scores_directory
        return self.configuration.composer_scores_directory

    def _handle_address(self, directory, response):
        assert response.prefix, repr(response)
        if response.prefix == '@':
            self.smart_edit(directory, response.pattern, response.payload)
        elif response.prefix == '@@':
            self.edit_all(directory, response.pattern)
        elif response.prefix == '%':
            self.go_to_directory(directory, response.pattern, response.payload)
        elif response.prefix == '%%':
            self.go_to_directory(directory, response.string[1:])
        elif response.prefix == '^':
            self.smart_doctest(directory, response.pattern, response.payload)
        elif response.prefix == '^^':
            self.doctest_all(directory, response.pattern)
        elif response.prefix == '+':
            self.smart_pytest(directory, response.pattern, response.payload)
        elif response.prefix == '++':
            self.pytest_all(directory, response.pattern)
        elif response.prefix == '*':
            self.smart_pdf(directory, response.pattern, response.payload)
        elif response.prefix == '**':
            self.open_all_pdfs(directory, response.pattern)
        else:
            raise ValueEror(response.prefix)

    def _interpret_file(self, path):
        path = Path(path)
        if not path.exists():
            message = f'missing {path} ...'
            self.display(message)
            return False
        if path.suffix == '.py':
            command = f'python {path}'
        elif path.suffix == '.ly':
            command = f'lilypond -dno-point-and-click {path}'
        else:
            message = f'can not interpret {path}.'
            raise Exception(message)
        directory = path.parent
        directory = abjad.TemporaryDirectoryChange(directory)
        string_buffer = io.StringIO()
        with directory, string_buffer:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                )
            for line in process.stdout:
                line = line.decode('utf-8')
                print(line, end='')
                string_buffer.write(line)
            process.wait()
            stdout_lines = string_buffer.getvalue().splitlines()
            stderr_lines = abjad.IOManager._read_from_pipe(process.stderr)
            stderr_lines = stderr_lines.splitlines()
        exit_code = process.returncode
        return stdout_lines, stderr_lines, exit_code

    def _interpret_tex_file(self, tex):
        if not tex.is_file():
            self.io.display(f'can not find {tex.trim()} ...')
            return
        pdf = tex.with_suffix('.pdf')
        if pdf.exists():
            self.io.display(f'removing {pdf.trim()} ...')
            pdf.remove()
        self.io.display(f'interpreting {tex.trim()} ...')
        if not tex.is_file():
            return
        executables = abjad.IOManager.find_executable('xelatex')
        executables = [Path(_) for _ in executables]
        if not executables:
            executable_name = 'pdflatex'
            fancy_executable_name = 'LaTeX'
        else:
            executable_name = 'xelatex'
            fancy_executable_name = 'XeTeX'
        pdf_path = tex.parent / (str(tex.stem) + '.pdf')
        log = self.configuration.latex_log_file_path
        command = f'date > {log};'
        command += f' {executable_name} -halt-on-error'
        command += f' --jobname={tex.stem}'
        command += f' -output-directory={tex.parent} {tex}'
        command += f' >> {log} 2>&1'
        command_called_twice = f'{command}; {command}'
        with self.change(tex.parent):
            abjad.IOManager.spawn_subprocess(command_called_twice)
            for path in sorted(tex.parent.glob('*.aux')):
                path.remove()
            for path in sorted(tex.parent.glob('*.log')):
                path.remove()
        if pdf.is_file():
            self.io.display(f'writing {pdf.trim()} ...')
        else:
            self.io.display('ERROR IN LATEX LOG FILE ...')
            log_file = self.configuration.latex_log_file_path
            with log_file.open() as file_pointer:
                lines = [_.strip('\n') for _ in file_pointer.readlines()]
            self.io.display(lines)

    def _interpret_tex_files_ending_with(self, directory, name):
        paths = directory.get_files_ending_with(name)
        if not paths:
            self.io.display(f'no files ending in *{name} ...')
            return
        self.io.display('will interpret ...')
        for path in paths:
            self.io.display(path.trim(), raw=True)
        self.io.display('')
        ok = self.io.get('ok?')
        if ok and self.is_navigation(ok):
            return
        if ok != 'y':
            return
        for source in paths:
            target = source.with_suffix('.pdf')
            self._interpret_tex_file(source)

    def _make_build_directory(self, builds):
        name = self.io.get('build name')
        if self.is_navigation(name):
            return
        name = builds.coerce(name)
        build = builds / name
        if build.exists():
            self.io.display(f'existing {build.trim()} ...')
            return
        paper_size = self.io.get('paper size')
        if paper_size and self.is_navigation(paper_size):
            return
        paper_size = paper_size or 'letter'
        orientation = 'portrait'
        if paper_size.endswith(' landscape'):
            orientation = 'landscape'
            length = len(' landscape')
            paper_size = paper_size[:-length]
        elif paper_size.endswith(' portrait'):
            length = len(' portrait')
            paper_size = paper_size[:-length]
        if paper_size not in self.known_paper_sizes:
            self.io.display(f'unknown paper size {paper_size!r} ...')
            self.io.display('choose from ...')
            for paper_size in self.known_paper_sizes:
                self.io.display(f'    {paper_size}')
            return
        price = self.io.get('price')
        if price and self.is_navigation(price):
            return
        suffix = self.io.get('catalog number suffix')
        if suffix and self.is_navigation(suffix):
            return
        names = (
            'back-cover.tex',
            'front-cover.tex',
            'music.ly',
            'preface.tex',
            'score.tex',
            'stylesheet.ily',
            )
        paths = [build / _ for _ in names]
        self.io.display('making ...')
        self.io.display(f'    {build.trim()}')
        for path in paths:
            self.io.display(f'    {path.trim()}')
        response = self.io.get('ok?')
        if self.is_navigation(response):
            return
        if response != 'y':
            return
        assert not build.exists()
        build.mkdir()
        if bool(paper_size):
            build.add_metadatum('paper_size', paper_size)
        if not orientation == 'portrait':
            build.add_metadatum('orientation', orientation)
        if bool(price):
            build.add_metadatum('price', price)
        if bool(suffix):
            build.add_metadatum('catalog_number_suffix', suffix)
        self.generate_back_cover(build)
        self.io.display('')
        self.generate_front_cover(build)
        self.io.display('')
        self._copy_boilerplate(build, 'layout.py')
        self.io.display('')
        self.collect_segment_lys(build)
        self.io.display('')
        self.generate_music(build)
        self.io.display('')
        self.generate_preface(build)
        self.io.display('')
        self.generate_score(build)
        self.io.display('')
        self.generate_stylesheet(build)

    def _make_command_sections(self, directory):
        commands = []
        for command in self.commands.values():
            blacklist = command.score_package_path_blacklist
            if directory.is_scores() and command.scores_directory:
                commands.append(command)
            elif (directory.is_external() and
                not directory.is_scores() and
                command.external_directories):
                commands.append(command)
            elif (directory.is_score_package_path() and
                directory.is_prototype(command.score_package_paths) and
                not directory.is_prototype(blacklist)):
                commands.append(command)
        entries_by_section = {}
        navigations = {}
        navigation_sections = ('go', 'package')
        for command in commands:
            if command.menu_section not in entries_by_section:
                entries_by_section[command.menu_section] = []
            entries = entries_by_section[command.menu_section]
            display = f'{command.description} ({command.command_name})'
            entry = (display, command.command_name)
            entries.append(entry)
            if command.menu_section in navigation_sections:
                name = command.command_name
                navigations[name] = command
        del(navigations['%'])
        self._navigations = navigations
        sections = []
        for name in Command.known_sections:
            if name not in entries_by_section:
                continue
            entries = entries_by_section[name]
            section = MenuSection(
                command=name,
                entries=entries,
                )
            sections.append(section)
        return sections

    def _make_file(self, directory):
        name = self.io.get('file name')
        if self.is_navigation(name):
            return
        if directory.is_score_package_path():
            name = directory.coerce(name)
            predicate = directory.get_name_predicate()
            if predicate and not predicate(abjad.String(name)):
                self.io.display(f'invalid file name {name!r} ...')
                return
        elif directory.is_library():
            suffix = Path(name).suffix
            if suffix and suffix != '.py':
                self.io.display(f'invalid file name {name!r} ...')
            stem = abjad.String(Path(name).stem)
            if stem.islower():
                stem = stem.to_snake_case()
            else:
                stem = stem.to_upper_camel_case()
            suffix = suffix or '.py'
            name = stem + suffix
        target = directory / name
        #boilerplate = self.configuration.boilerplate_directory
        if target.exists():
            self.io.display(f'existing {target.trim()} ...')
            return
        else:
            self.io.display(f'writing {target.trim()} ...')
            response = self.io.get('ok?')
            if self.is_navigation(response):
                return
            if response != 'y':
                return
        if directory.is_tools():
            if abjad.String(name).is_classfile_name():
                self._copy_boilerplate(directory, 'Maker.py', target.name)
                template = target.read_text()
                template = template.format(class_name=target.stem)
                target.write_text(template)
            else:
                self._copy_boilerplate(directory, 'function.py', target.name)
                template = target.read_text()
                template = template.format(function_name=target.stem)
                target.write_text(template)
        else:
            if not target.parent.exists():
                target.parent.mkdir()
            target.write_text('')

    def _make_material_ly(self, directory):
        assert directory.is_material()
        definition = directory('definition.py')
        if not definition.is_file():
            self.io.display(f'can not find {definition.trim()} ...')
            return
        ly = directory('illustration.ly')
        if ly.exists():
            self.io.display(f'removing {ly.trim()} ...')
        maker = directory('__make_material_ly__.py')
        maker.remove()
        with self.cleanup([maker]):
            self.io.display(f'writing {maker.trim()} ...')
            self._copy_boilerplate(directory, maker.name)
            self.io.display(f'interpreting {maker.trim()} ...')
            result = self._interpret_file(str(maker))
            if ly.is_file():
                self.io.display(f'writing {ly.trim()} ...')
            self.io.display(f'removing {maker.trim()} ...')
            stdout_lines, stderr_lines, exit_code = result
            if exit_code:
                self.io.display(stderr_lines, raw=True)

    def _make_material_pdf(self, directory, open_after=True):
        assert directory.is_material()
        definition = directory('definition.py')
        if not definition.is_file():
            self.io.display(f'missing {definition.trim()} ...')
            return 0 
        name = directory.name.replace('_', ' ')
        self.io.display(f'making {name} PDF ...')
        ly = directory('illustration.ly')
        if ly.exists():
            self.io.display(f'removing {ly.trim()} ...')
            ly.remove()
        pdf = directory('illustration.pdf')
        if pdf.exists():
            self.io.display(f'removing {pdf.trim()} ...')
            pdf.remove()
        maker = directory('__make_material_pdf__.py')
        maker.remove()
        with self.cleanup([maker]):
            self.io.display(f'writing {maker.trim()} ...')
            self._copy_boilerplate(directory, maker.name)
            self.io.display(f'interpreting {maker.trim()} ...')
            result = self._interpret_file(maker)
            if ly.is_file():
                self.io.display(f'writing {ly.trim()} ...')
            if pdf.is_file():
                self.io.display(f'writing {pdf.trim()} ...')
            self.io.display(f'removing {maker.trim()} ...')
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self.io.display(stderr_lines, raw=True)
        if pdf.is_file() and open_after:
            self._open_files([pdf])
        return exit_code

    def _make_package(self, directory):
        asset_type = directory.get_asset_type()
        name = self.io.get(f'enter {asset_type} name')
        if self.is_navigation(name):
            return
        name = directory.coerce(name)
        path = directory(name)
        if path.exists():
            self.io.display(f'existing {path.trim()} ...')
            return
        self.io.display(f'making {path.trim()} ...')
        path.mkdir()
        target = path('__init__.py')
        self.io.display(f'writing {target.trim()} ...')
        target.write_text('')
        if path.is_segment():
            target = path('__metadata__.py')
            self.io.display(f'writing {target.trim()} ...')
            text = 'import abjad\n\n\nmetadata = abjad.TypedOrderedDict()'
            target.write_text(text)
        target = path('definition.py')
        self.io.display(f'writing {target.trim()} ...')
        target.write_text('')
        paths = path.parent.list_paths()
        if path not in paths:
            view = path.parent.get_metadatum('view')
            if view is not None:
                path.parent.add_metadatum('_view', view) 
                path.parent.remove_metadatum('view')

    def _make_score_package(self):
        scores = self._get_scores_directory()
        wrapper = scores._find_empty_wrapper()
        if wrapper is not None:
            self.io.display(f'found {wrapper.trim()}.')
            response = self.io.get(f'populate {wrapper.trim()}?')
            if self.is_navigation(response):
                return
            if response != 'y':
                return
        title = self.io.get('enter title')
        if self.is_navigation(title):
            return
        if wrapper is None:
            name = scores.coerce(title)
            wrapper = scores / name
            if wrapper.exists():
                self.io.display(f'existing {wrapper.trim()} ...')
                return
        self.io.display(f'making {wrapper.trim()} ...')
        year = datetime.date.today().year
        abjad.IOManager._make_score_package(
            score_package_path=str(wrapper),
            composer_email=abjad.abjad_configuration.composer_email,
            composer_full_name=abjad.abjad_configuration.composer_full_name,
            composer_github_username=abjad.abjad_configuration.composer_github_username,
            composer_last_name=abjad.abjad_configuration.composer_last_name,
            composer_library=abjad.abjad_configuration.composer_library,
            score_title=title,
            year=year,
            )
        for path in wrapper.builds.iterdir():
            if path.name == '.gitignore':
                continue
            path.remove()
        view = scores.get_metadatum('view', None)
        if view is not None:
            scores.add_metadatum('_view', view)
        scores.remove_metadatum('view')

    def _make_segment_ly(self, directory):
        assert directory.is_segment()
        definition = directory('definition.py')
        if not definition.is_file():
            self.io.display(f'can not find {definition.trim()} ...')
            return
        ly = directory('illustration.ly')
        if ly.exists():
            self.io.display(f'removing {ly.trim()} ...')
        maker = directory('__make_segment_ly__.py')
        maker.remove()
        with self.cleanup([maker]):
            self.io.display(f'writing {maker.trim()} ...')
            self._copy_boilerplate(directory, maker.name)
            previous_segment = directory.get_previous_package()
            if previous_segment is None:
                statement = 'previous_metadata = None'
            else:
                statement = 'from {}.segments.{}.__metadata__'
                statement += ' import metadata as previous_metadata'
                statement = statement.format(
                    directory.contents.name,
                    previous_segment.name,
                    )
            template = maker.read_text()
            template = template.format(
                previous_segment_metadata_import_statement=statement
                )
            maker.write_text(template)
            self.io.display(f'interpreting {maker.trim()} ...')
            result = self._interpret_file(maker)
            if ly.is_file():
                self.io.display(f'writing {ly.trim()} ...')
            self.io.display(f'removing {maker.trim()} ...')
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self.io.display(stderr_lines, raw=True)

    def _make_segment_midi(self, directory, open_after=True):
        assert directory.is_segment()
        definition = directory('definition.py')
        if not definition.is_file():
            self.io.display(f'can not find {definition.trim()} ...')
            return -1
        self.io.display('making MIDI ...')
        ly = directory('midi.ly')
        if ly.exists():
            self.io.display(f'removing {ly.trim()} ...')
            ly.remove()
        midi = directory('segment.midi')
        if midi.exists():
            self.io.display(f'removing {midi.trim()} ...')
            midi.remove()
        maker = directory('__make_segment_midi__.py')
        maker.remove()
        with self.cleanup([maker]):
            self.io.display(f'writing {maker.trim()} ...')
            self._copy_boilerplate(directory, maker.name)
            previous_segment = directory.get_previous_package()
            if previous_segment is None:
                statement = 'previous_metadata = None'
            else:
                statement = 'from {}.segments.{}.__metadata__'
                statement += ' import metadata as previous_metadata'
                statement = statement.format(
                    directory.contents.name,
                    previous_segment.name,
                    )
            template = maker.read_text()
            template = template.format(
                previous_segment_metadata_import_statement=statement
                )
            maker.write_text(template)
            self.io.display(f'interpreting {maker.trim()} ...')
            result = self._interpret_file(maker)
            self.io.display(f'removing {maker.trim()} ...')
            if midi.is_file():
                self.io.display(f'writing {midi.trim()} ...')
            self.io.display(f'removing {maker.trim()} ...')
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self.io.display(stderr_lines, raw=True)
            return exit_code
        log = abjad.abjad_configuration.lilypond_log_file_path
        log = Path(log)
        with log.open() as file_pointer:
            lines = file_pointer.readlines()
        for line in lines:
            if ('fatal' in line or
                ('error' in line and 'programming error' not in line) or
                'failed' in line):
                self.io.display('ERROR IN LILYPOND LOG FILE ...')
                break
        if midi.is_file() and open_after:
            self._open_files([midi])
        return 0

    def _make_segment_pdf(self, directory, open_after=True):
        assert directory.is_segment()
        self.make_layout_ly(directory)
        definition = directory('definition.py')
        if not definition.is_file():
            self.io.display(f'can not find {definition.trim()} ...')
            return -1
        self.io.display(f'making segment {directory.name} PDF ...')
        ly = directory('illustration.ly')
        if ly.exists():
            self.io.display(f'removing {ly.trim()} ...')
            ly.remove()
        pdf = directory('illustration.pdf')
        if pdf.exists():
            self.io.display(f'removing {pdf.trim()} ...')
            pdf.remove()
        maker = directory('__make_segment_pdf__.py')
        maker.remove()
        with self.cleanup([maker]):
            self._copy_boilerplate(directory, maker.name)
            previous_segment = directory.get_previous_package()
            if previous_segment is None:
                statement = 'previous_metadata = None'
            else:
                statement = 'from {}.segments.{}.__metadata__'
                statement += ' import metadata as previous_metadata'
                statement = statement.format(
                    directory.contents.name,
                    previous_segment.name,
                    )
            template = maker.read_text()
            completed_template = template.format(
                previous_segment_metadata_import_statement=statement
                )
            maker.write_text(completed_template)
            self.io.display(f'interpreting {maker.trim()} ...')
            result = self._interpret_file(maker)
            if ly.is_file():
                self.io.display(f'writing {ly.trim()} ...')
            if pdf.is_file():
                self.io.display(f'writing {pdf.trim()} ...')
            self.io.display(f'removing {maker.trim()} ...')
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self.io.display(stderr_lines, raw=True)
            return exit_code
        log = abjad.abjad_configuration.lilypond_log_file_path
        log = Path(log)
        with log.open() as file_pointer:
            lines = file_pointer.readlines()
        for line in lines:
            if ('fatal' in line or
                ('error' in line and 'programming error' not in line) or
                'failed' in line):
                self.io.display('ERROR IN LILYPOND LOG FILE ...')
                break
        if pdf.is_file() and open_after:
            self._open_files([pdf])
        return 0

    def _make_selector(
        self,
        aliases=None,
        navigations=None,
        force_single_column=False,
        header=None,
        items=None,
        prompt=None,
        ):
        entries = []
        for item in items:
            if isinstance(item, tuple):
                assert len(item) == 2, repr(item)
                entry = item
            elif isinstance(item, str):
                entry = (item, item)
            else:
                raise TypeError(item)
            entries.append(entry)
        if not entries:
            sections = []
        else:
            section = MenuSection(
                entries=entries,
                force_single_column=force_single_column,
                )
            sections = [section]
        menu = Menu(
            aliases=aliases,
            navigations=navigations,
            getter=True,
            header=header,
            io=self.io,
            prompt=prompt,
            sections=sections,
            )
        return menu

    def _manage_directory(self, directory, redraw=True):
        if not directory.exists():
            self.io.display(f'missing {directory.trim()} ...')
            return
        assert directory.is_dir(), repr(directory)
        if not self.current_directory == directory:
            self._previous_directory = self.current_directory
            self._current_directory = directory
        sections = self._make_command_sections(directory)
        menu = Menu.from_directory(
            directory,
            aliases=self.aliases,
            io=self.io,
            navigations=self.navigations,
            sections=sections,
            )
        dimensions = self._get_dimensions()
        response = menu(dimensions=dimensions, redraw=redraw)
        if self.is_navigation(response.string):
            pass
        elif response.is_address():
            self._handle_address(directory, response)
        elif response.is_command(self.commands):
            command = self.commands[response.payload]
            try:
                command(self.current_directory)
            except TypeError:
                command()
        elif response.is_path():
            path = response.get_path()
            if path.is_file():
                self._open_files([path])
            elif path.is_dir():
                if path.is_wrapper():
                    path = path.contents
                self._manage_directory(path)
            else:
                self.io.display(f'missing {path.trim()} ...')
        elif response.is_shell():
            self.call_shell(directory, response.string[1:].strip())
        else:
            assert response.payload is None, repr(response)
            self.io.display(f'unknown command {response.string!r} ...')
            if self.test and self.test != 'allow_unknown_input':
                raise Exception(response)
        self.io.display('')
        if response.string == 'q':
            return
        elif self.navigation is not None:
            string = self.navigation
            self._navigation = None
            if string in self.commands:
                command = self.commands[string]
                try:
                    command(self.current_directory)
                except TypeError:
                    command()
        else:
            redraw = response.string is None or self._redraw
            self._redraw = None
            self._manage_directory(self.current_directory, redraw=redraw)

    def _match_alias(self, directory, string):
        if not self.aliases:
            return
        if not self.aliases.get(string):
            return
        value = self.aliases.get(string)
        path = Path(value)
        if path.exists():
            return path
        if (directory.is_score_package_path() and not directory.is_scores()):
            score_directory = directory.contents
            return directory.contents(value)

    def _match_files(self, files, strings, pattern, prefix):
        if pattern:
            files = self._filter_files(files, strings, pattern)
        else:
            files = [_ for _ in files if _.name[0].isalpha()]
        address = prefix + (pattern or '')
        count = len(files)
        counter = abjad.String('file').pluralize(count)
        message = f'matching {address!r} to {count} {counter} ...'
        self.io.display(message)
        return files

    def _match_smart_file(
        self,
        directory,
        pattern,
        paths,
        prefix,
        finder,
        default_name=None,
        ):
        if not pattern:
            self.io.display(f"missing {prefix!r} pattern ...")
            return prefix, None
        alias = ''
        if self.aliases and pattern in self.aliases:
            alias = pattern
            path, pattern = Path(self.aliases[pattern]), None
            if path.is_dir():
                directory, paths = path, None
            else:
                paths = [path]
        elif not (pattern and pattern[0].isdigit()):
            paths = None
        if isinstance(paths, Path):
            paths = [paths]
        if paths:
            files = self._supply_name(paths, default_name)
        else:
            files, strings = finder(directory)
            files = self._filter_files(files, strings, pattern)
        address = prefix + (pattern or '') + alias
        count = len(files)
        counter = abjad.String('file').pluralize(count)
        result = None
        if not files:
            self.io.display(f'matching {address!r} to {count} {counter} ...')
        elif len(files) == 1:
            result = files[0]
        else:
            self.io.display(f'matching {address!r} to {count} {counter} ...')
            for file_ in files:
                self.io.display(file_.trim(), raw=True)
            self.io.display(f"narrow search or use {2*prefix!r} for all ...")
        return address, result

    def _match_paths_in_buildspace(self, directory, name, verb):
        assert directory.is_buildspace()
        is_glob = False
        pattern = None
        selected_paths = []
        if directory.is_segment():
            path = directory(name)
            if path.is_file():
                selected_paths.append(path)
        elif not directory.is_parts():
            path = directory.build(name)
            if path.is_file():
                selected_paths.append(path)
        else:
            paths = directory.get_files_ending_with(name)
            if not paths:
                self.io.display(f'no files ending in {name} ...')
            self.io.display('found ...')
            for path in paths:
                self.io.display(f'{path.trim()}', raw=True)
            self.io.display('')
            pattern = self.io.get('match name')
            if pattern and self.is_navigation(pattern):
                return
            if not pattern:
                return
            if '*' in pattern:
                is_glob = True
                matches = sorted(directory.glob(str(pattern)))
                matches = list(matches)
            selected_paths = []
            for path in paths:
                if is_glob and path in matches:
                    selected_paths.append(path)
                elif path.name.startswith(pattern):
                    selected_paths.append(path)
        if not selected_paths:
            if pattern is None:
                self.io.display(f'no files matching {name} ...')
            elif is_glob:
                self.io.display(f'no files matching {pattern} ...')
            else:
                self.io.display(f'no files starting with {pattern} ...')
            return
        if 1 < len(selected_paths):
            self.io.display(f'will {verb} {len(selected_paths)} files ...')
            for path in selected_paths:
                self.io.display(path.trim(), raw=True)
            self.io.display('')
            ok = self.io.get('ok?')
            if ok and self.is_navigation(ok):
                return
            if ok != 'y':
                return
        return selected_paths

    @staticmethod
    def _message_activate(ly, tag, count, name=None):
        messages = []
        name = name or tag
        if 0 < count:
            counter = abjad.String('tag').pluralize(count)
            message = f'activating {count} {name} {counter}'
            if ly is not None:
                message += f' in {ly.name}'
            message += ' ...'
            messages.append(message)
        return messages

    @staticmethod
    def _message_deactivate(ly, tag, count, name=None):
        messages = []
        name = name or tag
        if 0 < count: 
            counter = abjad.String('tag').pluralize(count)
            message = f'deactivating {count} {name} {counter}'
            if ly is not None:
                message += f' in {ly.name}'
            message += ' ...'
            messages.append(message)
        return messages

    def _open_files(self, paths, force_vim=False, silent=False):
        assert isinstance(paths, collections.Iterable), repr(paths)
        for path in paths:
            if not path.exists():
                self.io.display(f'missing {path.trim()} ...')
                return
            if not path.is_file():
                self.io.display(f'not a file {path.trim()} ...')
                return
        string = ' '.join([str(_) for _ in paths])
        if (force_vim or all(_.suffix in self.configuration.editor_suffixes 
            for _ in paths)):
            mode = 'e'
        elif all(_.suffix in ('.mid', '.midi', '.pdf') for _ in paths):
            mode = 'o'
        else:
            mode = self.io.get('open or edit (o|e)?')
            if self.is_navigation(mode):
                return
            mode = mode.lower()
        if mode == 'e':
            command = f'vim {string}'
            if not silent:
                for path in paths:
                    self.io.display(f'editing {path.trim()} ...')
        elif mode == 'o':
            command = f'open {string}'
            if not silent:
                for path in paths:
                    self.io.display(f'opening {path.trim()} ...')
        else:
            return
        if 20 <= len(paths):
            response = self.io.get(f'{len(paths)} files ok?')
            if self.is_navigation(response):
                return response
            if response != 'y':
                return
        if self.test:
            return
        if not paths:
            return
        if (platform.system() == 'Darwin' and paths[0].suffix == '.pdf'):
            boilerplate = self.configuration.boilerplate_directory
            source = boilerplate / '__close_preview_pdf__.scr'
            for path in paths:
                template = source.read_text()
                template = template.format(file_path=path)
                target = self.configuration.home_directory / source.name
                if target.exists():
                    target.remove()
                with self.cleanup([target]):
                    target.write_text(template)
                    permissions = f'chmod 755 {target}'
                    abjad.IOManager.spawn_subprocess(permissions)
                    abjad.IOManager.spawn_subprocess(str(target))
        abjad.IOManager.spawn_subprocess(command)

    @staticmethod
    def _replace_in_file(file_path, old, new, whole_words=False):
        assert file_path.is_file()
        assert isinstance(old, str), repr(old)
        assert isinstance(new, str), repr(new)
        with file_path.open() as file_pointer:
            new_file_lines = []
            for line in file_pointer.readlines():
                if whole_words:
                    line = re.sub(r"\b%s\b" % old, new, line)
                else:
                    line = line.replace(old, new)
                new_file_lines.append(line)
        new_file_contents = ''.join(new_file_lines)
        file_path.write_text(new_file_contents)

    def _replace_in_tree(
        self,
        directory,
        search_string,
        replace_string,
        complete_words=False,
        ):
        command = f'ajv replace {search_string!r} {replace_string!r} -Y'
        if complete_words:
            command += ' -W'
        with self.change(directory):
            lines = abjad.IOManager.run_command(command)
            lines = [_.strip() for _ in lines if not _ == '']
            return lines

    def _run_doctest(self, paths):
        assert isinstance(paths, collections.Iterable), repr(paths)
        for path in paths:
            if path.is_dir():
                raise Exception(f'directory {path.trim()} not a file ...')
        if self.test:
            return
        if paths:
            string = ' '.join([str(_) for _ in paths])
            command = f'ajv doctest --external-modules=baca -x {string}'
            abjad.IOManager.spawn_subprocess(command)

    def _run_lilypond(self, ly):
        assert ly.exists()
        if not abjad.IOManager.find_executable('lilypond'):
            message = 'cannot find LilyPond executable.'
            raise ValueError(message)
        directory = ly.parent
        pdf = ly.with_suffix('.pdf')
        backup_pdf = ly.with_suffix('._backup.pdf')
        if backup_pdf.exists():
            backup_pdf.remove()
        with self.change(directory), self.cleanup([backup_pdf]):
            if pdf.exists():
                self.io.display(f'removing {pdf.trim()} ...')
                shutil.move(str(pdf), str(backup_pdf))
                assert not pdf.exists()
            else:
                backup_pdf = None
            self.io.display(f'interpreting {ly.trim()} ...')
            abjad.IOManager.run_lilypond(str(ly))
            if not pdf.is_file():
                self.io.display(f'can not produce {pdf.trim()} ...')
                if backup_pdf:
                    self.io.display(f'restoring {backup_pdf.trim()} ...')
                    shutil.move(str(backup_pdf), str(pdf))
            self.io.display(f'writing {pdf.trim()} ...')

    def _run_pytest(self, paths):
        assert isinstance(paths, collections.Iterable), repr(paths)
        for path in paths:
            if path.is_dir():
                raise Exception(f'directory {path.trim()} not a file ...')
        if self.test:
            return
        if paths:
            string = ' '.join([str(_) for _ in paths])
            command = f'py.test -xrf {string}; say "done"'
            abjad.IOManager.spawn_subprocess(command)

    def _select_part_names(self, directory, name, verb):
        part_names = directory._get_part_names()
        if not part_names:
            self.io.display('score template defines no part names.')
            return
        part_names_ = []
        for i, part_name in enumerate(part_names):
            part_name = part_name + (i + 1,)
            part_names_.append(part_name)
        part_names = part_names_
        self.io.display('found ...')
        for part_name in part_names:
            self.io.display(part_name[0], raw=True)
        self.io.display('')
        pattern = self.io.get('match name')
        if pattern and self.is_navigation(pattern):
            return
        if not pattern:
            return
        selected_part_names = []
        if pattern == '*':
            selected_part_names.extend(part_names)
        else:
            for part_name in part_names:
                if part_name[0].startswith(pattern):
                    selected_part_names.append(part_name)
                elif part_name[0].lower().startswith(pattern):
                    selected_part_names.append(part_name)
        if not selected_part_names:
            self.io.display(f'no part names starting with {pattern} ...')
            return
        if 1 < len(selected_part_names):
            self.io.display(f'will {verb} {len(selected_part_names)} files ...')
            for part_name in selected_part_names:
                dashed_name = abjad.String(part_name[0]).to_dash_case()
                file_name = f'{dashed_name}-{name}'
                path = directory(file_name)
                self.io.display(path.trim(), raw=True)
            self.io.display('')
            ok = self.io.get('ok?')
            if ok and self.is_navigation(ok):
                return
            if ok != 'y':
                return
        return selected_part_names

    def _select_paths(self, directory, infinitive=''):
        counter = abjad.String(directory.get_asset_type()).pluralize()
        paths = directory.list_paths()
        if not paths:
            self.io.display(f'missing {directory.trim()} {counter} ...')
            return
        items = [(_.get_identifier(), _) for _ in paths]
        if infinitive:
            prompt = f'select {counter} {infinitive}'
        else:
            prompt = f'select {counter}'
        selector = self._make_selector(
            aliases=None,
            force_single_column=True,
            items=items,
            navigations=self.navigations,
            prompt=prompt,
            )
        response = selector(redraw=False)
        if self.is_navigation(response.string):
            return response.string
        if response.payload is None:
            if bool(response.string):
                self.io.display(f'matches no path {response.string!r} ...')
            return
        assert isinstance(response.payload, list), response
        result = response.payload
        return result

    @staticmethod
    def _supply_name(paths, name):
        files = []
        for path in paths:
            if path.is_dir() and name:
                path /= name
            if path.is_file():
                files.append(path)
        return files

    @staticmethod
    def _to_paper_dimensions(paper_size, orientation='portrait'):
        orientations = ('landscape', 'portrait', None)
        assert orientation in orientations, repr(orientation)
        paper_dimensions = AbjadIDE.paper_size_to_paper_dimensions[paper_size]
        paper_dimensions = paper_dimensions.replace(' x ', ' ')
        width, height, unit = paper_dimensions.split()
        if orientation == 'landscape':
            height_ = width
            width_ = height
            height = height_
            width = width_
        return width, height, unit

    def _trash_files(self, path):
        if isinstance(path, list):
            paths = path
        else:
            paths = [path]
        for path in paths:
            if path.is_file():
                self.io.display(f'trashing {path.trim()} ...')
                path.remove()
            else:
                self.io.display(f'missing {path.trim()} ...')

    @staticmethod
    def _trim_ly(ly):
        assert ly.is_file()
        lines = []
        with ly.open() as file_pointer:
            found_score_block = False
            found_first_close_parallel = False
            for line in file_pointer.readlines():
                if line.startswith(r'\score'):
                    found_score_block = True
                    continue
                if line.startswith('}'):
                    found_score_block = False
                    lines.append('\n')
                    continue
                # first line after score block:
                if line == '    <<\n':
                    continue
                # second line after score block:
                if r'\include "layout.ly"' in line:
                    continue
                # antepenultimate line in file:
                if line == '    >>\n' and not found_first_close_parallel:
                    found_first_close_parallel = True
                    continue
                if found_score_block:
                    lines.append(line)
        if lines and lines[0].startswith('    '):
            lines = [_[4:] for _ in lines]
        if lines and lines[-1] == '\n':
            lines.pop()
        lines = ''.join(lines)
        return lines

    ### PUBLIC PROPERTIES ###

    @property
    def aliases(self):
        r'''Gets aliases.

        Returns dictionary.
        '''
        return self._aliases

    @property
    def clipboard(self):
        r'''Gets clipboard.

        Returns list.
        '''
        return self._clipboard

    @property
    def commands(self):
        r'''Gets commands.

        Returns list.
        '''
        return self._commands

    @property
    def current_directory(self):
        r'''Gets current directory.

        Returns list.
        '''
        return self._current_directory

    @property
    def example(self):
        r'''Is true when IDE is example.

        Returns true, false or none.
        '''
        return self._example

    @property
    def io(self):
        r'''Gets IO manager.

        Returns IO manager.
        '''
        return self._io

    @property
    def navigation(self):
        r'''Gets current navigation command.

        Returns string.
        '''
        return self._navigation

    @property
    def navigations(self):
        r'''Gets all navigation commands.

        Returns dictionary.
        '''
        return self._navigations

    @property
    def previous_directory(self):
        r'''Gets previous directory.

        Returns list.
        '''
        return self._previous_directory

    @property
    def test(self):
        r'''Is true when IDE is test.

        Returns true, false or none.
        '''
        return self._test

    ### PUBLIC METHODS ###

    @staticmethod
    def change(directory):
        r'''Makes temporary directory change context manager.
        '''
        return abjad.TemporaryDirectoryChange(directory=directory)

    @staticmethod
    def cleanup(remove=None):
        r'''Makes filesystem state context manager.
        '''
        return abjad.FilesystemState(remove=remove)

    def is_navigation(self, argument):
        r'''Is true when `argument` is navigation.

        Returns true or false.
        '''
        assert argument != '', repr(argument)
        if argument is None:
            return True
        if str(argument) in self.navigations:
            self._navigation = argument
            return True
        if isinstance(argument, Response):
            if argument.string is None:
                return True
            if argument.string in self.navigations:
                self._navigation = argument.string
                return True
        return False

    def test_baca_directories(self):
        r'''Is true when IDE can test local directories on Trevor's machine.

        Returns true or false.
        '''
        scores = abjad.abjad_configuration.composer_scores_directory
        if 'trevorbaca' in scores:
            return True
        return False

    ### USER METHODS ###

    @Command(
        'ctm',
        description=f'{abjad.tags.CLOCK_TIME_MARKUP} - activate',
        menu_section='markup',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def activate_clock_time_markup_tags(self, directory):
        r'''Activates clock time markup tags.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tag = abjad.tags.CLOCK_TIME_MARKUP
        self._activate_tag(directory, tag)

    @Command(
        'fnm',
        description=f'{abjad.tags.FIGURE_NAME_MARKUP} - activate',
        menu_section='markup',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def activate_figure_name_markup_tags(self, directory):
        r'''Activates figure name markup tags.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tag = abjad.tags.FIGURE_NAME_MARKUP
        self._activate_tag(directory, tag)

    @Command(
        'mnm',
        description=f'{abjad.tags.MEASURE_NUMBER_MARKUP} - activate',
        menu_section='markup',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def activate_measure_index_markup_tags(self, directory):
        r'''Activates measure index markup tags.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tag = abjad.tags.MEASURE_NUMBER_MARKUP
        self._activate_tag(directory, tag)

    @Command(
        'spm',
        description=f'{abjad.tags.SPACING_MARKUP} - activate',
        menu_section='markup',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def activate_spacing_markup_tags(self, directory):
        r'''Activates spacing markup tags.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tags = (
            abjad.tags.SPACING_MARKUP,
            abjad.tags.SPACING_OVERRIDE_MARKUP,
            )
        self._activate_tag(directory, baca.Match(match_any=tags))

    @Command(
        'snm',
        description=f'{abjad.tags.STAGE_NUMBER_MARKUP} - activate',
        menu_section='markup',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def activate_stage_number_markup_tags(self, directory):
        r'''Activates stage number markup tags.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tag = abjad.tags.STAGE_NUMBER_MARKUP
        self._activate_tag(directory, tag)

    @Command(
        'bw*',
        description='b&w - ALL',
        menu_section='bw',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def black_and_white_all(self, directory):
        r'''Renders all persistent indicators in black and white.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tags = self._get_persistent_indicator_color_expression_tags(directory)
        self._deactivate_tag(
            directory,
            baca.Match(match_any=tags),
            name='persistent indicator color expression',
            )
        tags = self._get_persistent_indicator_color_suppression_tags(
            directory)
        self._activate_tag(
            directory,
            baca.Match(match_any=tags),
            name='persistent indicator color suppression',
            )
        self._deactivate_tag(
            directory,
            baca.Match(match_any=abjad.tags.markup_tags),
            name='colored markup',
            )

    @Command(
        'bwc',
        description='b&w - CLEFS',
        menu_section='bw',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def black_and_white_clefs(self, directory):
        r'''Renders clefs in black and white.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tags = self._color_clef_tags
        if directory.is_build():
            tags += (baca.tags.REAPPLIED_CLEF,)
        self._deactivate_tag(
            directory,
            baca.Match(match_any=tags),
            name='clef',
            )

    @Command(
        'bwd',
        description='b&w - DYNAMICS',
        menu_section='bw',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def black_and_white_dynamics(self, directory):
        r'''Renders dynamics in black and white.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._deactivate_tag(
            directory,
            baca.Match(match_any=self._color_dynamic_tags),
            name='dynamic',
            )

    @Command(
        'bwi',
        description='b&w - INSTRUMENTS',
        menu_section='bw',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def black_and_white_instruments(self, directory):
        r'''Renders instruments in black and white.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tags = self._color_instrument_tags['activate']
        if directorty.is_build():
            tags += (baca.tags.REAPPLIED_INSTRUMENT,)
        self._deactivate_tag(
            directory,
            baca.Match(match_any=tags),
            name='instrument color expression',
            )
        self._activate_tag(
            directory,
            baca.Match(match_any=self._color_instrument_tags['deactivate']),
            name='instrument color suppression',
            )

    @Command(
        'ylb',
        description='layout ly - b&w',
        menu_section='layout',
        score_package_paths=('_segments', 'build',),
        )
    def black_and_white_layout_ly(self, directory):
        r'''Renders layout.ly file in black and white.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        name, verb = 'layout.ly', 'color'
        if directory.is_parts():
            paths = self._match_paths_in_buildspace(directory, name, verb)
        else:
            paths = [directory(name)]
        tags = (
            abjad.tags.SPACING_MARKUP,
            abjad.tags.SPACING_OVERRIDE_MARKUP,
            )
        for path in paths:
            self._deactivate_tag(
                path,
                baca.Match(match_any=tags),
                name='spacing markup',
                )

    @Command(
        'bwmm',
        description='b&w - MARGIN MARKUP',
        menu_section='bw',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def black_and_white_margin_markup(self, directory):
        r'''Renders margin markup in black and white.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._deactivate_tag(
            directory,
            baca.Match(match_any=self._color_margin_markup_tags['activate']),
            name='margin markup',
            )

    @Command(
        'bwtm',
        description='b&w - METRONOME MARKS',
        menu_section='bw',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def black_and_white_metronome_marks(self, directory):
        r'''Renders metronome marks in black and white.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tags = self._black_and_white_metronome_mark_tags['activate']
        self._activate_tag(
            directory,
            baca.Match(match_any=tags),
            name='b&w metronome mark expression',
            )
        tags = self._black_and_white_metronome_mark_tags['deactivate']
        self._deactivate_tag(
            directory,
            baca.Match(match_any=tags),
            name='b&w metrononme mark suppression',
            )

    @Command(
        'bwsl',
        description='b&w - STAFF LINES',
        menu_section='bw',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def black_and_white_staff_lines(self, directory):
        r'''Renders staff lines in black and white.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._deactivate_tag(
            directory,
            baca.Match(match_any=self._color_staff_line_tags),
            name='staff line color',
            )

    @Command(
        'bwts',
        description='b&w - TIME SIGNATURES',
        menu_section='bw',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def black_and_white_time_signatures(self, directory):
        r'''Renders time signatures in black and white.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._deactivate_tag(
            directory,
            baca.Match(match_any=self._color_time_signature_tags),
            name='color time signature',
            )

    @Command(
        'ab',
        description='part - build',
        menu_section='parts',
        score_package_paths=('parts',),
        )
    def build_part(self, directory):
        r'''Builds part from the ground up.

        Returns none.
        '''
        assert directory.is_parts()
        name = 'part.tex'
        part_names = self._select_part_names(directory, name, 'build')
        if not part_names:
            return
        total_parts = len(part_names)
        for i, part_name in enumerate(part_names):
            assert len(part_name) == 3, repr(part_name)
            part_name, abbreviation, number = part_name
            dashed_part_name = abjad.String(part_name).to_dash_case()
            name = 'front-cover.tex'
            file_name = f'{dashed_part_name}-{name}'
            path = directory(file_name)
            self.io.display(f'interpreting {path.trim()} ...')
            self._interpret_tex_file(path)
            self.io.display('')
            name = 'preface.tex'
            file_name = f'{dashed_part_name}-{name}'
            path = directory(file_name)
            self.io.display(f'interpreting {path.trim()} ...')
            self._interpret_tex_file(path)
            self.io.display('')
            name = 'music.ly'
            file_name = f'{dashed_part_name}-{name}'
            path = directory(file_name)
            self.io.display(f'interpreting {path.trim()} ...')
            self._run_lilypond(path)
            self.io.display('')
            name = 'back-cover.tex'
            file_name = f'{dashed_part_name}-{name}'
            path = directory(file_name)
            self.io.display(f'interpreting {path.trim()} ...')
            self._interpret_tex_file(path)
            self.io.display('')
            name = 'part.tex'
            file_name = f'{dashed_part_name}-{name}'
            path = directory(file_name)
            self.io.display(f'interpreting {path.trim()} ...')
            self._interpret_tex_file(path)
            if 1 < total_parts and i < total_parts - 1:
                self.io.display('')
        if len(part_names) == 1:
            name = 'part.pdf'
            file_name = f'{dashed_part_name}-{name}'
            path = directory(file_name)
            self._open_files([path])

    @Command(
        'bld',
        description='build - build',
        menu_section='build',
        score_package_path_blacklist=('parts',),
        score_package_paths=('_segments', 'build',),
        )
    def build_score(self, directory):
        r'''Builds score from the ground up.

        Returns none.
        '''
        assert directory.is_build() or directory.is__segments()
        directory = directory.build
        self.io.display('building score ...')
        self.collect_segment_lys(directory)
        self.io.display('')
        self.generate_music(directory)
        self.io.display('')
        self.interpret_music(directory, open_after=False)
        self.io.display('')
        tex = directory('front-cover.tex')
        pdf = directory('front-cover.pdf')
        if tex.is_file():
            self.interpret_front_cover(directory, open_after=False)
        elif pdf.is_file():
            self.io.display(f'using existing {pdf.trim()} ...')
        else:
            self.io.display('missing front cover ...')
            return
        self.io.display('')
        tex = directory('preface.tex')
        pdf = directory('preface.pdf')
        if tex.is_file():
            self.interpret_preface(directory, open_after=False)
        elif pdf:
            self.io.display(f'using existing {pdf.trim()} ...')
        else:
            self.io.display('missing preface ...')
            return
        self.io.display('')
        tex = directory('back-cover.tex')
        pdf = directory('back-cover.pdf')
        if tex.is_file():
            self.interpret_back_cover(directory, open_after=False)
        elif pdf.is_file():
            self.io.display(f'using existing {pdf.trim()} ...')
        else:
            self.io.display('missing back cover ...')
            return
        self.io.display('')
        self.generate_score(directory)
        self.io.display('')
        self.interpret_score(directory)

    @Command(
        '!',
        description='shell - call',
        external_directories=True,
        menu_section='shell',
        score_package_paths=True,
        scores_directory=True,
        )
    def call_shell(self, directory, statement):
        r'''Calls shell.

        Returns none.
        '''
        with self.change(directory):
            self.io.display(f'calling shell on {statement!r} ...')
            abjad.IOManager.spawn_subprocess(statement)

    @Command(
        'dfk',
        description='definition - check',
        menu_section='definition',
        score_package_paths=('material', 'segment',),
        )
    def check_definition(self, directory):
        r'''Checks definition.

        Returns integer exit code for Travis tests.
        '''
        assert directory.is_material_or_segment()
        self.io.display('checking definition ...')
        definition = directory('definition.py')
        if not definition.is_file():
            self.io.display(f'missing {definition.trim()} ...')
            return
        with abjad.Timer() as timer:
            result = self._interpret_file(definition)
        stdout_lines, stderr_lines, exit_code = result
        self.io.display(stdout_lines)
        if exit_code:
            self.io.display([f'{definition.trim()} FAILED:'] + stderr_lines)
        else:
            self.io.display(f'{definition.trim()} ... OK', raw=True)
        self.io.display(timer.total_time_message)
        return exit_code

    @Command(
        'dfk*',
        description='definitions - check',
        menu_section='definitions',
        score_package_paths=('materials', 'segments'),
        )
    def check_definitions(self, directory):
        r'''Checks definitions.

        Returns none.
        '''
        assert directory.is_materials_or_segments()
        paths = directory.list_paths()
        for i, path in enumerate(paths):
            self.check_definition(path)
            if i + 1 < len(paths):
                self.io.display('')

    @Command(
        'lyc*',
        description='lys - collect',
        menu_section='lys',
        score_package_paths=('_segments', 'build',),
        )
    def collect_segment_lys(self, directory):
        r'''Collects segment lys.

        Copies from segment directories to build/_segments directory.

        Trims top-level comments.

        Keeps includes and directives from each ly.

        Trims header and paper block from each ly.

        Keeps score block in each ly.

        Returns none.
        '''
        assert directory.is_build() or directory.is__segments()
        directory = directory.build
        self.io.display('collecting segment lys ...')
        pairs = self._collect_segment_lys(directory)
        if not pairs:
            self.io.display('... no segment lys found.')
            return
        if not directory._assets.is_dir():
            directory._assets.mkdir()
            gitignore = directory._assets / '.gitignore'
            gitignore.write_text('')
        if not directory._segments.is_dir():
            directory._segments.mkdir()
            gitignore = directory._segments / '.gitignore'
            gitignore.write_text('*.ly')
        fermata_measure_numbers = abjad.TypedOrderedDict()
        time_signatures = abjad.TypedOrderedDict()
        for source, target in pairs:
            if target.exists():
                self.io.display(f'removing {target.trim()} ...')
            self.io.display(f'writing {target.trim()} ...')
            text = self._trim_ly(source)
            target.write_text(text)
            segment = source.parent
            time_signatures_ = segment.get_metadatum('time_signatures')
            time_signatures[segment.name] = time_signatures_
            numbers = segment.get_metadatum('fermata_measure_numbers')
            if numbers:
                fermata_measure_numbers[segment.name] = numbers
        directory.contents.add_metadatum('time_signatures', time_signatures)
        directory.contents.add_metadatum(
            'fermata_measure_numbers',
            fermata_measure_numbers,
            )
        self._deactivate_tag(
            directory,
            '+',
            name='+',
            )
        stem = abjad.String(directory.name).to_shout_case()
        if directory.is_parts():
            stem += '*'
        document_names = directory.document_names
        self._deactivate_tag(
            directory,
            baca.Match(match_any=['-' + _ for _ in document_names]),
            name=f'-{stem}',
            )
        self._activate_tag(
            directory,
            baca.Match(match_any=['+' + _ for _ in document_names]),
            name=f'+{stem}',
            )
        self._deactivate_bar_line_adjustment_after_noneol_fermata(directory)
        self._deactivate_shifted_clef_at_bol(directory)
        self.black_and_white_all(directory)

    @Command(
        'cl*',
        description='color - ALL',
        menu_section='color',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def color_all(self, directory):
        r'''Colors all persistent indicators.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tags = self._get_persistent_indicator_color_expression_tags(directory)
        self._activate_tag(
            directory,
            baca.Match(match_any=tags),
            name='persistent indicator color expression',
            )
        tags = self._get_persistent_indicator_color_suppression_tags(
            directory)
        match = baca.Match(match_any=tags)
        self._deactivate_tag(
            directory,
            baca.Match(match_any=tags),
            name='persistent indicator color suppression',
            )

    @Command(
        'clc',
        description='color - CLEFS',
        menu_section='color',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def color_clefs(self, directory):
        r'''Colors clefs.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tags = self._color_clef_tags
        if directory.is_build():
            tags += (baca.tags.REAPPLIED_CLEF,)
        self._activate_tag(
            directory,
            baca.Match(match_any=tags),
            name='color clef',
            )

    @Command(
        'cld',
        description='color - DYNAMICS',
        menu_section='color',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def color_dynamics(self, directory):
        r'''Colors dynamics.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._activate_tag(
            directory,
            baca.Match(match_any=self._color_dynamic_tags),
            name='color dynamic',
            )

    @Command(
        'cli',
        description='color - INSTRUMENTS',
        menu_section='color',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def color_instruments(self, directory):
        r'''Colors instruments.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tags = self._color_instrument_tags['activate']
        self._activate_tag(
            directory,
            baca.Match(match_any=tags),
            name='instrument color expression',
            )
        tags = self._color_instrument_tags['deactivate']
        self._deactivate_tag(
            directory,
            baca.Match(match_any=tags),
            name='instrument color suppression',
            )

    @Command(
        'ylc',
        description='layout ly - color',
        menu_section='layout',
        score_package_paths=('_segments', 'build',),
        )
    def color_layout_ly(self, directory):
        r'''Colors layout.ly file.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        name, verb = 'layout.ly', 'color'
        if directory.is_parts():
            paths = self._match_paths_in_buildspace(directory, name, verb)
        else:
            paths = [directory(name)]
        tags = (
            abjad.tags.SPACING_MARKUP,
            abjad.tags.SPACING_OVERRIDE_MARKUP,
            )
        for path in paths:
            self._activate_tag(
                path,
                baca.Match(match_any=tags),
                name='spacing markup',
                )

    @Command(
        'clmm',
        description='color - MARGIN MARKUP',
        menu_section='color',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def color_margin_markup(self, directory):
        r'''Colors margin markup.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tags = self._color_margin_markup_tags['activate']
        self._activate_tag(
            directory,
            baca.Match(match_any=tags),
            name='color margin markup',
            )

    @Command(
        'cltm',
        description='color - METRONOME MARKS',
        menu_section='color',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def color_metronome_marks(self, directory):
        r'''Colors metronome marks.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tags = self._color_metronome_mark_tags['activate']
        self._activate_tag(
            directory,
            baca.Match(match_any=tags),
            name='metronome mark color expression',
            )
        tags = self._color_metronome_mark_tags['deactivate']
        self._deactivate_tag(
            directory,
            baca.Match(match_any=tags),
            name='metronome mark color suppression',
            )

    @Command(
        'clsl',
        description='color - STAFF LINES',
        menu_section='color',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def color_staff_lines(self, directory):
        r'''Colors staff lines.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._activate_tag(
            directory,
            baca.Match(match_any=self._color_staff_line_tags),
            name='staff line color',
            )

    @Command(
        'clts',
        description='color - TIME SIGNATURES',
        menu_section='color',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def color_time_signatures(self, directory):
        r'''Colors time signatures.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._activate_tag(
            directory,
            baca.Match(match_any=self._color_time_signature_tags),
            name='time signature color'
            )

    @Command(
        'cp',
        description='clipboard - copy',
        external_directories=True,
        menu_section='clipboard',
        score_package_paths=True,
        scores_directory=True,
        )
    def copy_to_clipboard(self, directory):
        r'''Copies to clipboard.

        Returns none.
        '''
        paths = self._select_paths(directory, infinitive='for clipboard')
        if self.is_navigation(paths):
            return
        assert isinstance(paths, list)
        self.io.display('copying to clipboard ...')
        for path in paths:
            self.io.display(path.trim(), raw=True)
            self.clipboard.append(path)

    @Command(
        'ctmx',
        description=f'{abjad.tags.CLOCK_TIME_MARKUP} - deactivate',
        menu_section='markup',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def deactivate_clock_time_markup_tags(self, directory):
        r'''Deactivates clock time markup tags.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tag = abjad.tags.CLOCK_TIME_MARKUP
        self._deactivate_tag(directory, tag)

    @Command(
        'fnmx',
        description=f'{abjad.tags.FIGURE_NAME_MARKUP} - deactivate',
        menu_section='markup',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def deactivate_figure_name_markup_tags(self, directory):
        r'''Deactivates figure name markup tags.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tag = abjad.tags.FIGURE_NAME_MARKUP
        self._deactivate_tag(directory, tag)

    @Command(
        'mnmx',
        description=f'{abjad.tags.MEASURE_NUMBER_MARKUP} - deactivate',
        menu_section='markup',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def deactivate_measure_index_markup_tags(self, directory):
        r'''Deactivates measure index markup tags.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tag = abjad.tags.MEASURE_NUMBER_MARKUP
        self._deactivate_tag(directory, tag)

    @Command(
        'spmx',
        description=f'{abjad.tags.SPACING_MARKUP} - deactivate',
        menu_section='markup',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def deactivate_spacing_markup_tags(self, directory):
        r'''Deactivates spacing markup tags.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tags = (
            abjad.tags.SPACING_MARKUP,
            abjad.tags.SPACING_OVERRIDE_MARKUP,
            )
        self._deactivate_tag(directory, tags)

    @Command(
        'snmx',
        description=f'{abjad.tags.STAGE_NUMBER_MARKUP} - deactivate',
        menu_section='markup',
        score_package_paths=('_segments', 'build', 'segment', 'segments'),
        )
    def deactivate_stage_number_markup_tags(self, directory):
        r'''Deactivates stage number markup tags.

        Returns none.
        '''
        assert directory.is_score_package_path()
        tag = abjad.tags.STAGE_NUMBER_MARKUP
        self._deactivate_tag(directory, tag)

    @Command(
        '^^',
        description='all - doctest',
        external_directories=True,
        menu_section='all',
        score_package_paths=True,
        scores_directory=True,
        )
    def doctest_all(self, directory, pattern=None):
        r'''Doctests all.

        Returns none.
        '''
        files, strings = directory._find_doctest_files(force=True)
        files = self._match_files(files, strings, pattern, '^^')
        self._run_doctest(files)
        abjad.IOManager.spawn_subprocess('say "done"')

    @Command(
        'dup',
        description='path - duplicate',
        external_directories=True,
        menu_section='path',
        score_package_path_blacklist=('contents', 'material', 'segment'),
        score_package_paths=True,
        scores_directory=True,
        )
    def duplicate(self, directory):
        r'''Duplicates asset in `directory`.

        Returns none.
        '''
        paths = self._select_paths(directory, infinitive='to duplicate')
        if self.is_navigation(paths):
            return
        assert isinstance(paths, list)
        if len(paths) == 1:
            source = paths[0]
            self.io.display(f'duplicating {source.trim()} ...')
        else:
            self.io.display(f'duplicating ...')
            for path in paths:
                self.io.display(f'    {path.trim()}')
            response = self.io.get('ok?')
            if self.is_navigation(response):
                return
            if response != 'y':
                return
        for source in paths:
            title = None
            name_metadatum = None
            if source.is_wrapper():
                title = self.io.get('enter title')
                if self.is_navigation(title):
                    continue
                name = title
            else:
                name = self.io.get('enter new name')
                if self.is_navigation(name):
                    continue
            name = source.parent.coerce(name, suffix=source.suffix)
            target = source.with_name(name)
            if source == target:
                continue
            if source.is_segment() and source.get_metadatum('name'):
                name_metadatum = self.io.get('name metadatum')
            self.io.display(f'writing {target.trim()} ...')
            response = self.io.get('ok?')
            if self.is_navigation(response):
                return
            if response != 'y':
                continue
            if source.is_file():
                shutil.copyfile(str(source), str(target))
            elif source.is_dir():
                shutil.copytree(str(source), str(target))
            else:
                raise ValueError(source)
            if target.is_material_or_segment():
                if name_metadatum:
                    target.add_metadatum('name', name_metadatum)
                else:
                    target.remove_metadatum('name')
                lines = self._replace_in_tree(
                    target,
                    source.name,
                    target.name,
                    complete_words=True,
                    )
                self.io.display(lines)
            elif target.is_wrapper():
                shutil.move(
                    str(target.wrapper(source.name)),
                    str(target.contents),
                    )
                lines = self._replace_in_tree(
                    target,
                    source.name,
                    target.name,
                    complete_words=True,
                    )
                self.io.display(lines)
                if title is not None:
                    target.contents.add_metadatum('title', title)
                    source_title = source.contents.get_metadatum('title')
                    if source_title is not None:
                        lines = self._replace_in_tree(
                            target,
                            source_title,
                            title,
                            complete_words=True,
                            )
                        self.io.display(lines)

    @Command(
        'al',
        description='log - aliases',
        external_directories=True,
        menu_section='log',
        score_package_paths=True,
        scores_directory=True,
        )
    def edit_aliases_file(self):
        r'''Edits aliases file.

        Returns none.
        '''
        self._open_files([self.configuration.aliases_file_path])
        self.configuration._read_aliases_file()
        self._aliases = dict(self.configuration.aliases)
        for name, path in self.aliases.items():
            if not Path(path).exists():
                self.io.display(f'missing {name!r} {path} ...')

    @Command(
        '@@',
        description='all - edit',
        external_directories=True,
        menu_section='all',
        score_package_paths=True,
        scores_directory=True,
        )
    def edit_all(self, directory, pattern=None):
        r'''Edits all.

        Returns none.
        '''
        files, strings = directory._find_editable_files(force=True)
        files = self._match_files(files, strings, pattern, '@@')
        self._open_files(files)

    @Command(
        'bce',
        description='back cover - edit',
        menu_section='back cover',
        score_package_paths=('_segments', 'build',),
        )
    def edit_back_cover_source(self, directory):
        r'''Edits ``back-cover.tex`` in `directory`.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        name = 'back-cover.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'open')
        if paths:
            self._open_files(paths)

    @Command(
        'dfe',
        description='definition - edit',
        menu_section='definition',
        score_package_paths=('material', 'segment',),
        )
    def edit_definition(self, directory):
        r'''Edits definition.

        Returns none.
        '''
        assert directory.is_material_or_segment()
        path = directory('definition.py')
        self._open_files([path])

    @Command(
        'dfe*',
        description='definitions - edit',
        menu_section='definitions',
        score_package_paths=('materials', 'segments',),
        )
    def edit_definitions(self, directory):
        r'''Edits definitions.

        Returns none.
        '''
        assert directory.is_materials_or_segments()
        definitions = []
        for path in directory.list_paths():
            definition = path('definition.py')
            if definition.is_file():
                definitions.append(definition)
        self._open_files(definitions)

    @Command(
        'fce',
        description='front cover - edit',
        menu_section='front cover',
        score_package_paths=('_segments', 'build',),
        )
    def edit_front_cover_source(self, directory):
        r'''Edits ``front-cover.tex`` in `directory`.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        name = 'front-cover.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'open')
        if paths:
            self._open_files(paths)

    @Command(
        'lx',
        description='log - latex',
        external_directories=True,
        menu_section='log',
        score_package_paths=True,
        scores_directory=True,
        )
    def edit_latex_log(self):
        r'''Edits LaTeX log.

        Returns none.
        '''
        path = self.configuration.latex_log_file_path
        self._open_files([path])

    @Command(
        'yle',
        description='layout ly - edit',
        menu_section='layout',
        score_package_paths=('_segments', 'build', 'segment',),
        )
    def edit_layout_ly(self, directory):
        r'''Edits layout.ly file.

        Returns none.
        '''
        assert directory.is_buildspace()
        name = 'layout.ly'
        paths = self._match_paths_in_buildspace(directory, name, 'open')
        if paths:
            self._open_files(paths)

    @Command(
        'ype',
        description='layout py - edit',
        menu_section='layout',
        score_package_paths=('_segments', 'build', 'segment',),
        )
    def edit_layout(self, directory):
        r'''Edits layout.py file.

        Returns none.
        '''
        assert directory.is_buildspace()
        name = 'layout.py'
        paths = self._match_paths_in_buildspace(directory, name, 'open')
        if paths:
            self._open_files(paths)

    @Command(
        'lp',
        description='log - lilypond',
        external_directories=True,
        menu_section='log',
        score_package_paths=True,
        scores_directory=True,
        )
    def edit_lilypond_log(self):
        r'''Edits LilyPond log.

        Returns none.
        '''
        path = Path(abjad.abjad_configuration.lilypond_log_file_path)
        self._open_files([path])

    @Command(
        'lye',
        description='ly - edit',
        menu_section='ly',
        score_package_paths=('material', 'segment',),
        )
    def edit_ly(self, directory):
        r'''Edits ``illustration.ly`` in `directory`.

        Returns none.
        '''
        assert directory.is_material_or_segment()
        path = directory('illustration.ly')
        self._open_files([path])

    @Command(
        'me',
        description='music - edit',
        menu_section='music',
        score_package_paths=('_segments', 'build',),
        )
    def edit_music_source(self, directory):
        r'''Edits ``music.ly`` in `directory`.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        name = 'music.ly'
        paths = self._match_paths_in_buildspace(directory, name, 'open')
        if paths:
            self._open_files(paths)

    @Command(
        'ae',
        description='part - edit',
        menu_section='parts',
        score_package_paths=('parts',),
        )
    def edit_part_source(self, directory):
        r'''Edits ``part.tex`` in `directory`.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        assert directory.is_parts()
        name = 'part.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'open')
        if paths:
            self._open_files(paths)

    @Command(
        'pe',
        description='preface - edit',
        menu_section='preface',
        score_package_paths=('_segments', 'build',),
        )
    def edit_preface_source(self, directory):
        r'''Edits ``preface.tex`` in `directory`.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        name = 'preface.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'open')
        if paths:
            self._open_files(paths)

    @Command(
        're',
        description='score - edit',
        menu_section='score',
        score_package_path_blacklist=('parts',),
        score_package_paths=('_segments', 'build',),
        )
    def edit_score_source(self, directory):
        r'''Edits ``score.tex`` in `directory`.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        path = directory('score.tex')
        self._open_files([path])

    @Command(
        'ye',
        description='stylesheet - edit',
        menu_section='stylesheet',
        score_package_paths=('_segments', 'build',),
        )
    def edit_stylesheet(self, directory):
        r'''Edits ``stylesheet.ily`` in `directory`.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        path = directory('stylesheet.ily')
        self._open_files([path])

    @Command(
        'it',
        description='text - edit',
        external_directories=True,
        menu_section='text',
        score_package_paths=True,
        scores_directory=True,
        )
    def edit_text(self, directory):
        r'''Opens Vim and goes to every occurrence of search string.

        Returns none.
        '''
        search_string = self.io.get('enter search string')
        if self.is_navigation(search_string):
            return
        command = rf'vim -c "grep {search_string!s} --type=python"'
        if self.test:
            return
        with self.change(directory):
            abjad.IOManager.spawn_subprocess(command)

    @Command(
        'cx',
        description='clipboard - empty',
        external_directories=True,
        menu_section='clipboard',
        score_package_paths=True,
        scores_directory=True,
        )
    def empty_clipboard(self, directory):
        r'''Empties clipboard.

        Returns none.
        '''
        if not bool(self.clipboard):
            self.io.display('clipboard is empty ...')
            return
        self.io.display('emptying clipboard ...')
        for path in self.clipboard:
            self.io.display(path.trim())
        self._clipboard[:] = []

    @Command(
        ';',
        description='show - column',
        external_directories=True,
        menu_section='show',
        score_package_paths=True,
        scores_directory=True,
        )
    def force_single_column(self):
        r'''Forces single-column display.

        Returns none.
        '''
        pass

    @Command(
        'bcg',
        description='back cover - generate',
        menu_section='back cover',
        score_package_paths=('_segments', 'build',),
        )
    def generate_back_cover(self, directory):
        r'''Generates ``back-cover.tex``.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'back-cover.tex'
        if not directory.is_parts():
            path = directory(name)
            self._generate_back_cover(path)
            return
        part_names = self._select_part_names(directory, name, 'generate')
        if not part_names:
            return
        total_parts = len(directory._get_part_names())
        for part_name in part_names:
            assert len(part_name) == 3, repr(part_name)
            part_name, abbreviation, number = part_name
            dashed_part_name = abjad.String(part_name).to_dash_case()
            file_name = f'{dashed_part_name}-{name}'
            path = directory(file_name)
            price = f'{abbreviation} ({number}/{total_parts})'
            self._generate_back_cover(path, price=price)

    @Command(
        'fcg',
        description='front cover - generate',
        menu_section='front cover',
        score_package_paths=('_segments', 'build',),
        )
    def generate_front_cover(self, directory):
        r'''Generates ``front-cover.tex``.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'front-cover.tex'
        if not directory.is_parts():
            path = directory(name)
            self._generate_front_cover(path)
            return
        part_names = self._select_part_names(directory, name, 'generate')
        if not part_names:
            return
        for part_name in part_names:
            assert len(part_name) == 3, repr(part_name)
            part_name, abbreviation, number = part_name
            dashed_part_name = abjad.String(part_name).to_dash_case()
            file_name = f'{dashed_part_name}-{name}'
            path = directory(file_name)
            words = abjad.String(part_name).delimit_words()
            words = [_.lower() for _ in words]
            forces_tagline = ' '.join(words) + ' part'
            path = directory(file_name)
            self._generate_front_cover(path, forces_tagline=forces_tagline)

    @Command(
        'mg',
        description='music - generate',
        menu_section='music',
        score_package_paths=('_segments', 'build',),
        )
    def generate_music(self, directory):
        r'''Generates build/``music.ly``.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'music.ly'
        if not directory.is_parts():
            path = directory(name)
            self._generate_music(path)
            return
        part_names = self._select_part_names(directory, name, 'generate')
        if not part_names:
            return
        for part_name in part_names:
            assert len(part_name) == 3, repr(part_name)
            part_name, abbreviation, number = part_name
            dashed_part_name = abjad.String(part_name).to_dash_case()
            file_name = f'{dashed_part_name}-{name}'
            path = directory(file_name)
            forces_tagline = abjad.String(part_name).delimit_words()
            forces_tagline = [_.lower() for _ in forces_tagline]
            forces_tagline = ' '.join(forces_tagline) + ' part'
            self._generate_music(
                path,
                forces_tagline=forces_tagline,
                keep_with_tag=part_name,
                )

    @Command(
        'ag',
        description='part - generate',
        menu_section='parts',
        score_package_paths=('parts',),
        )
    def generate_part(self, directory):
        r'''Generates ``part.tex``.

        Returns none.
        '''
        assert directory.is_parts()
        name = 'part.tex'
        part_names = self._select_part_names(directory, name, 'generate')
        if not part_names:
            return
        for part_name in part_names:
            assert len(part_name) == 3, repr(part_name)
            part_name, abbreviation, number = part_name
            dashed_part_name = abjad.String(part_name).to_dash_case()
            file_name = f'{dashed_part_name}-{name}'
            path = directory(file_name)
            self._generate_part(path, dashed_part_name)

    @Command(
        'pg',
        description='preface - generate',
        menu_section='preface',
        score_package_paths=('_segments', 'build',),
        )
    def generate_preface(self, directory):
        r'''Generates ``preface.tex``.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'preface.tex'
        if not directory.is_parts():
            path = directory(name)
            self._generate_preface(path)
            return
        part_names = self._select_part_names(directory, name, 'generate')
        if not part_names:
            return
        for part_name in part_names:
            assert len(part_name) == 3, repr(part_name)
            part_name, abbreviation, number = part_name
            dashed_part_name = abjad.String(part_name).to_dash_case()
            file_name = f'{dashed_part_name}-{name}'
            path = directory(file_name)
            self._generate_preface(path)

    @Command(
        'rg',
        description='score - generate',
        menu_section='score',
        score_package_path_blacklist=('parts',),
        score_package_paths=('_segments', 'build',),
        )
    def generate_score(self, directory):
        r'''Generates ``score.tex``.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        self.io.display('generating score ...')
        self._generate_document(directory)

    @Command(
        'yg',
        description='stylesheet - generate',
        menu_section='stylesheet',
        score_package_paths=('_segments', 'build',),
        )
    def generate_stylesheet(self, directory):
        r'''Generates build directory ``stylesheet.ily``.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        self.io.display('generating stylesheet ...')
        values = {}
        paper_size = directory.get_metadatum('paper_size', 'letter')
        values['paper_size'] = paper_size
        orientation = directory.get_metadatum('orientation', '')
        values['orientation'] = orientation
        self._copy_boilerplate(directory, 'stylesheet.ily', values=values)

    @Command(
        'get',
        description='path - get',
        menu_section='path',
        score_package_path_blacklist=('contents',),
        score_package_paths=True,
        )
    def get(self, directory):
        r'''Copies into `directory`.

        Returns none.
        '''
        items = []
        if directory.is_material_or_segment():
            siblings = directory.parent.list_paths()
            siblings.remove(directory)
            for sibling in siblings:
                definition = sibling('definition.py')
                if definition.is_file():
                    items.append((definition.trim(), definition))
            label = directory.get_asset_type()
            header = directory.get_header() 
            header += f' : get {label} ...'
        if not items:
            for path in directory.scores.list_paths():
                items.append((path.get_identifier(), path))
            label = abjad.String(directory.get_asset_type()).pluralize()
            header = directory.get_header() + f' : get {label} from ...'
            selector = self._make_selector(
                aliases=self.aliases,
                header=header,
                items=items,
                navigations=self.navigations,
                )
            response = selector()
            if self.is_navigation(response):
                self._redraw = True
                return
            if response.payload is None:
                self.io.display(f'matches no score {response.string!r} ...')
                return
            if isinstance(response.payload, list):
                assert len(response.payload) == 1, repr(response)
                score = response.payload[0]
            else:
                score = response.payload
            cousin = directory.with_score(score.name)
            items = []
            if directory.is_material_or_segment():
                cousins = cousin.parent.list_paths()
                cousins.remove(cousin)
                for cousin in cousins:
                    definition = cousin('definition.py')
                    if definition.is_file():
                        items.append((definition.trim(), definition))
                label = directory.get_asset_type()
            else:
                for path in cousin.list_paths():
                    items.append((path.get_identifier(), path))
            header = directory.get_header() 
            header += f' : get {score.get_identifier()} {label} ...'
        selector = self._make_selector(
            aliases=self.aliases,
            header=header,
            items=items,
            navigations=self.navigations,
            )
        response = selector()
        if self.is_navigation(response):
            self._redraw = True
            return
        if response.payload is None:
            self.io.display(f'matches no {label} {response.string!r} ...')
            return
        if isinstance(response.payload, Path):
            paths = [response.payload]
        else:
            paths = response.payload
        if len(paths) == 1:
            self.io.display(f'getting {paths[0].trim()} ...')
        else:
            self.io.display(f'getting ...')
            for path in paths:
                self.io.display(f'    {path.trim()}')
        targets = []
        for source in paths:
            target = directory(source.name)
            if target.exists():
                self.io.display(f'existing {target.trim()} ...')
                name = self.io.get('enter new name')
                if self.is_navigation(name):
                    return
                suffix = source.suffix
                name = source.parent.coerce(name, suffix=suffix)
                target = target.with_name(name)
                if target.exists():
                    self.io.display(f'existing {target.trim()} ...')
                    return
            targets.append(target)
        assert targets
        if len(targets) == 1:
            self.io.display(f'will write {targets[0].trim()} ...')
        else:
            self.io.display(f'will write ...')
            for target in targets:
                self.io.display(f'    {target.trim()} ...')
        response = self.io.get('ok?')
        if self.is_navigation(response):
            return
        if response != 'y':
            return
        for source, target in zip(paths, targets):
            self.io.display(f'writing {target.trim()} ...')
            if source.is_file():
                shutil.copyfile(str(source), str(target))
            elif source.is_dir():
                shutil.copytree(str(source), str(target))
            else:
                raise ValueError(source)
            if (source.is_material_or_segment() and
                source.get_metadatum('name')):
                name = self.io.get('name metadatum')
                if self.is_navigation(name):
                    return
                if name:
                    target.add_metadatum('name', name)
                else:
                    target.remove_metadatum('name')

    @Command(
        'ci',
        description='git - commit',
        external_directories=True,
        menu_section='git',
        score_package_paths=True,
        )
    def git_commit(self, directory, commit_message=None):
        r'''Commits working copy.

        Returns none.
        '''
        root = directory._get_repository_root()
        if not root:
            self.io.display(f'missing {directory.trim()} repository ...')
            return
        with self.change(root):
            self.io.display(f'git commit {root} ...')
            if not root._has_pending_commit():
                self.io.display(f'{root} ... nothing to commit.')
                return
            abjad.IOManager.spawn_subprocess('git status .')
            if self.test:
                return
            command = f'git add -A {root}'
            lines = abjad.IOManager.run_command(command)
            self.io.display(lines, raw=True)
            if commit_message is None:
                commit_message = self.io.get('commit message')
                if self.is_navigation(commit_message):
                    return
            command = f'git commit -m "{commit_message}" {root}'
            command += '; git push'
            lines = abjad.IOManager.run_command(command)
            self.io.display(lines, raw=True)

    @Command(
        'ci*',
        description='git - commit',
        menu_section='git',
        scores_directory=True,
        )
    def git_commit_every_package(self, directory):
        r'''Commits every working copy.

        Returns none.
        '''
        assert directory.is_scores()
        commit_message = self.io.get('commit message')
        if self.is_navigation(commit_message):
            return
        paths = directory.list_paths()
        for i, path in enumerate(paths):
            self.git_commit(path, commit_message=commit_message)
            if i + 1 < len(paths):
                self.io.display('')

    @Command(
        'diff',
        description='git - diff',
        external_directories=True,
        menu_section='git',
        score_package_paths=True,
        )
    def git_diff(self, directory):
        r'''Displays Git diff of working copy.

        Returns none.
        '''
        if not directory._get_repository_root():
            self.io.display(f'missing {directory.trim()} repository ...')
            return
        with self.change(directory):
            self.io.display(f'git diff {directory.trim()} ...')
            abjad.IOManager.spawn_subprocess(f'git diff {directory}')

    @Command(
        'diff*',
        description='git - diff',
        menu_section='git',
        scores_directory=True,
        )
    def git_diff_every_package(self, directory):
        r'''Displays Git diff of every working copy.

        Returns none.
        '''
        assert directory.is_scores()
        paths = directory.list_paths()
        for i, path in enumerate(paths):
            self.git_diff(path)
            if i + 1 < len(paths):
                self.io.display('')

    @Command(
        'pull',
        description='git - pull',
        external_directories=True,
        menu_section='git',
        score_package_paths=True,
        )
    def git_pull(self, directory):
        r'''Pulls working copy.

        Returns none.
        '''
        root = directory._get_repository_root()
        if not root:
            self.io.display(f'missing {directory.trim()} repository ...')
            return
        with self.change(root):
            self.io.display(f'git pull {root} ...')
            if not self.test:
                lines = abjad.IOManager.run_command('git pull .')
                if lines and 'Already up-to-date' in lines[-1]:
                    lines = lines[-1:]
                self.io.display(lines)
                command = 'git submodule foreach git pull origin master'
                self.io.display(f'{command} ...')
                lines = abjad.IOManager.run_command(command)
                if lines and 'Already up-to-date' in lines[-1]:
                    lines = lines[-1:]
                self.io.display(lines)

    @Command(
        'pull*',
        description='git - pull',
        menu_section='git',
        scores_directory=True,
        )
    def git_pull_every_package(self, directory):
        r'''Pulls every working copy.

        Returns none.
        '''
        assert directory.is_scores()
        paths = directory.list_paths()
        for i, path in enumerate(paths):
            self.git_pull(path)
            if i + 1 < len(paths):
                self.io.display('')

    @Command(
        'push',
        description='git - push',
        external_directories=True,
        menu_section='git',
        score_package_paths=True,
        )
    def git_push(self, directory):
        r'''Pushes working copy.

        Returns none.
        '''
        root = directory._get_repository_root()
        if not root:
            self.io.display(f'missing {directory.trim()} repository ...')
            return
        with self.change(root):
            self.io.display(f'git push {root} ...')
            if not self.test:
                abjad.IOManager.spawn_subprocess('git push .')

    @Command(
        'push*',
        description='git - push',
        menu_section='git',
        scores_directory=True,
        )
    def git_push_every_package(self, directory):
        r'''Pushes every package.

        Returns none.
        '''
        assert directory.is_scores()
        paths = directory.list_paths()
        for i, path in enumerate(paths):
            self.git_push(path)
            if i + 1 < len(paths):
                self.io.display('')

    @Command(
        'st',
        description='git - status',
        external_directories=True,
        menu_section='git',
        score_package_paths=True,
        )
    def git_status(self, directory):
        r'''Displays Git status of working copy.

        Returns none.
        '''
        root = directory._get_repository_root()
        if not root:
            self.io.display(f'missing {directory.trim()} repository ...')
            return
        with self.change(root):
            self.io.display(f'git status {root} ...')
            abjad.IOManager.spawn_subprocess('git status .')
            self.io.display('')
            command = 'git submodule foreach git fetch'
            self.io.display(f'{command} ...')
            abjad.IOManager.spawn_subprocess(command)

    @Command(
        'st*',
        description='git - status',
        menu_section='git',
        scores_directory=True,
        )
    def git_status_every_package(self, directory):
        r'''Displays Git status of every working copy.

        Returns none.
        '''
        assert directory.is_scores()
        paths = directory.list_paths()
        for i, path in enumerate(paths):
            self.git_status(path)
            if i + 1 < len(paths):
                self.io.display('')

    @Command(
        '-',
        description='go - back',
        external_directories=True,
        menu_section='go',
        score_package_paths=True,
        scores_directory=True,
        )
    def go_back(self):
        r'''Goes back.

        Returns none.
        '''
        if self.previous_directory:
            self._manage_directory(self.previous_directory)
        else:
            self._manage_directory(self.current_directory)

    @Command(
        'bb',
        description='package - builds',
        menu_section='package',
        score_package_paths=True,
        )
    def go_to_builds_directory(self, directory):
        r'''Goes to builds directory.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._manage_directory(directory.builds())

    @Command(
        'cc',
        description='package - contents',
        menu_section='package',
        score_package_paths=True,
        )
    def go_to_contents_directory(self, directory):
        r'''Goes to contents directory.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._manage_directory(directory.contents)

    @Command(
        '%',
        description='go - directory',
        external_directories=True,
        menu_section='go',
        score_package_paths=True,
        scores_directory=True,
        )
    def go_to_directory(self, directory, pattern=None, payload=None):
        r'''Goes to directory.

        Returns none.
        '''
        assert directory.is_dir()
        address = '%' + (pattern or '')
        if self.aliases and pattern in self.aliases:
            path = Path(self.aliases[pattern])
            self.io.display(f'matching {address!r} to {path.trim()} ...')
            self._manage_directory(path)
            return
        if isinstance(payload, Path):
            path = payload
            self.io.display(f'matching {address!r} to {path.trim()} ...')
            self._manage_directory(path)
            return
        if isinstance(payload, list) and len(payload) == 1:
            path = payload[0]
            self.io.display(f'matching {address!r} to {path.trim()} ...')
            self._manage_directory(path)
            return
        if isinstance(payload, list):
            assert all(isinstance(_, Path) for _ in payload), repr(payload)
            paths = payload
            counter = abjad.String('directory').pluralize(len(paths))
            message = f'matching {address!r} to {len(paths)} {counter} ...'
            self.io.display(message)
            for path in paths:
                self.io.display(path.trim(), raw=True)
            if paths:
                self._manage_directory(paths[:1])
            return
        assert payload is None, repr(payload)
        paths, strings = [], []
        if directory.is_score_package_path():
            root = directory.contents
        else:
            root = directory
        for path in sorted(root.glob('**/*')):
            if '__pycache__' in str(path):
                continue
            if not path.is_dir():
                continue
            paths.append(path)
            strings.append(path.name)
        if isinstance(pattern, str):
            indices = abjad.String.match_strings(strings, pattern)
            paths = abjad.Sequence(paths).retain(indices)
        if len(paths) == 1:
            self.io.display(f'matching {address!r} to {paths[0].trim()} ...')
        else:
            counter = abjad.String('directory').pluralize(len(paths))
            message = f'matching {address!r} to {len(paths)} {counter} ...'
            self.io.display(message)
            for path in paths:
                self.io.display(path.trim(), raw=True)
        if paths:
            self._manage_directory(paths[0])

    @Command(
        'dd',
        description='package - distribution',
        menu_section='package',
        score_package_paths=True,
        )
    def go_to_distribution_directory(self, directory):
        r'''Goes to distribution directory.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._manage_directory(directory.distribution())

    @Command(
        'ee',
        description='package - etc',
        menu_section='package',
        score_package_paths=True,
        )
    def go_to_etc_directory(self, directory):
        r'''Goes to etc directory.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._manage_directory(directory.etc())

    @Command(
        'll',
        description='go - library',
        external_directories=True,
        menu_section='go',
        score_package_paths=True,
        scores_directory=True,
        )
    def go_to_library(self):
        r'''Goes to library.

        Returns none.
        '''
        library = abjad.abjad_configuration.composer_library_tools
        if library is None:
            self.io.display('missing library ...')
        else:
            self._manage_directory(Path(library))

    @Command(
        'mm',
        description='package - materials',
        menu_section='package',
        score_package_paths=True,
        )
    def go_to_materials_directory(self, directory):
        r'''Goes to materials directory.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._manage_directory(directory.materials())

    @Command(
        '>',
        description='hop - next package',
        menu_section='hop',
        score_package_paths=('material', 'materials', 'segment', 'segments'),
        )
    def go_to_next_package(self, directory):
        r'''Goes to next package.

        Returns none.
        '''
        assert (directory.is_material_or_segment() or
            directory.is_materials_or_segments())
        directory = directory.get_next_package(cyclic=True)
        self._manage_directory(directory)

    @Command(
        '>>',
        description='hop - next score',
        menu_section='hop',
        score_package_paths=True,
        scores_directory=True,
        )
    def go_to_next_score(self, directory):
        r'''Goes to next score.

        Returns none.
        '''
        assert directory.is_score_package_path() or directory.is_scores()
        wrapper = directory.get_next_score(cyclic=True)
        self._manage_directory(wrapper.contents)

    @Command(
        '<',
        description='hop - previous package',
        menu_section='hop',
        score_package_paths=('material', 'materials', 'segment', 'segments',),
        )
    def go_to_previous_package(self, directory):
        r'''Goes to previous package.

        Returns none.
        '''
        assert (directory.is_material_or_segment() or
            directory.is_materials_or_segments())
        directory = directory.get_previous_package(cyclic=True)
        self._manage_directory(directory)

    @Command(
        '<<',
        description='hop - previous score',
        menu_section='hop',
        score_package_paths=True,
        scores_directory=True,
        )
    def go_to_previous_score(self, directory):
        r'''Goes to previous score.

        Returns none.
        '''
        assert directory.is_score_package_path() or directory.is_scores()
        wrapper = directory.get_previous_score(cyclic=True)
        self._manage_directory(wrapper.contents)

    @Command(
        'ss',
        description='go - scores',
        external_directories=True,
        menu_section='go',
        score_package_paths=True,
        scores_directory=True,
        )
    def go_to_scores_directory(self):
        r'''Goes to scores directory.

        Returns none.
        '''
        directory = self.configuration.composer_scores_directory
        if self.test or self.example:
            directory = self.configuration.test_scores_directory
        self._manage_directory(directory)

    @Command(
        'gg',
        description='package - segments',
        menu_section='package',
        score_package_paths=True,
        )
    def go_to_segments_directory(self, directory):
        r'''Goes to segments directory.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._manage_directory(directory.segments())

    @Command(
        'yy',
        description='package - stylesheets',
        menu_section='package',
        score_package_paths=True,
        )
    def go_to_stylesheets_directory(self, directory):
        r'''Goes to stylesheets directory.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._manage_directory(directory.stylesheets())

    @Command(
        'tt',
        description='package - test',
        menu_section='package',
        score_package_paths=True,
        )
    def go_to_test_directory(self, directory):
        r'''Goes to test directory.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._manage_directory(directory.test())

    @Command(
        'oo',
        description='package - tools',
        menu_section='package',
        score_package_paths=True,
        )
    def go_to_tools_directory(self, directory):
        r'''Goes to tools directory.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._manage_directory(directory.tools())

    @Command(
        'ww',
        description='package - wrapper',
        menu_section='package',
        score_package_paths=True,
        )
    def go_to_wrapper_directory(self, directory):
        r'''Goes to wrapper directory.

        Returns none.
        '''
        assert directory.is_score_package_path()
        self._manage_directory(directory.wrapper)

    @Command(
        '..',
        description='go - up',
        external_directories=True,
        menu_section='go',
        score_package_paths=True,
        scores_directory=True,
        )
    def go_up(self):
        r'''Goes up.

        Returns none.
        '''
        if self.current_directory:
            self._manage_directory(self.current_directory.parent)

    @Command(
        'bci',
        description='back cover - interpret',
        menu_section='back cover',
        score_package_paths=('_segments', 'build',),
        )
    def interpret_back_cover(self, directory, open_after=True):
        r'''Interprets ``back-cover.tex``.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'back-cover.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'interpret')
        if not paths:
            return
        for path in paths:
            self._interpret_tex_file(path)
        if len(paths) == 1:
            target = path.with_suffix('.pdf')
            if target.is_file() and open_after:
                self._open_files([target])

    @Command(
        'fci',
        description='front cover - interpret',
        menu_section='front cover',
        score_package_paths=('_segments', 'build',),
        )
    def interpret_front_cover(self, directory, open_after=True):
        r'''Interprets ``front-cover.tex``.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'front-cover.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'interpret')
        if not paths:
            return
        for path in paths:
            self._interpret_tex_file(path)
        if len(paths) == 1:
            target = path.with_suffix('.pdf')
            if target.is_file() and open_after:
                self._open_files([target])

    @Command(
        'lyi',
        description='ly - interpret',
        menu_section='ly',
        score_package_paths=('material', 'segment',),
        )
    def interpret_ly(self, directory, open_after=True):
        r'''Interprets illustration ly in `directory`.

        Makes illustration PDF.

        Returns none.
        '''
        assert directory.is_material_or_segment()
        self.io.display('interpreting ly ...')
        source = directory('illustration.ly')
        target = source.with_suffix('.pdf')
        if source.is_file():
            self._run_lilypond(source)
        else:
            self.io.display(f'missing {source.trim()} ...')
        if target.is_file() and open_after:
            self._open_files([target])

    @Command(
        'lyi*',
        description='lys - interpret',
        menu_section='lys',
        score_package_paths=('materials', 'segments',),
        )
    def interpret_lys(self, directory):
        r'''Interprets LilyPond file in every directory.

        Makes PDF in every directory.

        Returns none.
        '''
        assert directory.is_materials_or_segments()
        self.io.display('interpreting every ly ...')
        paths = directory.list_paths()
        sources = []
        for path in paths:
            source = path('illustration.ly')
            if source.is_file():
                sources.append(source)
        if not sources:
            self.io.display('missing LilyPond files ...')
            return
        with abjad.Timer() as timer:
            for i, source in enumerate(sources):
                self.interpret_ly(source.parent, open_after=False)
                if i + 1 < len(sources):
                    self.io.display('')
            self.io.display(timer.total_time_message)

    @Command(
        'mi',
        description='music - interpret',
        menu_section='music',
        score_package_paths=('_segments', 'build',),
        )
    def interpret_music(self, directory, open_after=True):
        r'''Interprets ``music.ly``.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'music.ly'
        paths = self._match_paths_in_buildspace(directory, name, 'interpret')
        if not paths:
            return
        for path in paths:
            self._run_lilypond(path)
        if len(paths) == 1:
            target = path.with_suffix('.pdf')
            if target.is_file() and open_after:
                self._open_files([target])

    @Command(
        'ai',
        description='part - interpret',
        menu_section='parts',
        score_package_paths=('parts',),
        )
    def interpret_part(self, directory, open_after=True):
        r'''Interprets ``part.tex``.

        Returns none.
        '''
        assert directory.is_parts()
        name = 'part.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'interpret')
        if not paths:
            return
        for path in paths:
            self._interpret_tex_file(path)
        if len(paths) == 1:
            target = path.with_suffix('.pdf')
            if target.is_file() and open_after:
                self._open_files([target])

    @Command(
        'pi',
        description='preface - interpret',
        menu_section='preface',
        score_package_paths=('_segments', 'build',),
        )
    def interpret_preface(self, directory, open_after=True):
        r'''Interprets ``preface.tex``.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'preface.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'interpret')
        if not paths:
            return
        for path in paths:
            self._interpret_tex_file(path)
        if len(paths) == 1:
            target = path.with_suffix('.pdf')
            if target.is_file() and open_after:
                self._open_files([target])

    @Command(
        'ri',
        description='score - interpret',
        menu_section='score',
        score_package_path_blacklist=('parts',),
        score_package_paths=('_segments', 'build',),
        )
    def interpret_score(self, directory, open_after=True):
        r'''Interprets ``score.tex``.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'score.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'interpret')
        if not paths:
            return
        for path in paths:
            self._interpret_tex_file(path)
        if len(paths) == 1:
            target = path.with_suffix('.pdf')
            if target.is_file() and open_after:
                self._open_files([target])

    @Command(
        'ylm',
        description='layout ly - make',
        menu_section='layout',
        score_package_paths=('_segments', 'build', 'segment',),
        )
    def make_layout_ly(self, directory):
        r'''Makes layout.ly.

        Returns none.
        '''
        assert directory.is_buildspace()
        if directory.is__segments():
            directory = directory.build
        name = 'layout.py'
        paths = self._match_paths_in_buildspace(directory, name, 'interpret')
        if not paths:
            return
        total = len(paths)
        for i, layout_py in enumerate(paths):
            self.io.display(f'interpreting {layout_py.trim()} ...')
            layout_ly = layout_py.with_suffix('.ly')
            if not layout_py.is_file():
                self.io.display(f'missing {layout_py.trim()} ...')
                continue
            maker = '__make_layout_ly__.py'
            maker = directory(maker)
            with self.cleanup([maker]):
                self._copy_boilerplate(
                    directory,
                    maker.name,
                    values={'layout_module_name':layout_py.stem},
                    )
                self.io.display(f'interpreting {maker.trim()} ...')
                result = self._interpret_file(maker)
                error_code = result[-1]
                if error_code == 0 and layout_ly.is_file():
                    self.io.display(f'writing {layout_ly.trim()} ...')
                self.io.display(f'removing {maker.trim()} ...')
            stdout_lines, stderr_lines, exit_code = result
            if exit_code:
                self.io.display(stderr_lines, raw=True)
            if 0 < total and i < total - 1:
                self.io.display('')

    @Command(
        'lym',
        description='ly - make',
        menu_section='ly',
        score_package_paths=('material', 'segment',),
        )
    def make_ly(self, directory):
        r'''Makes illustration ly.

        Returns none.
        '''
        assert directory.is_material_or_segment()
        self.io.display('making ly ...')
        if directory.is_material():
            self._make_material_ly(directory)
        elif directory.is_segment():
            self._make_segment_ly(directory)
        else:
            raise ValueError(directory)

    @Command(
        'lym*',
        description='lys - make',
        menu_section='lys',
        score_package_paths=('materials', 'segments',),
        )
    def make_lys(self, directory):
        r'''Makes lys.

        Returns none.
        '''
        assert directory.is_materials_or_segments()
        paths = directory.list_paths()
        for i, path in enumerate(paths):
            path.make_ly()
            if i + 1 < len(paths):
                self.io.display('')

    @Command(
        'midm',
        description='midi - make',
        menu_section='midi',
        score_package_paths=('segment',),
        )
    def make_midi(self, directory, open_after=True):
        r'''Makes segment MIDI file.

        Returns integer exit code for Travis tests.
        '''
        assert directory.is_segment()
        return self._make_segment_midi(directory, open_after=open_after)

    @Command(
        'pdfm',
        description='pdf - make',
        menu_section='pdf',
        score_package_paths=('material', 'segment',),
        )
    def make_pdf(self, directory, open_after=True):
        r'''Makes illustration PDF.

        Returns integer exit code for Travis tests.
        '''
        assert directory.is_material_or_segment()
        if directory.is_material():
            return self._make_material_pdf(
                directory,
                open_after=open_after,
                )
        elif directory.is_segment():
            return self._make_segment_pdf(directory, open_after=open_after)
        else:
            raise ValueError(directory)

    @Command(
        'pdfm*',
        description='pdfs - make',
        menu_section='pdfs',
        score_package_paths=('materials', 'segments',),
        )
    def make_pdfs(self, directory):
        r'''Makes PDF in every directory.

        Returns none.
        '''
        assert directory.is_materials_or_segments()
        paths = directory.list_paths()
        for i, path in enumerate(paths):
            self.make_pdf(path, open_after=False)
            if i + 1 < len(paths):
                self.io.display('')
            else:
                abjad.IOManager.spawn_subprocess('say "done"')

    @Command(
        'new',
        description='path - new',
        external_directories=True,
        menu_section='path',
        score_package_path_blacklist=('contents',),
        score_package_paths=True,
        scores_directory=True,
        )
    def new(self, directory):
        r'''Makes asset.

        Returns none.
        '''
        if directory.is_builds():
            self._make_build_directory(directory)
        elif directory.is_materials_or_segments():
            self._make_package(directory)
        elif directory.is_scores():
            self._make_score_package()
        else:
            self._make_file(directory)

    @Command(
        '**',
        description='all - pdfs',
        external_directories=True,
        menu_section='all',
        score_package_paths=True,
        scores_directory=True,
        )
    def open_all_pdfs(self, directory, pattern=None):
        r'''Opens all PDFs.

        Returns none.
        '''
        files, strings = directory._find_pdfs(force=True)
        files = self._match_files(files, strings, pattern, '**')
        self._open_files(files)

    @Command(
        'bco',
        description='back cover - open',
        menu_section='back cover',
        score_package_paths=('_segments', 'build',),
        )
    def open_back_cover_pdf(self, directory):
        r'''Opens ``back-cover.pdf`` in `directory`.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'back-cover.pdf'
        paths = self._match_paths_in_buildspace(directory, name, 'open')
        if paths:
            self._open_files(paths)

    @Command(
        'fco',
        description='front cover - open',
        menu_section='front cover',
        score_package_paths=('_segments', 'build',),
        )
    def open_front_cover_pdf(self, directory):
        r'''Opens files ending in ``front-cover.pdf`` in `directory`.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'front-cover.pdf'
        paths = self._match_paths_in_buildspace(directory, name, 'open')
        if paths:
            self._open_files(paths)

    @Command(
        'mo',
        description='music - open',
        menu_section='music',
        score_package_paths=('_segments', 'build',),
        )
    def open_music_pdf(self, directory):
        r'''Opens ``music.pdf`` in `directory`.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'music.pdf'
        paths = self._match_paths_in_buildspace(directory, name, 'open')
        if paths:
            self._open_files(paths)

    @Command(
        'ao',
        description='part - open',
        menu_section='parts',
        score_package_paths=('parts',),
        )
    def open_part_pdf(self, directory):
        r'''Opens ``part.pdf`` in `directory`.

        Returns none.
        '''
        assert directory.is_parts()
        name = 'part.pdf'
        paths = self._match_paths_in_buildspace(directory, name, 'open')
        if paths:
            self._open_files(paths)

    @Command(
        'pdfo',
        description='pdf - open',
        menu_section='pdf',
        score_package_paths=('material', 'segment',),
        )
    def open_pdf(self, directory):
        r'''Opens illustration PDF.

        Returns none.
        '''
        assert directory.is_material_or_segment()
        path = directory('illustration.pdf')
        self._open_files([path])

    @Command(
        'po',
        description='preface - open',
        menu_section='preface',
        score_package_paths=('_segments', 'build',),
        )
    def open_preface_pdf(self, directory):
        r'''Opens ``preface.pdf`` in `directory`.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'preface.pdf'
        paths = self._match_paths_in_buildspace(directory, name, 'open')
        if paths:
            self._open_files(paths)

    @Command(
        'ro',
        description='score - open',
        menu_section='score',
        score_package_paths=True,
        )
    def open_score(self, directory):
        r'''Opens ``score.pdf`` in build `directory`.

        Opens score PDF in all other package directories.

        Returns none.
        '''
        if directory.is_build() and not directory.is_parts():
            name = 'score.pdf'
            paths = directory.get_files_ending_with(name)
            if paths:
                self._open_files(paths)
            else:
                self.io.display(f'no files ending in *{name} ...')
        else:
            assert directory.is_score_package_path()
            path = directory._get_score_pdf()
            if path:
                self._open_files([path])
            else:
                message = 'missing score PDF'
                message += ' in distribution and build directories ...'
                self.io.display(message)

    @Command(
        'ro*',
        description='scores - open',
        menu_section='score',
        scores_directory=True,
        )
    def open_scores(self, directory):
        r'''Opens score PDF in all score packages.

        Returns none.
        '''
        assert directory.is_scores()
        pdfs = []
        for path in directory.list_paths():
            pdf = path._get_score_pdf()
            if pdf:
                pdfs.append(pdf)
        self._open_files(pdfs)

    @Command(
        'parts',
        description='parts - new',
        menu_section='parts',
        score_package_paths=('builds',),
        )
    def parts(self, directory):
        r'''Makes new parts directory.

        Returns none.
        '''
        assert directory.is_builds()
        self.io.display('getting part names from score template ...')
        result = directory._get_part_names()
        if isinstance(result, tuple) and result[0] == -1:
            message = result[-1]
            self.io.display(message)
            return
        part_name_pairs = result
        part_names = [_[0] for _ in result]
        part_abbreviations = [_[1] for _ in result]
        for part_name in part_names:
            self.io.display(f'found {part_name} ...')
        self.io.display('')
        name = self.io.get('directory name')
        if self.is_navigation(name):
            return
        name = directory.coerce(name)
        directory = directory / name
        if directory.exists():
            self.io.display(f'existing {directory.trim()} ...')
            return
        paper_size = self.io.get('paper size')
        if self.is_navigation(paper_size):
            return
        orientation = 'portrait'
        if paper_size.endswith(' landscape'):
            orientation = 'landscape'
            length = len(' landscape')
            paper_size = paper_size[:-length]
        elif paper_size.endswith(' portrait'):
            length = len(' portrait')
            paper_size = paper_size[:-length]
        if paper_size not in self.known_paper_sizes:
            self.io.display(f'unknown paper size: {paper_size} ...')
            self.io.display(f'choose from ...')
            for paper_size in self.known_paper_sizes:
                self.io.display(f'    {paper_size}')
            return
        suffix = self.io.get('catalog number suffix')
        if self.is_navigation(suffix):
            return
        names = (
            'front-cover.tex',
            'preface.tex',
            'music.ly',
            'back-cover.tex',
            'part.tex',
            )
        paths = [directory / _ for _ in names]
        self.io.display('will make ...')
        self.io.display(f'    {directory.trim()}')
        path = directory / 'stylesheet.ily'
        self.io.display(f'    {path.trim()}')
        for part_name in part_names:
            part_name_ = abjad.String(part_name).to_dash_case()
            for name in names:
                name = f'{part_name_}-{name}'
                path = directory / name
                self.io.display(f'    {path.trim()}')
        response = self.io.get('ok?')
        if self.is_navigation(response):
            return
        if response != 'y':
            return
        assert not directory.exists()
        directory.mkdir()
        directory.add_metadatum('parts_directory', True)
        if bool(paper_size):
            directory.add_metadatum('paper_size', paper_size)
        if not orientation == 'portrait':
            directory.add_metadatum('orientation', orientation)
        if bool(suffix):
            directory.add_metadatum('catalog_number_suffix', suffix)
        self.collect_segment_lys(directory)
        self.generate_stylesheet(directory)
        total_parts = len(part_name_pairs)
        for i, pair in enumerate(part_name_pairs):
            part_name, part_abbreviation = pair
            part_number = i + 1
            price = f'{part_abbreviation} ({part_number}/{total_parts})'
            dash_part_name = abjad.String(part_name).to_dash_case()
            path = directory(f'{dash_part_name}-back-cover.tex')
            self._generate_back_cover(path, price=price),
            path = directory(f'{dash_part_name}-front-cover.tex')
            words = abjad.String(dash_part_name).delimit_words()
            forces_tagline = f"{' '.join(words)} part"
            self._generate_front_cover(path, forces_tagline=forces_tagline)
            name = 'layout.py'
            target_name = f'{dash_part_name}_{name}'
            target_name = abjad.String(target_name).to_snake_case()
            self._copy_boilerplate(directory, name, target_name=target_name)
            path = directory(target_name)
            self._generate_music(
                path,
                forces_tagline=forces_tagline,
                keep_with_tag=part_name,
                silent=True,
                )
            self._generate_document(
                directory,
                name='part.tex',
                prefix=dash_part_name,
                )
            self._generate_preface(directory, prefix=dash_part_name)

    @Command(
        'cv',
        description='clipboard - paste',
        external_directories=True,
        menu_section='clipboard',
        score_package_paths=True,
        scores_directory=True,
        )
    def paste_from_clipboard(self, directory):
        r'''Pastes from clipboard.

        Returns none.
        '''
        if not bool(self.clipboard):
            self.io.display('showing empty clipboard ...')
            return
        self.io.display('pasting from clipboard ...')
        for i, source in enumerate(self.clipboard[:]):
            self.io.display(f'    {source.trim()} ...')
            target = directory(source.name)
            self.io.display(f'    {target.trim()} ...')
            if target.exists():
                self.io.display(['', f'existing {target.trim()} ...'])
                name = self.io.get('enter new name')
                if self.is_navigation(name):
                    return
                if not bool(name):
                    continue
                target = target.with_name(name)
                if target.exists():
                    self.io.display(f'existing {target.trim()} ...')
                    return
                self.io.display(f'    {source.trim()} ...')
                self.io.display(f'    {target.trim()} ...')
            if source.is_dir():
                shutil.copytree(str(source), str(target))
            else:
                shutil.copy(str(source), str(target))
            if i < len(self.clipboard) - 1:
                self.io.display('')

    @Command(
        '++',
        description='all - pytest',
        external_directories=True,
        menu_section='all',
        score_package_paths=True,
        scores_directory=True,
        )
    def pytest_all(self, directory, pattern=None):
        r'''Pytests all.

        Returns none.
        '''
        files, strings = directory._find_pytest_files(force=True)
        files = self._match_files(files, strings, pattern, '++')
        self._run_pytest(files)

    @Command(
        'q',
        description='go - quit',
        external_directories=True,
        menu_section='go',
        score_package_paths=True,
        scores_directory=True,
        )
    def quit(self):
        r'''Quits Abjad IDE.

        Returns none.
        '''
        self._navigation = 'q'

    @Command(
        'rm',
        description='path - remove',
        external_directories=True,
        menu_section='path',
        score_package_path_blacklist=('contents',),
        score_package_paths=True,
        scores_directory=True,
        )
    def remove(self, directory):
        r'''Removes assets in `directory`.

        Returns none.
        '''
        paths = self._select_paths(directory, infinitive='to remove')
        if self.is_navigation(paths):
            return
        assert isinstance(paths, list)
        count = len(paths)
        if count == 1:
            self.io.display(f'will remove {paths[0].trim()} ...')
        else:
            self.io.display('will remove ...')
            for path in paths:
                self.io.display(f'    {path.trim()}')
        if count == 1:
            string = 'remove'
        else:
            string = f'remove {count}'
        result = self.io.get(f"type {string!r} to proceed")
        if self.is_navigation(result):
            return
        if result != string:
            return
        for path in paths:
            self.io.display(f'removing {path.trim()} ...')
            path.remove()

    @Command(
        'ren',
        description='path - rename',
        external_directories=True,
        menu_section='path',
        score_package_path_blacklist=('contents',),
        score_package_paths=True,
        scores_directory=True,
        )
    def rename(self, directory):
        r'''Renames asset.

        Returns none.
        '''
        paths = self._select_paths(directory, infinitive='to rename')
        if self.is_navigation(paths):
            return
        assert isinstance(paths, list), repr(paths)
        for source in paths:
            self.io.display(f'renaming {source.trim()} ...')
            name = self.io.get('new name')
            if self.is_navigation(name):
                return
            name_ = directory.coerce(name, suffix=source.suffix)
            target = source.parent(name_)
            if target.exists():
                self.io.display(f'existing {target.trim()!r} ...')
                return
            self.io.display('renaming ...')
            self.io.display(f' FROM: {source.trim()}')
            self.io.display(f'   TO: {target.trim()}')
            response = self.io.get('ok?')
            if self.is_navigation(response):
                return
            if response != 'y':
                return
            shutil.move(str(source), str(target))
            if target.is_wrapper():
                assert target(source.name).is_dir()
                shutil.move(
                    str(target(source.name)),
                    str(target.contents),
                    )
                target.contents.add_metadatum('title', name)
            if not target.is_dir():
                return
            for path in sorted(target.glob('*.py')):
                self._replace_in_file(
                    path,
                    source.name,
                    target.name,
                    whole_words=True,
                    )

    @Command(
        'rp',
        description='text - replace',
        external_directories=True,
        menu_section='text',
        score_package_paths=True,
        scores_directory=True,
        )
    def replace(self, directory):
        r'''Replaces search string with replace string.

        Returns none.
        '''
        search_string = self.io.get('enter search string')
        if self.is_navigation(search_string):
            return
        replace_string = self.io.get('enter replace string')
        if self.is_navigation(replace_string):
            return
        complete_words = False
        response = self.io.get('complete words only?')
        if self.is_navigation(response):
            return
        if response != 'y':
            complete_words = True
        if directory == directory.scores:
            pass
        elif directory.is_score_package_path():
            directory = directory.wrapper
        lines = self._replace_in_tree(
            directory,
            search_string,
            replace_string,
            complete_words,
            )
        self.io.display(lines, raw=True)

    @Command(
        'sr',
        description='text - search',
        external_directories=True,
        menu_section='text',
        score_package_paths=True,
        scores_directory=True,
        )
    def search(self, directory):
        r'''Searches for expression

        Delegates to ack if ack is found.

        Delegates to grep is ack is not found.

        Returns none.
        '''
        executables = abjad.IOManager.find_executable('ack')
        if not executables:
            executables = abjad.IOManager.find_executable('grep')
        executables = [Path(_) for _ in executables]
        if not executables:
            self.io.display('can not find ack.')
            self.io.display('can not find grep.')
            return
        assert 1 <= len(executables)
        executable = None
        for path in executables:
            if path.is_file():
                executable = path
        if executable is None:
            self.io.display('can not find ack.')
            self.io.display('can not find grep.')
            return
        search_string = self.io.get('enter search string')
        if self.is_navigation(search_string):
            return
        if executable.name == 'ack':
            command = r'{!s} --ignore-dir=_docs {} --type=python'
            command = command.format(executable, search_string)
        elif executable.name == 'grep':
            command = rf'{executable!s} -r {search_string!r} *'
        if directory.wrapper is not None:
            directory = directory.wrapper
        with self.change(directory):
            lines = abjad.IOManager.run_command(command)
            self.io.display(lines, raw=True)

    @Command(
        'cs',
        description='clipboard - show',
        external_directories=True,
        menu_section='clipboard',
        score_package_paths=True,
        scores_directory=True,
        )
    def show_clipboard(self, directory):
        r'''Shows clipboard.

        Returns none.
        '''
        if not bool(self.clipboard):
            self.io.display('showing empty clipboard ...')
            return
        self.io.display('showing clipboard ...')
        for path in self.clipboard:
            self.io.display(path.trim(), raw=True)

    @Command(
        '?',
        description='show - help',
        external_directories=True,
        menu_section='show',
        score_package_paths=True,
        scores_directory=True,
        )
    def show_help(self):
        r'''Shows help.

        Returns none.
        '''
        pass

    @Command(
        '^',
        description='smart - doctest',
        external_directories=True,
        menu_section='smart',
        score_package_paths=True,
        scores_directory=True,
        )
    def smart_doctest(self, directory, pattern, menu_paths):
        r'''Smart doctest.

        Returns none.
        '''
        address, file_ = self._match_smart_file(
            directory,
            pattern,
            menu_paths,
            '^',
            Path._find_doctest_files,
            'definition.py',
            )
        if file_:
            self.io.display(f'matching {address!r} to {file_.trim()} ...')
            self._run_doctest([file_])

    @Command(
        '@',
        description='smart - edit',
        external_directories=True,
        menu_section='smart',
        score_package_paths=True,
        scores_directory=True,
        )
    def smart_edit(self, directory, pattern, menu_paths):
        r'''Smart edit.

        Returns none.
        '''
        address, file_ = self._match_smart_file(
            directory,
            pattern,
            menu_paths,
            '@',
            Path._find_editable_files,
            'definition.py',
            )
        if file_:
            self._open_files([file_])

    @Command(
        '*',
        description='smart - pdf',
        external_directories=True,
        menu_section='smart',
        score_package_paths=True,
        scores_directory=True,
        )
    def smart_pdf(self, directory, pattern, menu_paths):
        r'''Smart PDF.

        Returns none.
        '''
        address, file_ = self._match_smart_file(
            directory,
            pattern,
            menu_paths,
            '*',
            Path._find_pdfs,
            'illustration.pdf',
            )
        if file_:
            self._open_files([file_])

    @Command(
        '+',
        description='smart - pytest',
        external_directories=True,
        menu_section='smart',
        score_package_paths=True,
        scores_directory=True,
        )
    def smart_pytest(self, directory, pattern, menu_paths):
        r'''Smart pytest.

        Returns none.
        '''
        address, file_ = self._match_smart_file(
            directory,
            pattern,
            menu_paths,
            '+',
            Path._find_pytest_files,
            None,
            )
        if file_:
            self.io.display(f'matching {address!r} to {file_.trim()} ...')
            self._run_pytest([file_])

    @Command(
        'bct',
        description='back cover - trash',
        menu_section='back cover',
        score_package_paths=('_segments', 'build',),
        )
    def trash_back_cover(self, directory):
        r'''Trashes back cover.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'back-cover.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'trash')
        if paths:
            self._trash_files(paths)

    @Command(
        'dft',
        description='definition - trash',
        menu_section='definition',
        score_package_paths=('material', 'segment'),
        )
    def trash_definition(self, directory):
        r'''Trashes definition.

        Returns none.
        '''
        assert directory.is_material_or_segment()
        path = directory('definition.py')
        self._trash_files(path)

    @Command(
        'dft*',
        description='definitions - trash',
        menu_section='definitions',
        score_package_paths=('materials', 'segments'),
        )
    def trash_definitions(self, directory):
        r'''Trashes definitions.

        Returns none.
        '''
        assert directory.is_materials_or_segments()
        for path in directory.list_paths():
            path /= 'definition.py'
            self._trash_files(path)

    @Command(
        'fct',
        description='front cover - trash',
        menu_section='front cover',
        score_package_paths=('_segments', 'build',),
        )
    def trash_front_cover(self, directory):
        r'''Trashes front cover (source).

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'front-cover.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'trash')
        if paths:
            self._trash_files(paths)

    @Command(
        'lyt',
        description='ly - trash',
        menu_section='ly',
        score_package_paths=('material', 'segment',),
        )
    def trash_ly(self, directory):
        r'''Trashes LilyPond file.

        Returns none.
        '''
        assert directory.is_material_or_segment()
        path = directory('illustration.ly')
        self._trash_files(path)

    @Command(
        'lyt*',
        description='lys - trash',
        menu_section='lys',
        score_package_paths=('materials', 'segments',),
        )
    def trash_lys(self, directory):
        r'''Trashes LilyPond files.

        Returns none.
        '''
        assert directory.is_materials_or_segments()
        for path in directory.list_paths():
            path /= 'illustration.ly'
            self._trash_files(path)

    @Command(
        'mt',
        description='music - trash',
        menu_section='music',
        score_package_paths=('_segments', 'build',),
        )
    def trash_music(self, directory):
        r'''Trashes music (source).

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'music.ly'
        paths = self._match_paths_in_buildspace(directory, name, 'trash')
        if paths:
            self._trash_files(paths)

    @Command(
        'at',
        description='part - trash',
        menu_section='parts',
        score_package_paths=('parts',),
        )
    def trash_part(self, directory):
        r'''Trashes part (source).

        Returns none.
        '''
        assert directory.is_parts()
        name = 'part.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'trash')
        if paths:
            self._trash_files(paths)

    @Command(
        'pdft',
        description='pdf - trash',
        menu_section='pdf',
        score_package_paths=('material', 'segment',),
        )
    def trash_pdf(self, directory):
        r'''Trashes PDF.

        Returns none.
        '''
        assert directory.is_material_or_segment()
        path = directory('illustration.pdf')
        self._trash_files(path)

    @Command(
        'pdft*',
        description='pdfs - trash',
        menu_section='pdfs',
        score_package_paths=('materials', 'segments',),
        )
    def trash_pdfs(self, directory):
        r'''Trashes PDFs.

        Returns none.
        '''
        assert directory.is_materials_or_segments()
        for path in directory.list_paths():
            path /= 'illustration.pdf'
            self._trash_files(path)

    @Command(
        'pt',
        description='preface - trash',
        menu_section='preface',
        score_package_paths=('_segments', 'build',),
        )
    def trash_preface(self, directory):
        r'''Trashes preface (source).

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        name = 'preface.tex'
        paths = self._match_paths_in_buildspace(directory, name, 'trash')
        if paths:
            self._trash_files(paths)

    @Command(
        'rt',
        description='score - trash',
        menu_section='score',
        score_package_path_blacklist=('parts',),
        score_package_paths=('_segments', 'build',),
        )
    def trash_score(self, directory):
        r'''Trashes score (source).

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        path = directory('score.tex')
        self._trash_files(path)

    @Command(
        'yt',
        description='stylesheet - trash',
        menu_section='stylesheet',
        score_package_paths=('_segments', 'build',),
        )
    def trash_stylesheet(self, directory):
        r'''Trashes stylesheet.

        Returns none.
        '''
        assert directory.is__segments() or directory.is_build()
        directory = directory.build
        path = directory('stylesheet.ily')
        self._trash_files(path)
