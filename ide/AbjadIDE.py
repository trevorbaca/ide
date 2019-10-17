import abjad
import baca
import collections
import datetime
import doctest
import importlib
import inspect
import io
import os
import pathlib
import platform
import re
import roman  # type: ignore
import shutil
import subprocess
import typing
from .Command import Command
from .Configuration import Configuration
from .Interaction import Interaction
from .IO import IO
from .Menu import Menu
from .MenuSection import MenuSection
from .Path import Path
from .Response import Response


class AbjadIDE(object):
    """
    Abjad IDE.

    ..  container:: example

        >>> ide.AbjadIDE()
        AbjadIDE()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_aliases",
        "_clipboard",
        "_commands",
        "_current_directory",
        "_example",
        "_io",
        "_navigation",
        "_navigations",
        "_previous_directory",
        "_redraw",
        "_test",
    )

    configuration = Configuration()

    # lilypond.org/doc/v2.19/Documentation/notation/predefined-paper-sizes
    paper_size_to_paper_dimensions = {
        "a3": "297 x 420 mm",
        "a4": "210 x 297 mm",
        "arch a": "9 x 12 in",
        "arch b": "12 x 18 in",
        "arch c": "18 x 24 in",
        "arch d": "24 x 36 in",
        "arch e": "36 x 48 in",
        "legal": "8.5 x 14 in",
        "ledger": "17 x 11 in",
        "letter": "8.5 x 11 in",
        "tabloid": "11 x 17 in",
    }

    known_paper_sizes = list(paper_size_to_paper_dimensions.keys())

    ### INITIALIZER ###

    def __init__(self, example: bool = None, test: bool = None) -> None:
        self._aliases = abjad.OrderedDict(self.configuration.aliases)
        self._clipboard: typing.List[str] = []
        self._current_directory = None
        self._example = example
        self._navigation: typing.Optional[str] = None
        self._navigations: abjad.OrderedDict = abjad.OrderedDict()
        self._previous_directory = None
        self._redraw: typing.Optional[bool] = None
        self._test = test
        self._io = IO()
        self._check_test_scores_directory(example or test)
        self._cache_commands()

    ### SPECIAL METHODS ###

    def __call__(self, string=None) -> None:
        """
        Calls IDE on ``string``.
        """
        if self.test and not string.endswith("q"):
            raise Exception(f"Test input must end with 'q': {string!r}.")
        AbjadIDE.__init__(self, example=self.example, test=self.test)
        self.io.pending_input(string)
        scores = self._get_scores_directory()
        self._manage_directory(scores)
        self.io.transcript.trim()
        last_line = self.io.transcript.lines[-1]
        assert last_line == "", repr(last_line)
        abjad.IOManager.clear_terminal()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _activate_part_specific_tags(self, path):
        parts_directory = path.parent.parent
        assert parts_directory.is_parts()
        self.run(abjad.Job.handle_edition_tags(parts_directory))
        part_identifier = path._parse_part_identifier()
        if part_identifier is None:
            self.io.display(f"no part identifier found in {path.name} ...")
        else:
            parts_directory_name = abjad.String(parts_directory.name)
            parts_directory_name = parts_directory_name.to_shout_case()
            tag = f"+{parts_directory_name}_{part_identifier}"
            self.activate(parts_directory, tag, message_zero=True)
        self.uncolor_persistent_indicators(parts_directory)

    def _cache_commands(self):
        commands = abjad.OrderedDict()
        for name in dir(self):
            if name.startswith("_"):
                continue
            try:
                command = getattr(self, name)
            except AttributeError:
                command = None
            if not inspect.ismethod(command):
                continue
            if not hasattr(command, "command_name"):
                continue
            commands[command.command_name] = command
        self._commands = commands

    def _check_out_paths(self, paths):
        assert isinstance(paths, collections.abc.Iterable), repr(paths)
        for path in paths:
            root = path._get_repository_root()
            if not root:
                self.io.display(f"missing {path.trim()} repository ...")
                return
            with self.change(root):
                command = f"git checkout {path}"
                self.io.display(f"Running {command} ...")
                lines = abjad.IOManager.run_command(command)
                self.io.display(lines, raw=True)

    def _check_test_scores_directory(self, check=False):
        if not check:
            return
        directory = self.configuration.test_scores_directory
        names = [_.name for _ in directory.iterdir()]
        if "red_score" not in names:
            message = f"Empty test scores directory {directory} ..."
            raise Exception(message)

    def _collect_segments(self, directory):
        paths = directory.segments._list_paths()
        names = [_.name for _ in paths]
        sources, targets = [], []
        for name in names:
            source = directory.segments / name / "illustration.ly"
            if not source.is_file():
                continue
            target = "segment-" + name.replace("_", "-") + ".ly"
            target = directory._segments / target
            sources.append(source)
            targets.append(target)
        if not directory.builds.is_dir():
            directory.builds.mkdir()
        return zip(sources, targets)

    def _copy_boilerplate(
        self, directory, source_name, indent=0, target_name=None, values=None
    ):
        target_name = target_name or source_name
        target = directory / target_name
        if target.exists():
            self.io.display(f"removing {target.trim()} ...", indent=indent)
        self.io.display(f"writing {target.trim()} ...", indent=indent)
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

    def _display_lilypond_log_errors(self, log=None):
        if log is None:
            log = abjad.abjad_configuration.lilypond_log_file_path
        log = Path(log)
        with log.open() as file_pointer:
            lines = file_pointer.readlines()
        for line in lines:
            if (
                "fatal" in line
                or ("error" in line and "programming error" not in line)
                or "failed" in line
            ):
                self.io.display("ERROR IN LILYPOND LOG FILE ...")
                break

    @staticmethod
    def _filter_files(files, strings, pattern):
        if isinstance(pattern, str):
            indices = abjad.String.match_strings(strings, pattern)
            files = abjad.Sequence(files).retain(indices)
        return files

    def _generate_back_cover_tex(self, path, price=None):
        assert path.build.exists(), repr((path, path.build))
        name = "back-cover.tex"
        assert path.name.endswith(name)
        directory = path.build
        local_template = directory._assets / name
        if local_template.is_file():
            self.io.display(f"removing {path.trim()} ...")
            path.remove()
            self.io.display(f"copying {local_template.trim()} ...")
            self.io.display(f"writing {path.trim()} ...")
            shutil.copyfile(str(local_template), str(path))
            if price is not None:
                text = path.read_text()
                if "_PRICE" in text:
                    text = text.replace("_PRICE", price)
                path.write_text(text)
            return
        values = {}
        string = "catalog_number"
        catalog_number = directory.contents.get_metadatum(string, r"\null")
        if path.build.is_part():
            metadata = path.build.parent.get_metadata()
        else:
            metadata = path.build.get_metadata()
        if catalog_number:
            suffix = metadata.get("catalog_number_suffix")
            if suffix:
                catalog_number = f"{catalog_number} / {suffix}"
        values["catalog_number"] = catalog_number
        composer_website = abjad.abjad_configuration.composer_website or ""
        if self.test or self.example:
            composer_website = "www.composer-website.com"
        values["composer_website"] = composer_website
        if price is None:
            price = metadata.get("price", r"\null")
            if "$" in price and r"\$" not in price:
                price = price.replace("$", r"\$")
        values["price"] = price
        paper_size = metadata.get("paper_size", "letter")
        if paper_size not in self.known_paper_sizes:
            self.io.display(f"unknown paper size {paper_size} ...")
            return
        orientation = metadata.get("orientation")
        dimensions = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = dimensions
        paper_size = f"{{{width}{unit}, {height}{unit}}}"
        values["paper_size"] = paper_size
        target_name = path.name
        self._copy_boilerplate(
            directory, "back-cover.tex", target_name=target_name, values=values
        )

    def _generate_document(self, path):
        directory = path.parent
        values = {}
        paper_size = directory.get_metadatum("paper_size", "letter")
        orientation = directory.get_metadatum("orientation")
        paper_size = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f"{{{width}{unit}, {height}{unit}}}"
        values["paper_size"] = paper_size
        if path.name.endswith("score.tex"):
            name = "score.tex"
        elif path.name.endswith("part.tex"):
            name = "part.tex"
            dashed_part_name = path.name.strip("-part.tex")
            values["dashed_part_name"] = dashed_part_name
        else:
            raise ValueError(path.name)
        self._copy_boilerplate(
            directory, name, target_name=path.name, values=values
        )

    def _generate_front_cover_tex(self, path, forces_tagline=None):
        assert path.build.exists(), repr(path)
        directory = path.build
        name = "front-cover.tex"
        local_template = directory._assets / name
        if local_template.is_file():
            self.io.display(f"removing {path.trim()} ...")
            path.remove()
            self.io.display(f"copying {local_template.trim()} ...")
            self.io.display(f"writing {path.trim()} ...")
            shutil.copyfile(str(local_template), str(path))
            if forces_tagline is not None:
                text = path.read_text()
                if "_FORCES_TAGLINE" in text:
                    text = text.replace("_FORCES_TAGLINE", forces_tagline)
                path.write_text(text)
            return
        values = {}
        score_title = directory.contents.get_title(year=False)
        score_title = score_title.upper()
        values["score_title"] = score_title
        if not forces_tagline:
            string = "forces_tagline"
            forces_tagline = directory.contents.get_metadatum(string, "")
        if forces_tagline:
            forces_tagline = forces_tagline.replace("\\", "")
        values["forces_tagline"] = forces_tagline
        year = directory.contents.get_metadatum("year", "")
        values["year"] = str(year)
        composer = abjad.abjad_configuration.composer_uppercase_name
        if self.test or self.example:
            composer = "COMPOSER"
        values["composer"] = str(composer)
        paper_size = directory.get_metadatum("paper_size", "letter")
        orientation = directory.get_metadatum("orientation")
        paper_size = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f"{{{width}{unit}, {height}{unit}}}"
        values["paper_size"] = paper_size
        target_name = None
        target_name = path
        self._copy_boilerplate(
            directory, name, target_name=target_name, values=values
        )

    def _generate_part_music_ly(
        self,
        path,
        dashed_part_name=None,
        forces_tagline=None,
        indent=0,
        keep_with_tag=None,
        part=None,
        part_subtitle=None,
        silent=None,
    ):
        assert path.build.exists(), repr(path)
        if path.exists():
            self.io.display(f"removing {path.trim()} ...", indent=indent)
            path.remove()
        segments = path.segments.list_paths()
        if not silent:
            if segments:
                view = path.segments.get_metadatum("view")
                if bool(view):
                    self.io.display(
                        f"examining segments in view order ...", indent=indent
                    )
            else:
                self.io.display("no segments found ...", indent=indent)
            for segment in segments:
                if not segment.is_segment():
                    continue
                self.io.display(
                    f"examining {segment.trim()} ...", indent=indent
                )
        names = [_.stem.replace("_", "-") for _ in segments]
        boilerplate = "part-music.ly"
        self._copy_boilerplate(
            path.build, boilerplate, indent=indent, target_name=path.name
        )
        lines, ily_lines = [], []
        for i, name in enumerate(names):
            name = "segment-" + name + ".ly"
            ly = path.build._segments / name
            if ly.is_file():
                line = rf'\include "../_segments/{name}"'
            else:
                line = rf'%\include "../_segments/{name}"'
            ily_lines.append(line.replace(".ly", ".ily"))
            if 0 < i:
                line = 8 * " " + line
            lines.append(line)
        if lines:
            segment_ily_include_statements = "\n".join(ily_lines)
        else:
            segment_ily_include_statements = ""
        language_token = abjad.LilyPondLanguageToken()
        lilypond_language_directive = format(language_token)
        version_token = abjad.LilyPondVersionToken()
        lilypond_version_directive = format(version_token)
        annotated_title = path.contents.get_title(year=True)
        if annotated_title:
            score_title = annotated_title
        else:
            score_title = path.contents.get_title(year=False)
        score_title_without_year = path.contents.get_title(year=False)
        if forces_tagline is None:
            string = "forces_tagline"
            forces_tagline = path.contents.get_metadatum(string, "")
        if forces_tagline:
            forces_tagline = forces_tagline.replace("\\", "")
        assert path.is_file(), repr(path)
        template = path.read_text()
        if path.parent.is_part():
            identifiers = path.global_skip_identifiers()
            identifiers = ["\\" + _ for _ in identifiers]
            newline = "\n" + 24 * " "
            global_skip_identifiers = newline.join(identifiers)
            if self.test:
                defaults_include_statement = ""
                segment_ly_include_statements = r"\FOO"
            else:
                dictionary = self._make_container_to_part_assignment(path)
                identifiers = path.part_to_identifiers(part, dictionary)
                if isinstance(identifiers, str):
                    self.io.display(identifiers + " ...")
                    self.io.display(f"removing {path.trim()} ...")
                    path.remove()
                    return
                identifiers = ["\\" + _ for _ in identifiers]
                newline = "\n" + 24 * " "
                segment_ly_include_statements = newline.join(identifiers)
            template = template.format(
                dashed_part_name=dashed_part_name,
                forces_tagline=forces_tagline,
                global_skip_identifiers=global_skip_identifiers,
                lilypond_language_directive=lilypond_language_directive,
                lilypond_version_directive=lilypond_version_directive,
                part_identifier=repr(part.identifier),
                part_subtitle=part_subtitle,
                score_title=score_title,
                score_title_without_year=score_title_without_year,
                segment_ily_include_statements=segment_ily_include_statements,
                segment_ly_include_statements=segment_ly_include_statements,
            )
        path.write_text(template)

    def _generate_part_tex(self, path, dashed_part_name):
        assert path.build.exists(), repr(path)
        assert path.build.is_parts() or path.build.is_part(), repr(path)
        directory = path.build
        name = "part.tex"
        local_template = directory._assets / name
        if local_template.is_file():
            self.io.display(f"removing {path.trim()} ...")
            path.remove()
            self.io.display(f"copying {local_template.trim()} ...")
            self.io.display(f"writing {path.trim()} ...")
            shutil.copyfile(str(local_template), str(path))
            return
        values = {}
        values["dashed_part_name"] = dashed_part_name
        if path.build.is_part():
            metadata = path.build.parent.get_metadata()
        else:
            metadata = path.build.get_metadata()
        paper_size = metadata.get("paper_size", "letter")
        orientation = metadata.get("orientation")
        paper_size = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f"{{{width}{unit}, {height}{unit}}}"
        values["paper_size"] = paper_size
        target_name = path.name
        self._copy_boilerplate(
            directory, name, target_name=target_name, values=values
        )

    def _generate_preface_tex(self, path):
        assert path.build.exists(), repr(path)
        directory = path.build
        name = "preface.tex"
        local_template = directory._assets / name
        if local_template.is_file():
            self.io.display(f"removing {path.trim()} ...")
            path.remove()
            self.io.display(f"copying {local_template.trim()} ...")
            self.io.display(f"writing {path.trim()} ...")
            shutil.copyfile(str(local_template), str(path))
            return
        values = {}
        if path.build.is_part():
            metadata = path.build.parent.get_metadata()
        else:
            metadata = path.build.get_metadata()
        paper_size = metadata.get("paper_size", "letter")
        orientation = metadata.get("orientation")
        paper_size = self._to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f"{{{width}{unit}, {height}{unit}}}"
        values["paper_size"] = paper_size
        if path.build.is_part():
            name = "part-preface.tex"
            target_name = f"{path.build.name}-preface.tex"
        else:
            name = "score-preface.tex"
            target_name = path.name
        self._copy_boilerplate(
            directory, name, target_name=target_name, values=values
        )

    def _generate_score_music_ly(
        self, path, forces_tagline=None, indent=0, silent=None
    ):
        assert path.build.exists(), repr(path)
        if path.exists():
            self.io.display(f"removing {path.trim()} ...", indent=indent)
            path.remove()
        segments = path.segments.list_paths()
        if not silent:
            if segments:
                view = path.segments.get_metadatum("view")
                if bool(view):
                    self.io.display(
                        f"examining segments in view order ...", indent=indent
                    )
            else:
                self.io.display("no segments found ...", indent=indent)
            for segment in segments:
                if not segment.is_segment():
                    continue
                self.io.display(
                    f"examining {segment.trim()} ...", indent=indent
                )
        names = [_.stem.replace("_", "-") for _ in segments]
        score_skeleton = path.score_skeleton()
        if score_skeleton is None:
            boilerplate = "score-music.ly"
        else:
            boilerplate = "full-score-music.ly"
            text = format(score_skeleton)
            lines = text.split("\n")
            lines = [lines[0]] + [8 * " " + _ for _ in lines[1:]]
            score_skeleton = "\n".join(lines)
        self._copy_boilerplate(
            path.build, boilerplate, indent=indent, target_name=path.name
        )
        lines, ily_lines = [], []
        for i, name in enumerate(names):
            name = "segment-" + name + ".ly"
            ly = path.build._segments / name
            if ly.is_file():
                line = rf'\include "_segments/{name}"'
            else:
                line = rf'%\include "_segments/{name}"'
            ily_lines.append(line.replace(".ly", ".ily"))
            if 0 < i:
                line = 8 * " " + line
            lines.append(line)
        if lines:
            segment_ly_include_statements = "\n".join(lines)
            segment_ily_include_statements = "\n".join(ily_lines)
        else:
            segment_ly_include_statements = ""
            segment_ily_include_statements = ""
        language_token = abjad.LilyPondLanguageToken()
        lilypond_language_directive = format(language_token)
        version_token = abjad.LilyPondVersionToken()
        lilypond_version_directive = format(version_token)
        annotated_title = path.contents.get_title(year=True)
        if annotated_title:
            score_title = annotated_title
        else:
            score_title = path.contents.get_title(year=False)
        score_title_without_year = path.contents.get_title(year=False)
        if forces_tagline is None:
            string = "forces_tagline"
            forces_tagline = path.contents.get_metadatum(string, "")
        if forces_tagline:
            forces_tagline = forces_tagline.replace("\\", "")
        assert path.is_file(), repr(path)
        template = path.read_text()
        if boilerplate == "score-music.ly":
            assert path.parent.is_score_build()
            template = template.format(
                forces_tagline=forces_tagline,
                lilypond_language_directive=lilypond_language_directive,
                lilypond_version_directive=lilypond_version_directive,
                score_title=score_title,
                segment_ily_include_statements=segment_ily_include_statements,
                segment_ly_include_statements=segment_ly_include_statements,
            )
        elif boilerplate == "full-score-music.ly":
            assert path.parent.is_score_build()
            template = template.format(
                forces_tagline=forces_tagline,
                lilypond_language_directive=lilypond_language_directive,
                lilypond_version_directive=lilypond_version_directive,
                score_title=score_title,
                segment_ily_include_statements=segment_ily_include_statements,
                score_skeleton=score_skeleton,
            )
        path.write_text(template)

    def _get_dimensions(self):
        dimensions = None
        if self.test is True:
            dimensions = False
        if isinstance(self.test, str) and self.test.startswith("dimensions"):
            dimensions = eval(self.test.strip("dimensions="))
        return dimensions

    def _get_doctest_globs(self, external_modules=()):
        globs = {}
        abjad = importlib.import_module("abjad")
        globs["abjad"] = abjad
        globs.update(abjad.__dict__)
        external_modules = external_modules or ""
        external_modules = external_modules.split(",")
        for name in external_modules:
            try:
                module = importlib.import_module(name)
                globs[name] = module
            except ImportError:
                pass
        try:
            ide_module = importlib.import_module("ide")
            globs["ide"] = ide_module
        except (AttributeError, ImportError):
            pass
        return globs

    def _get_score_names(self):
        scores = self._get_scores_directory()
        names = [_.name for _ in scores.list_paths()]
        return names

    def _get_scores_directory(self):
        if self.test or self.example:
            return self.configuration.test_scores_directory
        return self.configuration.composer_scores_directory

    def _handle_address(self, directory, response):
        assert response.prefix, repr(response)
        if response.prefix == "@":
            self.smart_edit(directory, response.pattern, response.payload)
        elif response.prefix == "@@":
            self.edit_all(directory, response.pattern)
        elif response.prefix == "%":
            self.go_to_directory(directory, response.pattern, response.payload)
        elif response.prefix == "%%":
            self.go_to_directory(directory, response.string[1:])
        elif response.prefix == "^":
            self.smart_doctest(directory, response.pattern, response.payload)
        elif response.prefix == "^^":
            self.doctest_all(directory, response.pattern)
        elif response.prefix == "+":
            self.smart_pytest(directory, response.pattern, response.payload)
        elif response.prefix == "++":
            self.pytest_all(directory, response.pattern)
        elif response.prefix == "*":
            self.smart_pdf(directory, response.pattern, response.payload)
        elif response.prefix == "**":
            self.open_all_pdfs(directory, response.pattern)
        else:
            raise ValueEror(response.prefix)

    def _interpret_file(self, path):
        path = Path(path)
        if not path.exists():
            message = f"missing {path} ..."
            self.display(message)
            return False
        if path.suffix == ".py":
            command = f"python {path}"
        elif path.suffix == ".ly":
            command = f"lilypond -dno-point-and-click {path}"
        else:
            message = f"can not interpret {path}."
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
                line = line.decode("utf-8")
                print(line, end="")
                string_buffer.write(line)
            process.wait()
            stdout_lines = string_buffer.getvalue().splitlines()
            stderr_lines = abjad.IOManager._read_from_pipe(process.stderr)
            stderr_lines = stderr_lines.splitlines()
        exit_code = process.returncode
        if path.suffix == ".ly":
            log = directory / ".log"
            self._display_lilypond_log_errors(log=log)
        return stdout_lines, stderr_lines, exit_code

    def _interpret_tex_file(self, tex):
        if not tex.is_file():
            self.io.display(f"can not find {tex.trim()} ...")
            return
        pdf = tex.with_suffix(".pdf")
        if pdf.exists():
            self.io.display(f"removing {pdf.trim()} ...")
            pdf.remove()
        self.io.display(f"interpreting {tex.trim()} ...")
        if not tex.is_file():
            return
        executables = abjad.IOManager.find_executable("xelatex")
        executables = [Path(_) for _ in executables]
        if not executables:
            executable_name = "pdflatex"
            fancy_executable_name = "LaTeX"
        else:
            executable_name = "xelatex"
            fancy_executable_name = "XeTeX"
        pdf_path = tex.parent / (str(tex.stem) + ".pdf")
        log = self.configuration.latex_log_file_path
        command = f"date > {log};"
        command += f" {executable_name} -halt-on-error"
        command += f" -interaction=nonstopmode"
        command += f" --jobname={tex.stem}"
        command += f" -output-directory={tex.parent} {tex}"
        command += f" >> {log} 2>&1"
        command_called_twice = f"{command}; {command}"
        with self.change(tex.parent):
            abjad.IOManager.spawn_subprocess(command_called_twice)
            for path in sorted(tex.parent.glob("*.aux")):
                path.remove()
            for path in sorted(tex.parent.glob("*.log")):
                path.remove()
        if pdf.is_file():
            self.io.display(f"found {pdf.trim()} ...")
        else:
            self.io.display("ERROR IN LATEX LOG FILE ...")
            log_file = self.configuration.latex_log_file_path
            with log_file.open() as file_pointer:
                lines = [_.strip("\n") for _ in file_pointer.readlines()]
            self.io.display(lines)

    def _interpret_tex_files_ending_with(self, directory, name):
        paths = directory.get_files_ending_with(name)
        if not paths:
            self.io.display(f"no files ending in *{name} ...")
            return
        self.io.display("will interpret ...")
        for path in paths:
            self.io.display(path.trim(), raw=True)
        self.io.display("")
        ok = self.io.get("ok?")
        if ok and self.is_navigation(ok):
            return
        if ok != "y":
            return
        for source in paths:
            target = source.with_suffix(".pdf")
            self._interpret_tex_file(source)

    @staticmethod
    def _make__assets_directory(directory):
        if directory._assets.exists():
            return
        directory._assets.mkdir()
        gitignore = directory._assets / ".gitignore"
        gitignore.write_text("")

    @staticmethod
    def _make__segments_directory(directory):
        if directory._segments.exists():
            return
        directory._segments.mkdir()
        gitignore = directory._segments / ".gitignore"
        gitignore.write_text("*.ily")
        gitignore.write_text("*.ly")

    def _make_command_sections(self, directory):
        commands = []
        for command in self.commands.values():
            blacklist = command.score_package_path_blacklist
            if directory.is_scores() and command.scores_directory:
                commands.append(command)
            elif (
                directory.is_external()
                and not directory.is_scores()
                and command.external_directories
            ):
                commands.append(command)
            elif (
                directory.is_score_package_path()
                and directory.is_prototype(command.score_package_paths)
                and not directory.is_prototype(blacklist)
            ):
                commands.append(command)
        entries_by_section = {}
        navigations = abjad.OrderedDict()
        navigation_sections = ("go", "directory")
        for command in commands:
            if command.menu_section not in entries_by_section:
                entries_by_section[command.menu_section] = []
            entries = entries_by_section[command.menu_section]
            display = f"{command.description} ({command.command_name})"
            entry = (display, command.command_name)
            entries.append(entry)
            if command.menu_section in navigation_sections:
                name = command.command_name
                navigations[name] = command
        del navigations["%"]
        self._navigations = navigations
        sections = []
        for name in Command.known_sections:
            if name not in entries_by_section:
                continue
            entries = entries_by_section[name]
            section = MenuSection(command=name, entries=entries)
            sections.append(section)
        return sections

    def _make_container_to_part_assignment(self, directory):
        pairs = self._collect_segments(directory.build)
        if not pairs:
            self.io.display("... no segment lys found.")
            return
        container_to_part_assignment = abjad.OrderedDict()
        for source, target in pairs:
            segment = source.parent
            value = segment.get_metadatum(
                "container_to_part_assignment", file_name="__persist__.py"
            )
            if value:
                container_to_part_assignment[segment.name] = value
        return container_to_part_assignment

    def _make_file(self, directory):
        name = self.io.get("file name")
        if self.is_navigation(name):
            return
        if directory.is_score_package_path():
            name = directory.coerce(name)
            predicate = directory.get_name_predicate()
            if predicate and not predicate(abjad.String(name)):
                self.io.display(f"invalid file name {name!r} ...")
                return
        target = directory / name
        if target.exists():
            self.io.display(f"existing {target.trim()} ...")
            return
        else:
            self.io.display(f"writing {target.trim()} ...")
            response = self.io.get("ok?")
            if self.is_navigation(response):
                return
            if response != "y":
                return
        if directory.is_tools():
            if abjad.String(name).is_classfile_name():
                self._copy_boilerplate(
                    directory, "Maker.py", target_name=target.name
                )
                template = target.read_text()
                template = template.format(class_name=target.stem)
                target.write_text(template)
            else:
                self._copy_boilerplate(
                    directory, "function.py", target_name=target.name
                )
                template = target.read_text()
                template = template.format(function_name=target.stem)
                target.write_text(template)
        else:
            if not target.parent.exists():
                target.parent.mkdir()
            target.write_text("")

    def _make_layout_ly(self, path):
        assert path.suffix == ".py"
        ly_name = abjad.String(path.stem).to_dash_case() + ".ly"
        ly_path = path.parent / ly_name
        maker = "__make_layout_ly__.py"
        maker = path.parent / maker
        with self.cleanup([maker]):
            self._copy_boilerplate(
                path.parent,
                maker.name,
                values={"layout_module_name": path.stem},
            )
            self.io.display(f"interpreting {maker.trim()} ...")
            result = self._interpret_file(maker)
            self.io.display(f"removing {maker.trim()} ...")
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self.io.display(stderr_lines, raw=True)

    def _make_material_ly(self, directory):
        assert directory.is_material()
        definition = directory / "definition.py"
        if not definition.is_file():
            self.io.display(f"can not find {definition.trim()} ...")
            return
        ly = directory / "illustration.ly"
        if ly.exists():
            self.io.display(f"removing {ly.trim()} ...")
        maker = directory / "__make_material_ly__.py"
        maker.remove()
        with self.cleanup([maker]):
            self.io.display(f"writing {maker.trim()} ...")
            self._copy_boilerplate(directory, maker.name)
            self.io.display(f"interpreting {maker.trim()} ...")
            result = self._interpret_file(str(maker))
            if ly.is_file():
                self.io.display(f"writing {ly.trim()} ...")
            self.io.display(f"removing {maker.trim()} ...")
            stdout_lines, stderr_lines, exit_code = result
            if exit_code:
                self.io.display(stderr_lines, raw=True)

    def _make_material_pdf(self, directory, open_after=True):
        assert directory.is_material()
        definition = directory / "definition.py"
        if not definition.is_file():
            self.io.display(f"missing {definition.trim()} ...")
            return 0
        name = directory.name.replace("_", " ")
        self.io.display(f"making {name} PDF ...")
        ly = directory / "illustration.ly"
        if ly.exists():
            self.io.display(f"removing {ly.trim()} ...")
            ly.remove()
        pdf = directory / "illustration.pdf"
        if pdf.exists():
            self.io.display(f"removing {pdf.trim()} ...")
            pdf.remove()
        maker = directory / "__make_material_pdf__.py"
        maker.remove()
        with self.cleanup([maker]):
            self.io.display(f"writing {maker.trim()} ...")
            self._copy_boilerplate(directory, maker.name)
            self.io.display(f"interpreting {maker.trim()} ...")
            result = self._interpret_file(maker)
            if ly.is_file():
                self.io.display(f"found {ly.trim()} ...")
            if pdf.is_file():
                self.io.display(f"found {pdf.trim()} ...")
            self.io.display(f"removing {maker.trim()} ...")
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self.io.display(stderr_lines, raw=True)
        if pdf.is_file() and open_after:
            self._open_files([pdf])
        return exit_code

    def _make_package(self, directory):
        asset_type = directory.get_asset_type()
        name = self.io.get(f"enter {asset_type} name")
        if self.is_navigation(name):
            return
        name = directory.coerce(name)
        path = directory / name
        if path.exists():
            self.io.display(f"existing {path.trim()} ...")
            return
        self.io.display(f"making {path.trim()} ...")
        path.mkdir()
        target = path / "__init__.py"
        self.io.display(f"writing {target.trim()} ...")
        target.write_text("")
        if path.is_segment():
            target = path / "__metadata__.py"
            self.io.display(f"writing {target.trim()} ...")
            text = "import abjad\n\n\nmetadata = abjad.OrderedDict()"
            target.write_text(text)
        target = path / "definition.py"
        self.io.display(f"writing {target.trim()} ...")
        target.write_text("")
        self._copy_boilerplate(
            path, "segment_layout.py", target_name="layout.py"
        )
        paths = path.parent.list_paths()
        if path not in paths:
            view = path.parent.get_metadatum("view")
            if view is not None:
                path.parent.add_metadatum("_view", view)
                path.parent.remove_metadatum("view")

    def _make_parts_directory(self, directory):
        assert directory.is_builds()
        self.io.display("getting part names from score template ...")
        part_manifest = directory._get_part_manifest()
        part_names = [_.name for _ in part_manifest]
        part_identifier = [_.identifier for _ in part_manifest]
        for part_name in part_names:
            self.io.display(f"found {part_name} ...")
        self.io.display("")
        name = self.io.get("directory name")
        if self.is_navigation(name):
            return
        name = directory.coerce(name)
        parts_directory = directory / name
        if parts_directory.exists():
            self.io.display(f"existing {parts_directory.trim()} ...")
            return
        paper_size = self.io.get("paper size")
        if self.is_navigation(paper_size):
            return
        orientation = "portrait"
        if paper_size.endswith(" landscape"):
            orientation = "landscape"
            length = len(" landscape")
            paper_size = paper_size[:-length]
        elif paper_size.endswith(" portrait"):
            length = len(" portrait")
            paper_size = paper_size[:-length]
        if paper_size not in self.known_paper_sizes:
            self.io.display(f"unknown paper size: {paper_size} ...")
            self.io.display(f"choose from ...")
            for paper_size in self.known_paper_sizes:
                self.io.display(f"    {paper_size}")
            return
        suffix = self.io.get("catalog number suffix")
        if self.is_navigation(suffix):
            return
        names = (
            "front-cover.tex",
            "preface.tex",
            "music.ly",
            "back-cover.tex",
            "part.tex",
        )
        paths = [parts_directory / _ for _ in names]
        self.io.display("will make ...")
        self.io.display(f"    {parts_directory.trim()}")
        path = parts_directory / "stylesheet.ily"
        self.io.display(f"    {path.trim()}")
        for part_name in part_names:
            dashed_part_name = abjad.String(part_name).to_dash_case()
            for name in names:
                name = f"{dashed_part_name}-{name}"
                path = parts_directory / dashed_part_name / name
                self.io.display(f"    {path.trim()}")
        response = self.io.get("ok?")
        if self.is_navigation(response):
            return
        if response != "y":
            return
        assert not parts_directory.exists()
        parts_directory.mkdir()
        parts_directory.add_metadatum("parts_directory", True)
        if bool(paper_size):
            parts_directory.add_metadatum("paper_size", paper_size)
        if not orientation == "portrait":
            parts_directory.add_metadatum("orientation", orientation)
        if bool(suffix):
            parts_directory.add_metadatum("catalog_number_suffix", suffix)
        self.collect_segments(parts_directory)
        stub = parts_directory.builds._assets / "preface-body.tex"
        if not stub.is_file():
            stub.write_text("")
        stub = parts_directory.builds._assets / "preface-colophon.tex"
        if not stub.is_file():
            stub.write_text("")
        self.generate_stylesheet_ily(parts_directory)
        total_parts = len(part_manifest)
        for i, part in enumerate(part_manifest):
            dashed_part_name = abjad.String(part.name).to_dash_case()
            part_directory = parts_directory / dashed_part_name
            part_directory.mkdir()
            snake_part_name = abjad.String(part.name).to_snake_case()
            part_subtitle = self._part_subtitle(part.name, parentheses=True)
            forces_tagline = self._part_subtitle(part.name) + " part"
            self._generate_back_cover_tex(
                part_directory / f"{dashed_part_name}-back-cover.tex",
                price=f"{part.identifier} ({part.number}/{total_parts})",
            ),
            self._generate_front_cover_tex(
                part_directory / f"{dashed_part_name}-front-cover.tex",
                forces_tagline=forces_tagline,
            )
            self._generate_part_music_ly(
                part_directory / f"{dashed_part_name}-music.ly",
                dashed_part_name=dashed_part_name,
                forces_tagline=forces_tagline,
                keep_with_tag=part.name,
                part=part,
                part_subtitle=part_subtitle,
                silent=True,
            )
            self._generate_part_tex(
                part_directory / f"{dashed_part_name}-part.tex",
                dashed_part_name,
            )
            self._generate_preface_tex(
                part_directory / f"{dashed_part_name}-preface.tex"
            )
            self._copy_boilerplate(
                part_directory,
                "part_layout.py",
                target_name=f"{snake_part_name}_layout.py",
                values={"part_identifier": part.identifier},
            )

    def _make_score_build_directory(self, builds):
        name = self.io.get("build name")
        if self.is_navigation(name):
            return
        name = builds.coerce(name)
        build = builds / name
        if build.exists():
            self.io.display(f"existing {build.trim()} ...")
            return
        paper_size = self.io.get("paper size")
        if paper_size and self.is_navigation(paper_size):
            return
        paper_size = paper_size or "letter"
        orientation = "portrait"
        if paper_size.endswith(" landscape"):
            orientation = "landscape"
            length = len(" landscape")
            paper_size = paper_size[:-length]
        elif paper_size.endswith(" portrait"):
            length = len(" portrait")
            paper_size = paper_size[:-length]
        if paper_size not in self.known_paper_sizes:
            self.io.display(f"unknown paper size {paper_size!r} ...")
            self.io.display("choose from ...")
            for paper_size in self.known_paper_sizes:
                self.io.display(f"    {paper_size}")
            return
        price = self.io.get("price")
        if price and self.is_navigation(price):
            return
        suffix = self.io.get("catalog number suffix")
        if suffix and self.is_navigation(suffix):
            return
        names = (
            "back-cover.tex",
            "front-cover.tex",
            "music.ly",
            "preface.tex",
            "score.tex",
            "stylesheet.ily",
        )
        paths = [build / _ for _ in names]
        self.io.display("making ...")
        self.io.display(f"    {build.trim()}")
        for path in paths:
            self.io.display(f"    {path.trim()}")
        response = self.io.get("ok?")
        if self.is_navigation(response):
            return
        if response != "y":
            return
        assert not build.exists()
        build.mkdir()
        if bool(paper_size):
            build.add_metadatum("paper_size", paper_size)
        if not orientation == "portrait":
            build.add_metadatum("orientation", orientation)
        if bool(price):
            build.add_metadatum("price", price)
        if bool(suffix):
            build.add_metadatum("catalog_number_suffix", suffix)
        self.generate_back_cover_tex(build)
        self.io.display("")
        self.generate_front_cover_tex(build)
        self.io.display("")
        self._copy_boilerplate(
            build, "score_layout.py", target_name="layout.py"
        )
        self.io.display("")
        self.collect_segments(build)
        self.io.display("")
        self.generate_music_ly(build)
        self.io.display("")
        self.generate_preface_tex(build)
        self.io.display("")
        self.generate_score_tex(build)
        self.io.display("")
        self.generate_stylesheet_ily(build)

    def _make_score_package(self):
        scores = self._get_scores_directory()
        wrapper = scores._find_empty_wrapper()
        if wrapper is not None:
            self.io.display(f"found {wrapper.trim()}.")
            response = self.io.get(f"populate {wrapper.trim()}?")
            if self.is_navigation(response):
                return
            if response != "y":
                return
        title = self.io.get("enter title")
        if self.is_navigation(title):
            return
        if wrapper is None:
            name = scores.coerce(title)
            wrapper = scores / name
            if wrapper.exists():
                self.io.display(f"existing {wrapper.trim()} ...")
                return
        self.io.display(f"making {wrapper.trim()} ...")
        year = datetime.date.today().year
        abjad.IOManager._make_score_package(
            score_package_path=str(wrapper),
            composer_email=abjad.abjad_configuration.composer_email,
            composer_full_name=abjad.abjad_configuration.composer_full_name,
            composer_github_username=abjad.abjad_configuration.composer_github_username,
            composer_last_name=abjad.abjad_configuration.composer_last_name,
            score_title=title,
            year=year,
        )
        for path in wrapper.builds.iterdir():
            if path.name == ".gitignore":
                continue
            path.remove()
        view = scores.get_metadatum("view", None)
        if view is not None:
            scores.add_metadatum("_view", view)
        scores.remove_metadatum("view")
        score = wrapper.contents
        assert score.exists()
        if not score.builds._assets.exists():
            self._make__assets_directory(score.builds)
        if not (score.builds / "__metadata__.py").is_file():
            score.builds.write_metadata_py(abjad.OrderedDict())

    def _make_segment_ly(self, directory):
        assert directory.is_segment()
        definition = directory / "definition.py"
        if not definition.is_file():
            self.io.display(f"can not find {definition.trim()} ...")
            return
        ly = directory / "illustration.ly"
        if ly.exists():
            self.io.display(f"removing {ly.trim()} ...")
        maker = directory / "__make_segment_ly__.py"
        maker.remove()
        with self.cleanup([maker]):
            self.io.display(f"writing {maker.trim()} ...")
            self._copy_boilerplate(directory, maker.name)
            previous_segment = directory.get_previous_package()
            if previous_segment is None:
                statement = "previous_metadata = None"
                persist_statement = "previous_persist = None"
            else:
                statement = "from {}.segments.{}.__metadata__"
                statement += " import metadata as previous_metadata"
                statement = statement.format(
                    directory.contents.name, previous_segment.name
                )
                persist_statement = "from {}.segments.{}._persist__"
                persist_statement += " import persist as previous_persist"
                persist_statement = persist_statement.format(
                    directory.contents.name, previous_segment.name
                )
            template = maker.read_text()
            template = template.format(
                previous_segment_metadata_import_statement=statement,
                previous_segment_persist_import_statement=persist_statement,
            )
            maker.write_text(template)
            self.io.display(f"interpreting {maker.trim()} ...")
            result = self._interpret_file(maker)
            if ly.is_file():
                self.io.display(f"found {ly.trim()} ...")
            self.io.display(f"removing {maker.trim()} ...")
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self.io.display(stderr_lines, raw=True)

    def _make_segment_midi(self, directory, open_after=True):
        assert directory.is_segment()
        definition = directory / "definition.py"
        if not definition.is_file():
            self.io.display(f"can not find {definition.trim()} ...")
            return -1
        self.io.display("making MIDI ...")
        ly = directory / "midi.ly"
        if ly.exists():
            self.io.display(f"removing {ly.trim()} ...")
            ly.remove()
        midi = directory / "segment.midi"
        if midi.exists():
            self.io.display(f"removing {midi.trim()} ...")
            midi.remove()
        maker = directory / "__make_segment_midi__.py"
        maker.remove()
        with self.cleanup([maker]):
            self.io.display(f"writing {maker.trim()} ...")
            self._copy_boilerplate(directory, maker.name)
            previous_segment = directory.get_previous_package()
            if previous_segment is None:
                statement = "previous_metadata = None"
                persist_statement = "previous_persist = None"
            else:
                statement = "from {}.segments.{}.__metadata__"
                statement += " import metadata as previous_metadata"
                statement = statement.format(
                    directory.contents.name, previous_segment.name
                )
                persist_statement = "from {}.segments.{}.__persist__"
                persist_statement += " import persist as previous_persist"
                persist_statement = persist_statement.format(
                    directory.contents.name, previous_segment.name
                )
            template = maker.read_text()
            template = template.format(
                previous_segment_metadata_import_statement=statement,
                previous_segment_persist_import_statement=persist_statement,
            )
            maker.write_text(template)
            self.io.display(f"interpreting {maker.trim()} ...")
            result = self._interpret_file(maker)
            self.io.display(f"removing {maker.trim()} ...")
            if midi.is_file():
                self.io.display(f"found {midi.trim()} ...")
            self.io.display(f"removing {maker.trim()} ...")
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self.io.display(stderr_lines, raw=True)
            return exit_code
        if midi.is_file() and open_after:
            self._open_files([midi])
        return 0

    def _make_segment_pdf(self, directory, layout=True, open_after=True):
        assert directory.is_segment()
        if layout is True:
            self.make_layout_ly(directory)
        definition = directory / "definition.py"
        if not definition.is_file():
            self.io.display(f"can not find {definition.trim()} ...")
            return -1
        self.io.display(f"making segment {directory.name} PDF ...")
        ly = directory / "illustration.ly"
        if ly.exists():
            self.io.display(f"removing {ly.trim()} ...")
            ly.remove()
        pdf = directory / "illustration.pdf"
        if pdf.exists():
            self.io.display(f"removing {pdf.trim()} ...")
            pdf.remove()
        maker = directory / "__make_segment_pdf__.py"
        maker.remove()
        with self.cleanup([maker]):
            self._copy_boilerplate(directory, maker.name)
            previous_segment = directory.get_previous_package()
            if previous_segment is None:
                statement = "previous_metadata = None"
                persist_statement = "previous_persist = None"
            else:
                statement = "from {}.segments.{}.__metadata__"
                statement += " import metadata as previous_metadata"
                statement = statement.format(
                    directory.contents.name, previous_segment.name
                )
                persist_statement = "from {}.segments.{}.__persist__"
                persist_statement += " import persist as previous_persist"
                persist_statement = persist_statement.format(
                    directory.contents.name, previous_segment.name
                )
            template = maker.read_text()
            completed_template = template.format(
                previous_segment_metadata_import_statement=statement,
                previous_segment_persist_import_statement=persist_statement,
            )
            maker.write_text(completed_template)
            self.io.display(f"interpreting {maker.trim()} ...")
            result = self._interpret_file(maker)
            if ly.is_file():
                self.io.display(f"found {ly.trim()} ...")
            if pdf.is_file():
                self.io.display(f"found {pdf.trim()} ...")
            self.io.display(f"removing {maker.trim()} ...")
        stdout_lines, stderr_lines, exit_code = result
        if exit_code:
            self.io.display(stderr_lines, raw=True)
            return exit_code
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
                entries=entries, force_single_column=force_single_column
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
        while True:
            result = self._manage_directory_once(directory, redraw=redraw)
            if result in ("quit", None):
                return
            directory, redraw = result

    def _manage_directory_once(self, directory, redraw=True):
        if not directory.exists():
            self.io.display(f"missing {directory.trim()} ...")
            return "quit"
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
        elif response.is_segment_name():
            self.go_to_directory(directory, response.string)
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
                # self._manage_directory(path)
                return path, True
            else:
                self.io.display(f"missing {path.trim()} ...")
        elif response.is_shell():
            self.call_shell(directory, response.string[1:].strip())
        else:
            assert response.payload is None, repr(response)
            self.io.display(f"unknown command {response.string!r} ...")
            if self.test and self.test != "allow_unknown_input":
                raise Exception(response)
        self.io.display("")
        if response.string == "q":
            return "quit"
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
            # self._manage_directory(self.current_directory, redraw=redraw)
            return self.current_directory, redraw

    def _match_alias(self, directory, string):
        if not self.aliases:
            return
        if not self.aliases.get(string):
            return
        value = self.aliases.get(string)
        path = Path(value)
        if path.exists():
            return path
        if directory.is_score_package_path() and not directory.is_scores():
            score_directory = directory.contents
            return directory.contents(value)

    def _match_files(self, files, strings, pattern, prefix):
        if pattern:
            files = self._filter_files(files, strings, pattern)
        else:
            files = [_ for _ in files if _.name[0].isalpha()]
        address = prefix + (pattern or "")
        count = len(files)
        counter = abjad.String("file").pluralize(count)
        message = f"matching {address!r} to {count} {counter} ..."
        self.io.display(message)
        return files

    def _match_smart_file(
        self, directory, pattern, paths, prefix, finder, default_name=None
    ):
        if not pattern:
            self.io.display(f"missing {prefix!r} pattern ...")
            return prefix, None
        alias = ""
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
        address = prefix + (pattern or "") + alias
        count = len(files)
        counter = abjad.String("file").pluralize(count)
        result = None
        if not files:
            self.io.display(f"matching {address!r} to {count} {counter} ...")
        elif len(files) == 1:
            result = files[0]
        else:
            self.io.display(f"matching {address!r} to {count} {counter} ...")
            for file_ in files:
                self.io.display(file_.trim(), raw=True)
            result = files[0]
        return address, result

    @staticmethod
    def _message_activate(ly, tag, count, name=None):
        messages = []
        name = name or tag
        if 0 < count:
            counter = abjad.String("tag").pluralize(count)
            message = f"activating {count} {name} {counter}"
            if ly is not None:
                message += f" in {ly.name}"
            message += " ..."
            messages.append(message)
        return messages

    @staticmethod
    def _message_deactivate(ly, tag, count, name=None):
        messages = []
        name = name or tag
        if 0 < count:
            counter = abjad.String("tag").pluralize(count)
            message = f"deactivating {count} {name} {counter}"
            if ly is not None:
                message += f" in {ly.name}"
            message += " ..."
            messages.append(message)
        return messages

    def _open_files(self, paths, force_vim=False, silent=False):
        assert isinstance(paths, collections.abc.Iterable), repr(paths)
        for path in paths:
            if not path.exists():
                self.io.display(f"missing {path.trim()} ...")
                return
            if not path.is_file():
                self.io.display(f"not a file {path.trim()} ...")
                return
        string = " ".join([str(_) for _ in paths])
        if force_vim or all(
            _.suffix in self.configuration.editor_suffixes for _ in paths
        ):
            mode = "e"
        elif all(_.suffix in (".mid", ".midi", ".pdf") for _ in paths):
            mode = "o"
        else:
            mode = self.io.get("open or edit (o|e)?")
            if self.is_navigation(mode):
                return
            mode = mode.lower()
        if mode == "e":
            command = f"vim {string}"
            if not silent:
                for path in paths:
                    self.io.display(f"editing {path.trim()} ...")
        elif mode == "o":
            command = f"open {string}"
            command = command.replace("(", r"\(")
            command = command.replace(")", r"\)")
            if not silent:
                for path in paths:
                    self.io.display(f"opening {path.trim()} ...")
        else:
            return
        if 20 <= len(paths):
            response = self.io.get(f"{len(paths)} files ok?")
            if self.is_navigation(response):
                return response
            if response != "y":
                return
        if self.test:
            return
        if not paths:
            return
        if platform.system() == "Darwin" and paths[0].suffix == ".pdf":
            boilerplate = self.configuration.boilerplate_directory
            source = boilerplate / "__close_preview_pdf__.scr"
            for path in paths:
                template = source.read_text()
                template = template.format(file_path=path)
                target = self.configuration.home_directory / source.name
                if target.exists():
                    target.remove()
                with self.cleanup([target]):
                    target.write_text(template)
                    permissions = f"chmod 755 {target}"
                    abjad.IOManager.spawn_subprocess(permissions)
                    abjad.IOManager.spawn_subprocess(str(target))
        abjad.IOManager.spawn_subprocess(command)

    @staticmethod
    def _part_subtitle(part_name, parentheses=False):
        words = abjad.String(part_name).delimit_words()
        number = None
        try:
            number = int(words[-1])
        except ValueError:
            pass
        if number is not None:
            if parentheses:
                words[-1] = f"({number})"
            else:
                words[-1] = str(number)
        words = [_.lower() for _ in words]
        part_subtitle = " ".join(words)
        return part_subtitle

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
        new_file_contents = "".join(new_file_lines)
        file_path.write_text(new_file_contents)

    def _replace_in_tree(
        self, directory, search_string, replace_string, complete_words=False
    ):
        command = f"ajv replace {search_string!r} {replace_string!r} -Y"
        if complete_words:
            command += " -W"
        with self.change(directory):
            lines = abjad.IOManager.run_command(command)
            lines = [_.strip() for _ in lines if not _ == ""]
            return lines

    def _run_doctest(self, paths):
        assert isinstance(paths, collections.abc.Iterable), repr(paths)
        for path in paths:
            if path.is_dir():
                raise Exception(f"directory {path.trim()} not a file ...")
        if self.test:
            return
        if paths:
            string = " ".join([str(_) for _ in paths])
            command = f"baca-doctest --report-only-first-failure {string}"
            abjad.IOManager.spawn_subprocess(command)

    def _run_lilypond(self, ly):
        assert ly.exists()
        if not abjad.IOManager.find_executable("lilypond"):
            raise ValueError("cannot find LilyPond executable.")
        directory = ly.parent
        pdf = ly.with_suffix(".pdf")
        backup_pdf = ly.with_suffix("._backup.pdf")
        log = directory / ".log"
        if backup_pdf.exists():
            backup_pdf.remove()
        if pdf.exists():
            self.io.display(f"removing {pdf.trim()} ...")
            pdf.remove()
        assert not pdf.exists()
        with self.change(directory):
            self.io.display(f"interpreting {ly.trim()} ...")
            abjad.IOManager.run_lilypond(
                str(ly), lilypond_log_file_path=str(log)
            )
            log.remove_lilypond_warnings(
                crescendo_too_small=True,
                decrescendo_too_small=True,
                overwriting_glissando=True,
            )
            self._display_lilypond_log_errors(log=log)
            if pdf.is_file():
                self.io.display(f"found {pdf.trim()} ...")
            else:
                self.io.display(f"can not produce {pdf.trim()} ...")

    def _run_pytest(self, paths):
        assert isinstance(paths, collections.abc.Iterable), repr(paths)
        for path in paths:
            if path.is_dir():
                raise Exception(f"directory {path.trim()} not a file ...")
        if self.test:
            return
        if paths:
            string = " ".join([str(_) for _ in paths])
            command = f'py.test -xrf {string}; say "done"'
            abjad.IOManager.spawn_subprocess(command)

    def _select_parts(self, directory, verb=""):
        part_manifest = directory._get_part_manifest()
        if not part_manifest:
            self.io.display("score template defines no part manifest.")
            return
        items = []
        for part in part_manifest:
            assert part.name is not None
            item = (part.name, part)
            items.append(item)
        if verb:
            header = f"available parts to {verb}"
            prompt = f"select parts to {verb}"
        else:
            header = "available parts"
            prompt = f"select parts"
        selector = self._make_selector(
            aliases=None,
            header=header,
            items=items,
            navigations=self.navigations,
            prompt=prompt,
        )
        response = selector(redraw=True)
        if self.is_navigation(response.string):
            return response.string
        if response.payload is None:
            if bool(response.string):
                self.io.display(f"matches no part {response.string!r} ...")
            return
        assert isinstance(response.payload, list), response
        result = response.payload
        return result

    def _select_paths(self, directory, infinitive=""):
        counter = abjad.String(directory.get_asset_type()).pluralize()
        paths = directory.list_paths()
        if not paths:
            self.io.display(f"missing {directory.trim()} {counter} ...")
            return
        items = [(_.get_identifier(), _) for _ in paths]
        if infinitive:
            prompt = f"select {counter} {infinitive}"
        else:
            prompt = f"select {counter}"
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
                self.io.display(f"matches no path {response.string!r} ...")
            return
        assert isinstance(response.payload, list), response
        result = response.payload
        return result

    def _select_paths_in_buildspace(
        self,
        directory,
        name,
        verb,
        count=None,
        supply_missing=None,
        underscores=False,
    ):
        assert directory.is_buildspace()
        selected_paths = []
        if directory.is_segment():
            if underscores:
                path = directory / name.replace("-", "_")
            else:
                path = directory / name
            if supply_missing or path.is_file():
                selected_paths.append(path)
            if not selected_paths:
                self.io.display(f"no files matching {name} ...")
            return selected_paths
        if directory.is_part():
            paths = directory.get_files_ending_with(name)
            if not paths:
                if supply_missing:
                    if underscores:
                        path = directory / name.replace("-", "_")
                    else:
                        path = directory / name
                    paths.append(path)
                else:
                    self.io.display(f"no file ending {name} ...")
                    return
            if 1 < len(paths):
                self.io.display(f"too many files ending in {name} ...")
                return
            assert len(paths) == 1, repr(paths)
            return paths
        if not directory.is_parts() and not directory.is_segments():
            path = directory.build / name
            if path.is_file():
                selected_paths.append(path)
            if not selected_paths:
                self.io.display(f"no files matching {name} ...")
            return selected_paths
        paths = []
        if directory.is_segments():
            for segment in directory.list_paths():
                if not segment.is_dir():
                    continue
                paths_ = segment.get_files_ending_with(name)
                paths.extend(paths_)
        else:
            for part_directory in directory.list_paths():
                if not part_directory.is_dir():
                    continue
                if part_directory.name in ("_assets", "_segments"):
                    continue
                paths_ = part_directory.get_files_ending_with(name)
                if paths_:
                    paths.extend(paths_)
                elif supply_missing:
                    file_name = f"{part_directory.name}-{name}"
                    if underscores:
                        file_name = file_name.replace("-", "_")
                    path = part_directory / file_name
                    paths.append(path)
        if not paths:
            self.io.display(f"no files ending in {name} ...")
        if count is not None:
            files = abjad.String("file").pluralize(count)
        else:
            files = "files"
        header = f"available {files} to {verb}:"
        items = [(_.name, _) for _ in paths]
        prompt = f"select {files} to {verb}"
        selector = self._make_selector(
            aliases=None,
            header=header,
            items=items,
            navigations=self.navigations,
            prompt=prompt,
        )
        response = selector()
        if self.is_navigation(response.string):
            return response.string
        if response.payload is None:
            if bool(response.string):
                self.io.display(f"matches no path {response.string!r} ...")
            return
        assert isinstance(response.payload, list), response
        paths = response.payload
        if len(paths) <= 1:
            return paths
        self.io.display(f"will {verb} ...")
        for path in paths:
            self.io.display(path.trim(), raw=True)
        self.io.display("")
        response = self.io.get("ok?")
        if self.is_navigation(response):
            return
        if response != "y":
            return
        return paths

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
    def _to_paper_dimensions(paper_size, orientation="portrait"):
        orientations = ("landscape", "portrait", None)
        assert orientation in orientations, repr(orientation)
        paper_dimensions = AbjadIDE.paper_size_to_paper_dimensions[paper_size]
        paper_dimensions = paper_dimensions.replace(" x ", " ")
        width, height, unit = paper_dimensions.split()
        if orientation == "landscape":
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
                self.io.display(f"trashing {path.trim()} ...")
                path.remove()
            else:
                self.io.display(f"missing {path.trim()} ...")

    @staticmethod
    def _trim_illustration_ly(ly):
        assert ly.is_file()
        lines = []
        with ly.open() as file_pointer:
            found_score_context_open = False
            found_score_context_close = False
            for line in file_pointer.readlines():
                if r"\context Score" in line:
                    found_score_context_open = True
                if line == "        >>\n":
                    found_score_context_close = True
                if found_score_context_open:
                    lines.append(line)
                if found_score_context_close:
                    lines.append("\n")
                    break
        if lines and lines[0].startswith("    "):
            lines = [_[8:] for _ in lines]
        if lines and lines[-1] == "\n":
            lines.pop()
        lines = "".join(lines)
        return lines

    ### PUBLIC PROPERTIES ###

    @property
    def aliases(self) -> abjad.OrderedDict:
        """
        Gets aliases.
        """
        return self._aliases

    @property
    def clipboard(self) -> list:
        """
        Gets clipboard.
        """
        return self._clipboard

    @property
    def commands(self) -> abjad.OrderedDict:
        """
        Gets commands.
        """
        return self._commands

    @property
    def current_directory(self) -> typing.Optional[abjad.Path]:
        """
        Gets current directory.
        """
        return self._current_directory

    @property
    def example(self) -> typing.Optional[bool]:
        """
        Is true when IDE is example.
        """
        return self._example

    @property
    def io(self) -> IO:
        """
        Gets IO.
        """
        return self._io

    @property
    def navigation(self) -> typing.Optional[str]:
        """
        Gets current navigation command.
        """
        return self._navigation

    @property
    def navigations(self) -> abjad.OrderedDict:
        """
        Gets all navigation commands.
        """
        return self._navigations

    @property
    def previous_directory(self) -> typing.Optional[str]:
        """
        Gets previous directory.
        """
        return self._previous_directory

    @property
    def test(self) -> typing.Optional[bool]:
        """
        Is true when IDE is test.
        """
        return self._test

    ### PUBLIC METHODS ###

    def activate(
        self,
        path: abjad.Path,
        tag: typing.Union[str, typing.Callable],
        deactivate: bool = False,
        indent: int = 0,
        message_zero: bool = False,
        name: str = None,
    ) -> None:
        """
        Activates ``tag`` in ``path``.
        """
        tag_: typing.Union[abjad.Tag, typing.Callable]
        if isinstance(tag, str):
            tag_ = abjad.Tag(tag)
        else:
            assert callable(tag)
            tag_ = tag
        assert isinstance(tag_, abjad.Tag) or callable(tag_)
        if deactivate:
            result = path.deactivate(
                tag_, indent=indent, message_zero=message_zero, name=name
            )
            assert result is not None
            count, skipped, messages = result
        else:
            result = path.activate(
                tag_, indent=indent, message_zero=message_zero, name=name
            )
            assert result is not None
            count, skipped, messages = result
        self.io.display(messages)

    @staticmethod
    def change(directory) -> abjad.TemporaryDirectoryChange:
        """
        Makes temporary directory change context manager.
        """
        return abjad.TemporaryDirectoryChange(directory=directory)

    @staticmethod
    def cleanup(remove=None) -> abjad.FilesystemState:
        """
        Makes filesystem state context manager.
        """
        return abjad.FilesystemState(remove=remove)

    def deactivate(
        self,
        path: abjad.Path,
        tag: typing.Union[str, typing.Callable],
        indent: int = 0,
        message_zero: bool = False,
        name: str = None,
    ) -> None:
        """
        Deactivates ``tag`` in ``path``.
        """
        self.activate(
            path,
            tag,
            name=name,
            deactivate=True,
            indent=indent,
            message_zero=message_zero,
        )

    def is_navigation(self, argument: typing.Optional[str]) -> bool:
        """
        Is true when ``argument`` is navigation.
        """
        assert argument != "", repr(argument)
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

    def run(self, job: abjad.Job, quiet: bool = False) -> None:
        """
        Runs ``job`` on ``path``.
        """
        message_zero = not bool(quiet)
        job = abjad.new(job, message_zero=message_zero)
        messages: typing.List[abjad.String] = job()
        self.io.display(messages)

    ### USER METHODS ###

    @Command(
        "bkc",
        description="package - black check",
        external_directories=True,
        menu_section="package",
        score_package_paths=True,
        scores_directory=True,
    )
    def black_check(self, directory: Path) -> None:
        """
        Runs black check on package.
        """
        if self.test:
            return
        BLACK_OPTS = "--target-version=py36 --line-length=79 --check --diff"
        BLACK_EXCLUDE = "__metadata__.py|__persist__.py|segments|layout.py"
        command = f"black {BLACK_OPTS} --exclude '{BLACK_EXCLUDE}'"
        if not directory.is_scores():
            root = directory._get_repository_root()
            if not root:
                self.io.display(f"missing {directory.trim()} repository ...")
                return
            with self.change(root):
                self.io.display(f"Running black check on {root} ...")
                lines = abjad.IOManager.run_command(f"{command} {root}")
                self.io.display(lines, raw=True)
        else:
            assert directory.is_scores()
            paths = directory.list_paths()
            for i, path in enumerate(paths):
                self.io.display(f"Running black check on {path} ...")
                lines = abjad.IOManager.run_command(f"{command} {path}")
                self.io.display(lines, raw=True)
                if i + 1 < len(paths):
                    self.io.display("")

    @Command(
        "bkr",
        description="package - black reformat",
        external_directories=True,
        menu_section="package",
        score_package_paths=True,
        scores_directory=True,
    )
    def black_reformat(self, directory: Path) -> None:
        """
        Runs black reformat on package.
        """
        if self.test:
            return
        BLACK_OPTS = "--target-version=py36 --line-length=79"
        BLACK_EXCLUDE = "__metadata__.py|__persist__.py|segments|layout.py"
        command = f"black {BLACK_OPTS} --exclude '{BLACK_EXCLUDE}'"
        if not directory.is_scores():
            root = directory._get_repository_root()
            if not root:
                self.io.display(f"missing {directory.trim()} repository ...")
                return
            with self.change(root):
                self.io.display(f"Running black reformat on {root} ...")
                lines = abjad.IOManager.run_command(f"{command} {root}")
                self.io.display(lines, raw=True)
        else:
            assert directory.is_scores()
            paths = directory.list_paths()
            for i, path in enumerate(paths):
                self.io.display(f"Running black reformat on {path} ...")
                lines = abjad.IOManager.run_command(f"{command} {path}")
                self.io.display(lines, raw=True)
                if i + 1 < len(paths):
                    self.io.display("")

    @Command(
        "ppb",
        description="part.pdf - build",
        menu_section="parts",
        score_package_paths=("part", "parts"),
    )
    def build_part_pdf(self, directory: Path) -> None:
        """
        Builds ``part.pdf`` from the ground up.
        """
        assert directory.is_parts() or directory.is_part()
        name, verb = "part.pdf", "build"
        # TODO:
        if directory.is_part():
            raise NotImplementedError()
        paths = self._select_paths_in_buildspace(
            directory, name, verb, supply_missing=True
        )
        if self.is_navigation(paths):
            return
        if not paths:
            return
        assert directory.build is not None
        total_parts = len(directory.build._get_part_manifest())
        path_count = len(paths)
        for i, path in enumerate(paths):
            part = path.to_part()
            dashed_part_name = abjad.String(part.name).to_dash_case()
            part_directory = directory / dashed_part_name
            part_pdf_path = part_directory / dashed_part_name
            part_pdf_path = part_pdf_path.with_suffix(".pdf")
            self.io.display(f"building {part_pdf_path.trim()} ...")
            snake_part_name = abjad.String(part.name).to_snake_case()
            file_name = f"{snake_part_name}_layout.py"
            path = part_directory / file_name
            self._make_layout_ly(path)
            self.io.display("")
            file_name = f"{dashed_part_name}-front-cover.tex"
            path = part_directory / file_name
            self._interpret_tex_file(path)
            self.io.display("")
            file_name = f"{dashed_part_name}-preface.tex"
            path = part_directory / file_name
            self._interpret_tex_file(path)
            self.io.display("")
            file_name = f"{dashed_part_name}-music.ly"
            path = part_directory / file_name
            self._run_lilypond(path)
            self.io.display("")
            file_name = f"{dashed_part_name}-back-cover.tex"
            path = part_directory / file_name
            self._interpret_tex_file(path)
            self.io.display("")
            file_name = f"{dashed_part_name}-part.tex"
            path = part_directory / file_name
            self._interpret_tex_file(path)
            if 1 < path_count and i < path_count - 1:
                self.io.display("")
        if path_count == 1:
            file_name = f"{dashed_part_name}-part.pdf"
            path = part_directory / file_name
            self._open_files([path])

    @Command(
        "spb",
        description="score.pdf - build",
        menu_section="score",
        score_package_path_blacklist=("parts",),
        score_package_paths=("_segments", "build"),
    )
    def build_score_pdf(self, directory: Path) -> None:
        """
        Builds ``score.pdf`` from the ground up.
        """
        assert directory.is_build() or directory.is__segments()
        assert directory.build is not None
        self.io.display("building score ...")
        self.interpret_music_ly(directory.build, open_after=False)
        self.io.display("")
        tex = directory.build / "front-cover.tex"
        pdf = directory.build / "front-cover.pdf"
        if tex.is_file():
            self.interpret_front_cover_tex(directory.build, open_after=False)
        elif pdf.is_file():
            self.io.display(f"using existing {pdf.trim()} ...")
        else:
            self.io.display("missing front cover ...")
            return
        self.io.display("")
        tex = directory.build / "preface.tex"
        pdf = directory.build / "preface.pdf"
        if tex.is_file():
            self.interpret_preface_tex(directory.build, open_after=False)
        elif pdf:
            self.io.display(f"using existing {pdf.trim()} ...")
        else:
            self.io.display("missing preface ...")
            return
        self.io.display("")
        tex = directory.build / "back-cover.tex"
        pdf = directory.build / "back-cover.pdf"
        if tex.is_file():
            self.interpret_back_cover_tex(directory.build, open_after=False)
        elif pdf.is_file():
            self.io.display(f"using existing {pdf.trim()} ...")
        else:
            self.io.display("missing back cover ...")
            return
        self.io.display("")
        self.generate_score_tex(directory.build)
        self.io.display("")
        self.interpret_score_tex(directory.build)

    @Command(
        "!",
        description="shell - call",
        external_directories=True,
        menu_section="shell",
        score_package_paths=True,
        scores_directory=True,
    )
    def call_shell(self, directory: Path, statement: str) -> None:
        """
        Calls shell.
        """
        with self.change(directory):
            self.io.display(f"calling shell on {statement!r} ...")
            abjad.IOManager.spawn_subprocess(statement)

    @Command(
        "dpc",
        description="definition.py - check",
        menu_section="definition",
        score_package_paths=("illustrationspace",),
    )
    def check_definition_py(self, directory: Path) -> int:
        """
        Checks ``definition.py``.

        Returns integer exit code for Travis tests.
        """
        assert directory.is_illustrationspace()
        if directory.is_material() or directory.is_segment():
            self.io.display("checking definition ...")
            definition = directory / "definition.py"
            if not definition.is_file():
                self.io.display(f"missing {definition.trim()} ...")
                return -1
            with abjad.Timer() as timer:
                result = self._interpret_file(definition)
            stdout_lines, stderr_lines, exit = result
            self.io.display(stdout_lines, wrap=True)
            if exit:
                self.io.display(
                    [f"{definition.trim()} FAILED:"] + stderr_lines, wrap=True
                )
            else:
                self.io.display(f"{definition.trim()} ... OK", raw=True)
            self.io.display(timer.total_time_message)
            return exit
        else:
            paths = directory.list_paths()
            path_count = len(paths)
            for i, path in enumerate(paths):
                self.check_definition_py(path)
                if i + 1 < path_count:
                    self.io.display("")
        return 0

    @Command(
        "oc",
        description=".optimization - checkout",
        menu_section="illustration",
        score_package_paths=("illustrationspace",),
    )
    def check_out_optimization(self, directory: Path) -> None:
        """
        Checks out ``.optimization``.
        """
        assert directory.is_illustrationspace()
        if directory.is_material() or directory.is_segment():
            paths = [directory / ".optimization"]
        else:
            paths = []
            for path in directory.list_paths():
                optimization = path / ".optimization"
                if optimization.is_file():
                    paths.append(optimization)
        self._check_out_paths(paths)

    @Command(
        "ggc",
        description="segments - collect",
        menu_section="segments",
        score_package_paths=("_segments", "build"),
    )
    def collect_segments(self, directory: Path) -> None:
        """
        Collects segment lys.

        Copies illustration.ly files from segment directories to
        build/_segments directory.

        Trims top-level comments, header block, paper block from each
        illustration.ly file.

        Keeps score block in each illustration.ly file.

        Activates and deactivates build-appropriate tags.
        """
        assert directory.is_build() or directory.is__segments()
        self.io.display("collecting segment lys ...")
        pairs = self._collect_segments(directory.build)
        if not pairs:
            self.io.display("... no segment lys found.")
            return
        self._make__assets_directory(directory.build)
        self._make__segments_directory(directory.build)
        fermata_measure_numbers = abjad.OrderedDict()
        time_signatures = abjad.OrderedDict()
        for source, target in pairs:
            source_ily = source.with_suffix(".ily")
            target_ily = target.with_suffix(".ily")
            if target_ily.exists():
                self.io.display(f" Removing {target_ily.trim()} ...")
            if source_ily.is_file():
                self.io.display(f" Writing {target_ily.trim()} ...")
                shutil.copyfile(str(source_ily), target_ily)
            if target.exists():
                self.io.display(f" Removing {target.trim()} ...")
            self.io.display(f" Writing {target.trim()} ...")
            text = self._trim_illustration_ly(source)
            target.write_text(text)
            segment = source.parent
            value = segment.get_metadatum("fermata_measure_numbers")
            if value:
                fermata_measure_numbers[segment.name] = value
            value = segment.get_metadatum("time_signatures")
            if value:
                time_signatures[segment.name] = value
        final_file_name = target.with_suffix(".ily").name
        key = "fermata_measure_numbers"
        if bool(fermata_measure_numbers):
            directory.contents.add_metadatum(key, fermata_measure_numbers)
        else:
            directory.contents.remove_metadatum(key)
        key = "time_signatures"
        if bool(time_signatures):
            directory.contents.add_metadatum(key, time_signatures)
        else:
            directory.contents.remove_metadatum(key)

        def match_left_broken_should_deactivate(tags):
            if (
                abjad.tags.LEFT_BROKEN in tags
                and abjad.tags.SPANNER_START in tags
            ):
                return True
            if (
                abjad.tags.LEFT_BROKEN in tags
                and abjad.tags.SPANNER_STOP in tags
                and abjad.tags.EXPLICIT_DYNAMIC in tags
            ):
                return True
            return False

        def match_phantom_should_activate(tags):
            if abjad.tags.PHANTOM not in tags:
                return False
            if abjad.tags.ONE_VOICE_COMMAND in tags:
                return True
            if abjad.tags.SHOW_TO_JOIN_BROKEN_SPANNERS in tags:
                return True
            if abjad.tags.SPANNER_STOP in tags:
                return True
            return False

        def match_phantom_should_deactivate(tags):
            if abjad.tags.PHANTOM not in tags:
                return False
            if (
                abjad.tags.SPANNER_START in tags
                and abjad.tags.LEFT_BROKEN in tags
            ):
                return True
            if (
                abjad.tags.SPANNER_STOP in tags
                and abjad.tags.RIGHT_BROKEN in tags
            ):
                return True
            if abjad.tags.HIDE_TO_JOIN_BROKEN_SPANNERS in tags:
                return True
            return False

        _segments = directory._segments
        for job in [
            abjad.Job.handle_edition_tags(_segments),
            abjad.Job.handle_fermata_bar_lines(_segments),
            abjad.Job.handle_shifted_clefs(_segments),
            abjad.Job.handle_mol_tags(_segments),
            abjad.Job.color_persistent_indicators(_segments, undo=True),
            abjad.Job.show_music_annotations(_segments, undo=True),
            abjad.Job.join_broken_spanners(_segments),
            abjad.Job.show_tag(
                _segments,
                "left-broken-should-deactivate",
                match=match_left_broken_should_deactivate,
                skip_file_name=final_file_name,
                undo=True,
            ),
            abjad.Job.show_tag(
                _segments, abjad.tags.PHANTOM, skip_file_name=final_file_name
            ),
            abjad.Job.show_tag(
                _segments,
                abjad.tags.PHANTOM,
                prepend_empty_chord=True,
                skip_file_name=final_file_name,
                undo=True,
            ),
            abjad.Job.show_tag(
                _segments,
                "phantom-should-activate",
                match=match_phantom_should_activate,
                skip_file_name=final_file_name,
            ),
            abjad.Job.show_tag(
                _segments,
                "phantom-should-deactivate",
                match=match_phantom_should_deactivate,
                skip_file_name=final_file_name,
                undo=True,
            ),
            abjad.Job.show_tag(
                _segments,
                abjad.tags.EOS_STOP_MM_SPANNER,
                skip_file_name=final_file_name,
            ),
        ]:
            self.run(job, quiet=False)

    @Command(
        "ccl",
        description="clefs - color",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def color_clefs(self, directory: Path) -> None:
        """
        Colors clefs.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_clefs(directory))

    @Command(
        "dcl",
        description="dynamics - color",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def color_dynamics(self, directory: Path) -> None:
        """
        Colors dynamics.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_dynamics(directory))

    @Command(
        "icl",
        description="instruments - color",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def color_instruments(self, directory: Path):
        """
        Colors instruments.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_instruments(directory))

    @Command(
        "mmcl",
        description="margin markup - color",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def color_margin_markup(self, directory: Path) -> None:
        """
        Colors margin markup.
        """
        assert directory.is_score_package_path()
        self.run(abjad.Job.color_margin_markup(directory))

    @Command(
        "tmcl",
        description="metronome marks - color",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def color_metronome_marks(self, directory: Path) -> None:
        """
        Colors metronome marks.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_metronome_marks(directory))

    @Command(
        "picl",
        description="persistent indicators - color",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def color_persistent_indicators(self, directory: Path) -> None:
        """
        Colors persistent indicators.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_persistent_indicators(directory))

    @Command(
        "slcl",
        description="staff lines - color",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def color_staff_lines(self, directory: Path) -> None:
        """
        Colors staff lines.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_staff_lines(directory))

    @Command(
        "tscl",
        description="time signatures - color",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def color_time_signatures(self, directory: Path) -> None:
        """
        Colors time signatures.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_time_signatures(directory))

    @Command(
        "cbc",
        description="clipboard - copy",
        external_directories=True,
        menu_section="clipboard",
        score_package_paths=True,
        scores_directory=True,
    )
    def copy_to_clipboard(self, directory: Path) -> None:
        """
        Copies to clipboard.
        """
        paths = self._select_paths(directory, infinitive="for clipboard")
        if self.is_navigation(paths):
            return
        assert isinstance(paths, list)
        self.io.display("copying to clipboard ...")
        for path in paths:
            self.io.display(path.trim(), raw=True)
            self.clipboard.append(path)

    @Command(
        "cbx",
        description="clipboard - cut",
        external_directories=True,
        menu_section="clipboard",
        score_package_paths=True,
        scores_directory=True,
    )
    def cut_to_clipboard(self, directory: Path) -> None:
        """
        Cuts to clipboard.
        """
        paths = self._select_paths(directory, infinitive="for clipboard")
        if self.is_navigation(paths):
            return
        assert isinstance(paths, list)
        self.io.display("cutting to clipboard ...")
        for path in paths:
            self.io.display(path.trim(), raw=True)
            self.clipboard.append(path)
            path.remove()

    @Command(
        "^^",
        description="all - doctest",
        external_directories=True,
        menu_section="all",
        score_package_paths=True,
        scores_directory=True,
    )
    def doctest_all(self, directory: Path, pattern: str = None) -> None:
        """
        Doctests all.
        """
        files, strings = directory._find_doctest_files(force=True)
        files = self._match_files(files, strings, pattern, "^^")
        self._run_doctest(files)
        abjad.IOManager.spawn_subprocess('say "done"')

    @Command(
        "dup",
        description="path - duplicate",
        external_directories=True,
        menu_section="path",
        score_package_path_blacklist=("contents", "material", "segment"),
        score_package_paths=True,
        scores_directory=True,
    )
    def duplicate(self, directory: Path) -> None:
        """
        Duplicates asset.
        """
        paths = self._select_paths(directory, infinitive="to duplicate")
        if self.is_navigation(paths):
            return
        assert isinstance(paths, list)
        if len(paths) == 1:
            source = paths[0]
            self.io.display(f"duplicating {source.trim()} ...")
        else:
            self.io.display(f"duplicating ...")
            for path in paths:
                self.io.display(f"    {path.trim()}")
            response = self.io.get("ok?")
            if self.is_navigation(response):
                return
            if response != "y":
                return
        for source in paths:
            title = None
            name_metadatum = None
            if source.is_wrapper():
                title = self.io.get("enter title")
                if self.is_navigation(title):
                    continue
                name = title
            else:
                name = self.io.get("enter new name")
                if self.is_navigation(name):
                    continue
            name = source.parent.coerce(name, suffix=source.suffix)
            target = source.with_name(name)
            if source == target:
                continue
            if source.is_segment() and source.get_metadatum("name"):
                name_metadatum = self.io.get("name metadatum")
            self.io.display(f"writing {target.trim()} ...")
            response = self.io.get("ok?")
            if self.is_navigation(response):
                return
            if response != "y":
                continue
            if source.is_file():
                shutil.copyfile(str(source), str(target))
            elif source.is_dir():
                shutil.copytree(str(source), str(target))
            else:
                raise ValueError(source)
            if target.is_material_or_segment():
                if name_metadatum:
                    target.add_metadatum("name", name_metadatum)
                else:
                    target.remove_metadatum("name")
                lines = self._replace_in_tree(
                    target, source.name, target.name, complete_words=True
                )
                self.io.display(lines)
            elif target.is_wrapper():
                shutil.move(
                    str(target.wrapper / source.name), str(target.contents)
                )
                lines = self._replace_in_tree(
                    target, source.name, target.name, complete_words=True
                )
                self.io.display(lines)
                if title is not None:
                    target.contents.add_metadatum("title", title)
                    source_title = source.contents.get_metadatum("title")
                    if source_title is not None:
                        lines = self._replace_in_tree(
                            target, source_title, title, complete_words=True
                        )
                        self.io.display(lines)

    @Command(
        "al",
        description="log - aliases",
        external_directories=True,
        menu_section="log",
        score_package_paths=True,
        scores_directory=True,
    )
    def edit_aliases_py(self) -> None:
        """
        Edits ``__aliases__.py``.
        """
        self._open_files([self.configuration.aliases_file_path])
        self.configuration._read_aliases_file()
        self._aliases = abjad.OrderedDict(self.configuration.aliases)
        for name, path in self.aliases.items():
            if not Path(path).exists():
                self.io.display(f"missing {name!r} {path} ...")

    @Command(
        "@@",
        description="all - edit",
        external_directories=True,
        menu_section="all",
        score_package_paths=True,
        scores_directory=True,
    )
    def edit_all(self, directory: Path, pattern: str = None) -> None:
        """
        Edits all files.
        """
        files, strings = directory._find_editable_files(force=True)
        files = self._match_files(files, strings, pattern, "@@")
        self._open_files(files)

    @Command(
        "bcte",
        description="back-cover.tex - edit",
        menu_section="back cover",
        score_package_paths=("_segments", "build"),
    )
    def edit_back_cover_tex(self, directory: Path) -> None:
        """
        Edits ``back-cover.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "back-cover.tex", "open"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._open_files(paths)

    @Command(
        "dpe",
        description="definition.py - edit",
        menu_section="definition",
        score_package_paths=("illustrationspace",),
    )
    def edit_definition_py(self, directory: Path) -> None:
        """
        Edits ``definition.py``.
        """
        assert directory.is_illustrationspace()
        paths = []
        if directory.is_material() or directory.is_segment():
            paths.append(directory / "definition.py")
        else:
            for path in directory.list_paths():
                definition_py = path / "definition.py"
                if definition_py.is_file():
                    paths.append(definition_py)
        self._open_files(paths)

    @Command(
        "fcte",
        description="front-cover.tex - edit",
        menu_section="front cover",
        score_package_paths=("_segments", "build"),
    )
    def edit_front_cover_tex(self, directory: Path) -> None:
        """
        Edits ``front-cover.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "front-cover.tex", "open"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._open_files(paths)

    @Command(
        "iie",
        description="illustration.ily - edit",
        menu_section="illustration",
        score_package_paths=("illustrationspace",),
    )
    def edit_illustration_ily(self, directory: Path) -> None:
        """
        Edits ``illustration.ily``.
        """
        assert directory.is_illustrationspace()
        if directory.is_material() or directory.is_segment():
            paths = [directory / "illustration.ily"]
        else:
            paths = []
            for path in directory.list_paths():
                illustration_ily = path / "illustration.ily"
                if illustration_ily.is_file():
                    paths.append(illustration_ily)
        self._open_files(paths)

    @Command(
        "ile",
        description="illustration.ly - edit",
        menu_section="illustration",
        score_package_paths=("illustrationspace",),
    )
    def edit_illustration_ly(self, directory: Path) -> None:
        """
        Edits ``illustration.ly``.
        """
        assert directory.is_illustrationspace()
        if directory.is_material() or directory.is_segment():
            paths = [directory / "illustration.ly"]
        else:
            paths = []
            for path in directory.list_paths():
                illustration_ly = path / "illustration.ly"
                if illustration_ly.is_file():
                    paths.append(illustration_ly)
        self._open_files(paths)

    @Command(
        "lx",
        description="log - latex",
        external_directories=True,
        menu_section="log",
        score_package_paths=True,
        scores_directory=True,
    )
    def edit_latex_log(self) -> None:
        """
        Edits ``latex.log``.
        """
        path = self.configuration.latex_log_file_path
        self._open_files([path])

    @Command(
        "lle",
        description="layout.ly - edit",
        menu_section="layout",
        score_package_paths=("buildspace",),
    )
    def edit_layout_ly(self, directory: Path) -> None:
        """
        Edits ``layout.ly``.
        """
        assert directory.is_buildspace()
        name, verb = "layout.ly", "open"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._open_files(paths)

    @Command(
        "lpe",
        description="layout.py - edit",
        menu_section="layout",
        score_package_paths=("buildspace",),
    )
    def edit_layout_py(self, directory: Path) -> None:
        """
        Edits ``layout.py``.
        """
        assert directory.is_buildspace()
        name, verb = "layout.py", "open"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._open_files(paths)

    @Command(
        "lp",
        description="log - lilypond",
        external_directories=True,
        menu_section="log",
        score_package_paths=True,
        scores_directory=True,
    )
    def edit_lilypond_log(self) -> None:
        """
        Edits ``lily.log``.
        """
        path = Path(abjad.abjad_configuration.lilypond_log_file_path)
        self._open_files([path])

    @Command(
        "le",
        description=".log - edit",
        menu_section="illustration",
        score_package_paths=("buildspace", "illustrationspace"),
    )
    def edit_log(self, directory: Path) -> None:
        """
        Edits ``.log``.
        """
        assert directory.is_buildspace()
        if (
            directory.is_material()
            or directory.is_segment()
            or directory.is_build()
        ):
            paths = [directory / ".log"]
        else:
            paths = []
            for path in directory.list_paths():
                illustration_ily = path / ".log"
                if illustration_ily.is_file():
                    paths.append(illustration_ily)
        self._open_files(paths, force_vim=True)

    @Command(
        "mle",
        description="music.ly - edit",
        menu_section="music",
        score_package_paths=("_segments", "build"),
    )
    def edit_music_ly(self, directory: Path) -> None:
        """
        Edits ``music.ly``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "music.ly", "open"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._open_files(paths)

    @Command(
        "oe",
        description=".optimization - edit",
        menu_section="illustration",
        score_package_paths=("illustrationspace",),
    )
    def edit_optimization(self, directory: Path) -> None:
        """
        Edits ``.optimization``.
        """
        assert directory.is_illustrationspace()
        if directory.is_material() or directory.is_segment():
            paths = [directory / ".optimization"]
        else:
            paths = []
            for path in directory.list_paths():
                optimization = path / ".optimization"
                if optimization.is_file():
                    paths.append(optimization)
        self._open_files(paths, force_vim=True)

    @Command(
        "pte",
        description="part.tex - edit",
        menu_section="parts",
        score_package_paths=("part", "parts"),
    )
    def edit_part_tex(self, directory: Path) -> None:
        """
        Edits ``part.tex``.
        """
        assert directory.is_parts() or directory.is_part()
        name, verb = "part.tex", "open"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._open_files(paths)

    @Command(
        "pfte",
        description="preface.tex - edit",
        menu_section="preface",
        score_package_paths=("_segments", "build"),
    )
    def edit_preface_tex(self, directory: Path) -> None:
        """
        Edits ``preface.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "preface.tex", "open"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._open_files(paths)

    @Command(
        "ste",
        description="score.tex - edit",
        menu_section="score",
        score_package_path_blacklist=("parts",),
        score_package_paths=("_segments", "build"),
    )
    def edit_score_tex(self, directory: Path) -> None:
        """
        Edits ``score.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        path = directory.build / "score.tex"
        self._open_files([path])

    @Command(
        "ssie",
        description="stylesheet.ily - edit",
        menu_section="stylesheet",
        score_package_paths=("_segments", "build"),
    )
    def edit_stylesheet_ily(self, directory: Path) -> None:
        """
        Edits ``stylesheet.ily``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        path = directory.build / "stylesheet.ily"
        self._open_files([path])

    @Command(
        "it",
        description="text - edit",
        external_directories=True,
        menu_section="text",
        score_package_paths=True,
        scores_directory=True,
    )
    def edit_text(self, directory: Path) -> None:
        """
        Opens Vim and goes to every occurrence of search string.
        """
        search_string = self.io.get("enter search string")
        if self.is_navigation(search_string):
            return
        if self.test:
            return
        with self.change(directory):
            options = "--sort-files --type=python"
            command = rf'vim -c "grep {search_string!s} {options}"'
            abjad.IOManager.spawn_subprocess(command)

    @Command(
        "cbe",
        description="clipboard - empty",
        external_directories=True,
        menu_section="clipboard",
        score_package_paths=True,
        scores_directory=True,
    )
    def empty_clipboard(self, directory: Path) -> None:
        """
        Empties clipboard.
        """
        if not bool(self.clipboard):
            self.io.display("clipboard is empty ...")
            return
        self.io.display("emptying clipboard ...")
        for path in self.clipboard:
            self.io.display(path.trim())
        self._clipboard[:] = []

    @Command(
        ";",
        description="show - column",
        external_directories=True,
        menu_section="show",
        score_package_paths=True,
        scores_directory=True,
    )
    def force_single_column(self) -> None:
        """
        Forces single-column display.
        """
        pass

    @Command(
        "bctg",
        description="back-cover.tex - generate",
        menu_section="back cover",
        score_package_paths=("_segments", "build"),
    )
    def generate_back_cover_tex(self, directory: Path) -> None:
        """
        Generates ``back-cover.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        name, verb = "back-cover.tex", "generate"
        # TODO:
        # if directory.is_part():
        #    file_name = f'{directory.name}-{name}'
        #    path = directory / file_name
        #    self._generate_back_cover_tex(path)
        #    return
        if not (directory.build.is_parts() or directory.build.is_part()):
            path = directory.build / name
            self._generate_back_cover_tex(path)
            return
        paths = self._select_paths_in_buildspace(
            directory, name, verb, supply_missing=True
        )
        if self.is_navigation(paths):
            return
        if not paths:
            return
        total_parts = len(directory.build._get_part_manifest())
        path_count = len(paths)
        for i, path in enumerate(paths):
            part = path.to_part()
            price = f"{part.identifier} ({part.number}/{total_parts})"
            self._generate_back_cover_tex(path, price=price)
            if i + 1 < path_count:
                self.io.display("")

    @Command(
        "fctg",
        description="front-cover.tex - generate",
        menu_section="front cover",
        score_package_paths=("_segments", "build"),
    )
    def generate_front_cover_tex(self, directory: Path) -> None:
        """
        Generates ``front-cover.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        name, verb = "front-cover.tex", "generate"
        # TODO:
        if directory.is_part():
            raise NotImplementedError()
            # file_name = f'{directory.name}-{name}'
            # path = directory / file_name
            # self._generate_front_cover_tex(path)
            # return
        if not directory.build.is_parts():
            path = directory.build / name
            self._generate_front_cover_tex(path)
            return
        paths = self._select_paths_in_buildspace(
            directory, name, verb, supply_missing=True
        )
        if self.is_navigation(paths):
            return
        if not paths:
            return
        path_count = len(paths)
        for i, path in enumerate(paths):
            part = path.to_part()
            forces_tagline = self._part_subtitle(part.name, parentheses=False)
            self._generate_front_cover_tex(path, forces_tagline=forces_tagline)
            if i + 1 < path_count:
                self.io.display("")

    @Command(
        "lpg",
        description="layout.py - generate",
        menu_section="layout",
        score_package_paths=("buildspace",),
    )
    def generate_layout_py(self, directory: Path) -> None:
        """
        Generates ``layout.py``.
        """
        assert directory.is_buildspace()
        name, verb = "layout.py", "generate"
        if directory.is_segment():
            self._copy_boilerplate(
                directory, "score_layout.py", target_name="layout.py"
            )
            return
        assert directory.build is not None
        if not directory.build.is_parts():
            self._copy_boilerplate(
                directory.build, "score_layout.py", target_name="layout.py"
            )
            return
        paths = self._select_paths_in_buildspace(
            directory, name, verb, supply_missing=True, underscores=True
        )
        if self.is_navigation(paths):
            return
        if not paths:
            return
        path_count = len(paths)
        for i, path in enumerate(paths):
            part = path.to_part()
            self._copy_boilerplate(
                path.parent,
                "part_layout.py",
                target_name=path.name,
                values={"part_identifier": part.identifier},
            )
            if 1 < path_count and i + 1 < path_count:
                self.io.display("")

    @Command(
        "mlg",
        description="music.ly - generate",
        menu_section="music",
        score_package_paths=("_segments", "build"),
    )
    def generate_music_ly(self, directory: Path) -> None:
        """
        Generates ``music.ly``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        name = "music.ly"
        if not (directory.build.is_parts() or directory.is_part()):
            path = directory.build / name
            self.io.display(f"generating {path.trim()} ...")
            self._generate_score_music_ly(path, indent=1)
            return
        else:
            name, verb = "music.ly", "generate"
            paths = self._select_paths_in_buildspace(directory, name, verb)
            if self.is_navigation(paths):
                return
            if not paths:
                return
            path_count = len(paths)
            for i, path in enumerate(paths):
                part = path.to_part()
                assert isinstance(part, abjad.Part)
                dashed_part_name = abjad.String(part.name).to_dash_case()
                file_name = f"{dashed_part_name}-{name}"
                assert path.build is not None
                path = path.build / file_name
                forces_tagline = self._part_subtitle(part.name) + " part"
                part_subtitle = self._part_subtitle(
                    part.name, parentheses=True
                )
                self._generate_part_music_ly(
                    path,
                    dashed_part_name=dashed_part_name,
                    forces_tagline=forces_tagline,
                    keep_with_tag=part.name,
                    part=part,
                    part_subtitle=part_subtitle,
                )
                if 0 < path_count and i + 1 < path_count:
                    self.io.display("")

    @Command(
        "ptg",
        description="part.tex - generate",
        menu_section="parts",
        score_package_paths=("part", "parts"),
    )
    def generate_part_tex(self, directory: Path) -> None:
        """
        Generates ``part.tex``.
        """
        assert directory.is_parts() or directory.is_part()
        name, verb = "part.tex", "generate"
        if directory.is_part():
            dashed_part_name = directory.name
            file_name = f"{dashed_part_name}-{name}"
            path = directory / file_name
            self._generate_part_tex(path, dashed_part_name)
            return
        paths = self._select_paths_in_buildspace(
            directory, name, verb, supply_missing=True
        )
        if self.is_navigation(paths):
            return
        if not paths:
            return
        path_count = len(paths)
        for i, path in enumerate(paths):
            part = path.to_part()
            dashed_part_name = abjad.String(part.name).to_dash_case()
            self._generate_part_tex(path, dashed_part_name)
            if 1 < path_count and i + 1 < path_count:
                self.io.display("")

    @Command(
        "pftg",
        description="preface.tex - generate",
        menu_section="preface",
        score_package_paths=("_segments", "build"),
    )
    def generate_preface_tex(self, directory: Path) -> None:
        """
        Generates ``preface.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        name, verb = "preface.tex", "generate"
        if directory.is_part():
            file_name = f"{directory.name}-{name}"
            path = directory / file_name
            self._generate_preface_tex(path)
            return
        if not directory.build.is_parts():
            path = directory.build / name
            self._generate_preface_tex(path)
            return
        paths = self._select_paths_in_buildspace(
            directory, name, verb, supply_missing=True
        )
        if self.is_navigation(paths):
            return
        if not paths:
            return
        for path in paths:
            self._generate_preface_tex(path)

    @Command(
        "stg",
        description="score.tex - generate",
        menu_section="score",
        score_package_path_blacklist=("parts",),
        score_package_paths=("_segments", "build"),
    )
    def generate_score_tex(self, directory: Path) -> None:
        """
        Generates ``score.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        self.io.display("generating score ...")
        path = directory.build / "score.tex"
        self._generate_document(path)

    @Command(
        "ssig",
        description="stylesheet.ily - generate",
        menu_section="stylesheet",
        score_package_paths=("_segments", "build"),
    )
    def generate_stylesheet_ily(self, directory: Path) -> None:
        """
        Generates build directory ``stylesheet.ily``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        self.io.display("generating stylesheet ...")
        values = {}
        paper_size = directory.build.get_metadatum("paper_size", "letter")
        values["paper_size"] = paper_size
        orientation = directory.build.get_metadatum("orientation", "")
        values["orientation"] = orientation
        self._copy_boilerplate(
            directory.build, "stylesheet.ily", values=values
        )

    @Command(
        "get",
        description="path - get",
        menu_section="path",
        score_package_path_blacklist=("contents",),
        score_package_paths=True,
    )
    def get(self, directory: Path) -> None:
        """
        Copies into ``directory``.
        """
        items = []
        if directory.is_material_or_segment():
            siblings = directory.parent.list_paths()
            siblings.remove(directory)
            for sibling in siblings:
                definition = sibling / "definition.py"
                if definition.is_file():
                    items.append((definition.trim(), definition))
            label = directory.get_asset_type()
            header = directory.get_header()
            header += f" : get {label} ..."
        if not items:
            scores_directory = directory.scores
            assert scores_directory is not None
            for path in scores_directory.list_paths():
                items.append((path.get_identifier(), path))
            label = abjad.String(directory.get_asset_type()).pluralize()
            header = directory.get_header() + f" : get {label} from ..."
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
                self.io.display(f"matches no score {response.string!r} ...")
                return
            if isinstance(response.payload, list):
                assert len(response.payload) == 1, repr(response)
                score = response.payload[0]
            else:
                score = response.payload
            cousin = directory.with_score(score.name)
            assert cousin is not None
            items = []
            if directory.is_material_or_segment():
                cousins = cousin.parent.list_paths()
                cousins.remove(cousin)
                for cousin in cousins:
                    definition = cousin / "definition.py"
                    if definition.is_file():
                        items.append((definition.trim(), definition))
                label = directory.get_asset_type()
            else:
                for path in cousin.list_paths():
                    items.append((path.get_identifier(), path))
            header = directory.get_header()
            header += f" : get {score.get_identifier()} {label} ..."
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
            self.io.display(f"matches no {label} {response.string!r} ...")
            return
        if isinstance(response.payload, Path):
            paths = [response.payload]
        else:
            paths = response.payload
        if len(paths) == 1:
            self.io.display(f"getting {paths[0].trim()} ...")
        else:
            self.io.display(f"getting ...")
            for path in paths:
                self.io.display(f"    {path.trim()}")
        targets = []
        for source in paths:
            target = directory / source.name
            if target.exists():
                self.io.display(f"existing {target.trim()} ...")
                name = self.io.get("enter new name")
                if self.is_navigation(name):
                    return
                suffix = source.suffix
                name = source.parent.coerce(name, suffix=suffix)
                target = target.with_name(name)
                if target.exists():
                    self.io.display(f"existing {target.trim()} ...")
                    return
            targets.append(target)
        assert targets
        if len(targets) == 1:
            self.io.display(f"will write {targets[0].trim()} ...")
        else:
            self.io.display(f"will write ...")
            for target in targets:
                self.io.display(f"    {target.trim()} ...")
        response = self.io.get("ok?")
        if self.is_navigation(response):
            return
        if response != "y":
            return
        for source, target in zip(paths, targets):
            self.io.display(f"writing {target.trim()} ...")
            if source.is_file():
                shutil.copyfile(str(source), str(target))
            elif source.is_dir():
                shutil.copytree(str(source), str(target))
            else:
                raise ValueError(source)
            if source.is_material_or_segment() and source.get_metadatum(
                "name"
            ):
                name = self.io.get("name metadatum")
                if self.is_navigation(name):
                    return
                if name:
                    target.add_metadatum("name", name)
                else:
                    target.remove_metadatum("name")

    @Command(
        "ci",
        description="git - commit",
        external_directories=True,
        menu_section="git",
        score_package_paths=True,
        scores_directory=True,
    )
    def git_commit(self, directory: Path, commit_message: str = None) -> None:
        """
        Commits working copy.
        """
        if not directory.is_scores():
            root = directory._get_repository_root()
            if not root:
                self.io.display(f"missing {directory.trim()} repository ...")
                return
            with self.change(root):
                if not root._has_pending_commit():
                    self.io.display("nothing to commit ...")
                    return
                self.git_status(root)
                if self.test:
                    return
                command = f"git add -A {root}"
                self.io.display(f"Running {command} ...")
                lines = abjad.IOManager.run_command(command)
                self.io.display(lines, raw=True)
                if commit_message is None:
                    commit_message = self.io.get("commit message")
                    assert isinstance(commit_message, str)
                    if self.is_navigation(commit_message):
                        return
                command = f'git commit -m "{commit_message}" {root}'
                command += "; git push"
                lines = abjad.IOManager.run_command(command)
                self.io.display(lines, raw=True)
        else:
            assert directory.is_scores()
            commit_message = self.io.get("commit message")
            assert isinstance(commit_message, str)
            if self.is_navigation(commit_message):
                return
            paths = directory.list_paths()
            for i, path in enumerate(paths):
                self.io.display(f"{path} ...")
                self.git_commit(path, commit_message=commit_message)
                if i + 1 < len(paths):
                    self.io.display("")

    @Command(
        "diff",
        description="git - diff",
        external_directories=True,
        menu_section="git",
        score_package_paths=True,
        scores_directory=True,
    )
    def git_diff(self, directory: Path) -> None:
        """
        Displays Git diff of working copy.
        """
        if not directory.is_scores():
            if not directory._get_repository_root():
                self.io.display(f"missing {directory.trim()} repository ...")
                return
            with self.change(directory):
                command = "git diff ."
                self.io.display(f"Running {command} ...")
                abjad.IOManager.spawn_subprocess(command)
        else:
            assert directory.is_scores()
            paths = directory.list_paths()
            for i, path in enumerate(paths):
                self.io.display(f"{path} ...")
                self.git_diff(path)
                if i + 1 < len(paths):
                    self.io.display("")

    @Command(
        "pull",
        description="git - pull",
        external_directories=True,
        menu_section="git",
        score_package_paths=True,
        scores_directory=True,
    )
    def git_pull(self, directory: Path) -> None:
        """
        Pulls working copy.
        """
        if not directory.is_scores():
            root = directory._get_repository_root()
            if not root:
                self.io.display(f"missing {directory.trim()} repository ...")
                return
            with self.change(root):
                command = f"git pull"
                self.io.display(f"Running {command} ...")
                if self.test:
                    return
                lines = abjad.IOManager.run_command(command)
                if lines and "Already up to date" in lines[-1]:
                    lines = lines[-1:]
                self.io.display(lines)
                command = "git submodule foreach git pull origin master"
                self.io.display(f"Running {command} ...")
                lines = abjad.IOManager.run_command(command)
                if lines and "Already up to date" in lines[-1]:
                    lines = lines[-1:]
                self.io.display(lines)
        else:
            assert directory.is_scores()
            paths = directory.list_paths()
            for i, path in enumerate(paths):
                self.io.display(f"{path} ...")
                self.git_pull(path)
                if i + 1 < len(paths):
                    self.io.display("")

    @Command(
        "push",
        description="git - push",
        external_directories=True,
        menu_section="git",
        score_package_paths=True,
        scores_directory=True,
    )
    def git_push(self, directory: Path) -> None:
        """
        Pushes working copy.
        """
        if not directory.is_scores():
            root = directory._get_repository_root()
            if not root:
                self.io.display(f"missing {directory.trim()} repository ...")
                return
            with self.change(root):
                command = "git push"
                self.io.display(f"Running {command} ...")
                if self.test:
                    return
                abjad.IOManager.spawn_subprocess(command)
        else:
            assert directory.is_scores()
            paths = directory.list_paths()
            for i, path in enumerate(paths):
                self.io.display(f"{path} ...")
                self.git_push(path)
                if i + 1 < len(paths):
                    self.io.display("")

    @Command(
        "st",
        description="git - status",
        external_directories=True,
        menu_section="git",
        score_package_paths=True,
        scores_directory=True,
    )
    def git_status(self, directory: Path) -> None:
        """
        Displays Git status of working copy.
        """
        if not directory.is_scores():
            if not directory._get_repository_root():
                self.io.display(f"missing {directory.trim()} repository ...")
                return
            with self.change(directory):
                command = "git status ."
                self.io.display(f"Running {command} ...")
                lines = abjad.IOManager.run_command(command)
                lines = [_ for _ in lines if _ != ""]
                self.io.display(lines)
                command = "git submodule foreach git fetch"
                self.io.display(f"Running {command} ...")
                abjad.IOManager.spawn_subprocess(command)
        else:
            assert directory.is_scores()
            paths = directory.list_paths()
            for i, path in enumerate(paths):
                self.io.display(f"{path} ...")
                self.git_status(path)
                if i + 1 < len(paths):
                    self.io.display("")

    @Command(
        "-",
        description="go - back",
        external_directories=True,
        menu_section="go",
        score_package_paths=True,
        scores_directory=True,
    )
    def go_back(self) -> None:
        """
        Goes back.
        """
        if self.previous_directory:
            self._manage_directory(self.previous_directory)
        else:
            self._manage_directory(self.current_directory)

    @Command(
        "bb",
        description="directory - builds",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_builds_directory(self, directory: Path) -> None:
        """
        Goes to builds directory.
        """
        assert directory.is_score_package_path()
        assert directory.builds is not None
        assert directory.builds._assets is not None
        if not directory.builds._assets.exists():
            self._make__assets_directory(directory.builds)
        if not (directory.builds / "__metadata__.py").is_file():
            directory.builds.write_metadata_py(abjad.OrderedDict())
        self._manage_directory(directory.builds)

    @Command(
        "cc",
        description="directory - contents",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_contents_directory(self, directory: Path) -> None:
        """
        Goes to contents directory.
        """
        assert directory.is_score_package_path()
        self._manage_directory(directory.contents)

    @Command(
        "%",
        description="go - directory",
        external_directories=True,
        menu_section="go",
        score_package_paths=True,
        scores_directory=True,
    )
    def go_to_directory(
        self, directory: Path, pattern: str = None, payload: typing.List = None
    ) -> None:
        """
        Goes to directory.
        """
        assert directory.is_dir()
        if Path.is_segment_name(pattern):
            address = pattern
        else:
            address = "%" + (pattern or "")
        if self.aliases and pattern in self.aliases:
            path = Path(self.aliases[pattern])
            self.io.display(f"matching {address!r} to {path.trim()} ...")
            self._manage_directory(path)
            return
        if isinstance(payload, Path):
            path = payload
            self.io.display(f"matching {address!r} to {path.trim()} ...")
            self._manage_directory(path)
            return
        if isinstance(payload, list) and len(payload) == 1:
            path = payload[0]
            self.io.display(f"matching {address!r} to {path.trim()} ...")
            self._manage_directory(path)
            return
        if isinstance(payload, list):
            assert all(isinstance(_, Path) for _ in payload), repr(payload)
            paths = payload
            counter = abjad.String("directory").pluralize(len(paths))
            message = f"matching {address!r} to {len(paths)} {counter} ..."
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
        for path in sorted(root.glob("**/*")):
            if "__pycache__" in str(path):
                continue
            if not path.is_dir():
                continue
            paths.append(path)
            strings.append(path.name)
        if isinstance(pattern, str):
            indices = abjad.String.match_strings(strings, pattern)
            paths = list(abjad.Sequence(paths).retain(indices))
            for index, path in zip(indices, paths):
                if path.name == address:
                    indices = [index]
                    paths = [path]
                    break
        if len(paths) == 1:
            self.io.display(f"matching {address!r} to {paths[0].trim()} ...")
        else:
            counter = abjad.String("directory").pluralize(len(paths))
            message = f"matching {address!r} to {len(paths)} {counter} ..."
            self.io.display(message)
            for path in paths:
                self.io.display(path.trim(), raw=True)
        if paths:
            self._manage_directory(paths[0])

    @Command(
        "dd",
        description="directory - distribution",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_distribution_directory(self, directory: Path) -> None:
        """
        Goes to distribution directory.
        """
        assert directory.is_score_package_path()
        assert directory.distribution is not None
        self._manage_directory(directory.distribution)

    @Command(
        "ee",
        description="directory - etc",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_etc_directory(self, directory: Path) -> None:
        """
        Goes to etc directory.
        """
        assert directory.is_score_package_path()
        assert directory.etc is not None
        self._manage_directory(directory.etc)

    @Command(
        "mm",
        description="directory - materials",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_materials_directory(self, directory: Path) -> None:
        """
        Goes to materials directory.
        """
        assert directory.is_score_package_path()
        assert directory.materials is not None
        self._manage_directory(directory.materials)

    @Command(
        ">",
        description="hop - next package",
        menu_section="hop",
        score_package_paths=("material", "materials", "segment", "segments"),
    )
    def go_to_next_package(self, directory: Path) -> None:
        """
        Goes to next package.
        """
        assert (
            directory.is_material_or_segment()
            or directory.is_materials_or_segments()
        )
        next_package = directory.get_next_package(cyclic=True)
        self._manage_directory(next_package)

    @Command(
        ">>",
        description="hop - next score",
        menu_section="hop",
        score_package_paths=True,
        scores_directory=True,
    )
    def go_to_next_score(self, directory: Path) -> None:
        """
        Goes to next score.
        """
        assert directory.is_score_package_path() or directory.is_scores()
        wrapper = directory.get_next_score(cyclic=True)
        assert wrapper is not None
        self._manage_directory(wrapper.contents)

    @Command(
        "<",
        description="hop - previous package",
        menu_section="hop",
        score_package_paths=("material", "materials", "segment", "segments"),
    )
    def go_to_previous_package(self, directory: Path) -> None:
        """
        Goes to previous package.
        """
        assert (
            directory.is_material_or_segment()
            or directory.is_materials_or_segments()
        )
        previous_package = directory.get_previous_package(cyclic=True)
        self._manage_directory(previous_package)

    @Command(
        "<<",
        description="hop - previous score",
        menu_section="hop",
        score_package_paths=True,
        scores_directory=True,
    )
    def go_to_previous_score(self, directory: Path) -> None:
        """
        Goes to previous score.
        """
        assert directory.is_score_package_path() or directory.is_scores()
        wrapper = directory.get_previous_score(cyclic=True)
        assert wrapper is not None
        self._manage_directory(wrapper.contents)

    @Command(
        "ss",
        description="go - scores",
        external_directories=True,
        menu_section="go",
        score_package_paths=True,
        scores_directory=True,
    )
    def go_to_scores_directory(self) -> None:
        """
        Goes to scores directory.
        """
        directory = self.configuration.composer_scores_directory
        if self.test or self.example:
            directory = self.configuration.test_scores_directory
        self._manage_directory(directory)

    @Command(
        "gg",
        description="directory - segments",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_segments_directory(self, directory: Path) -> None:
        """
        Goes to segments directory.
        """
        assert directory.is_score_package_path()
        assert directory.segments is not None
        self._manage_directory(directory.segments)

    @Command(
        "yy",
        description="directory - stylesheets",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_stylesheets_directory(self, directory: Path) -> None:
        """
        Goes to stylesheets directory.
        """
        assert directory.is_score_package_path()
        assert directory.stylesheets is not None
        self._manage_directory(directory.stylesheets)

    @Command(
        "tt",
        description="directory - test",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_test_directory(self, directory: Path) -> None:
        """
        Goes to test directory.
        """
        assert directory.is_score_package_path()
        assert directory.test is not None
        self._manage_directory(directory.test)

    @Command(
        "oo",
        description="directory - tools",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_tools_directory(self, directory: Path) -> None:
        """
        Goes to tools directory or tools.py module.
        """
        assert directory.is_score_package_path()
        assert directory.tools is not None
        if directory.tools.exists():
            self._manage_directory(directory.tools)
        else:
            path = directory.contents / "tools.py"
            self._open_files([path])
            self._manage_directory(directory)

    @Command(
        "ww",
        description="directory - wrapper",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_wrapper_directory(self, directory: Path) -> None:
        """
        Goes to wrapper directory.
        """
        assert directory.is_score_package_path()
        self._manage_directory(directory.wrapper)

    @Command(
        "..",
        description="go - up",
        external_directories=True,
        menu_section="go",
        score_package_paths=True,
        scores_directory=True,
    )
    def go_up(self) -> None:
        """
        Goes up.
        """
        if self.current_directory:
            self._manage_directory(self.current_directory.parent)

    @Command(
        "aimh",
        description=f"all invisible music - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_all_invisible_music(self, directory: Path) -> None:
        """
        Hides all invisible music.
        """
        assert directory.is_buildspace()
        tag = abjad.tags.INVISIBLE_MUSIC_COMMAND
        self.run(abjad.Job.show_tag(directory, tag))
        tag = abjad.tags.INVISIBLE_MUSIC_COLORING
        self.run(abjad.Job.show_tag(directory, tag, undo=True))

    @Command(
        "ash",
        description=f"annotation spanners - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_annotation_spanners(self, directory: Path) -> None:
        """
        Hides annotation spanners.
        """
        assert directory.is_buildspace()
        tags_ = abjad.tags.annotation_spanner_tags()

        def match(tags):
            return bool(set(tags) & set(tags_))

        name = "annotation spanners"
        self.run(abjad.Job.show_tag(directory, name, match=match, undo=True))

    @Command(
        "cth",
        description=f"clock time - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_clock_time(self, directory: Path) -> None:
        """
        Hides clock time.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.show_clock_time_markup(directory, undo=True))

    @Command(
        "fnh",
        description=f"figure names - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_figure_names(self, directory: Path) -> None:
        """
        Hides figure names.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.show_figure_name_markup(directory, undo=True))

    @Command(
        "lmnh",
        description=f"local measure numbers - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_local_measure_numbers(self, directory: Path) -> None:
        """
        Hides local measure numbers.
        """
        assert directory.is_buildspace()
        self.run(
            abjad.Job.show_local_measure_number_markup(directory, undo=True)
        )

    @Command(
        "mnh",
        description=f"measure numbers - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_measure_numbers(self, directory: Path) -> None:
        """
        Hides measure numbers.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.show_measure_number_markup(directory, undo=True))

    @Command(
        "mmh",
        description=f"mock music - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_mock_music(self, directory: Path) -> None:
        """
        Hides mock music.
        """
        assert directory.is_buildspace()
        tag = abjad.tags.MOCK_COLORING
        self.run(abjad.Job.show_tag(directory, tag, undo=True))

    @Command(
        "mah",
        description=f"music annotations - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_music_annotations(self, directory: Path) -> None:
        """
        Hides music annotations.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.show_music_annotations(directory, undo=True))

    @Command(
        "nyph",
        description=f"not yet pitched - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_not_yet_pitched_music(self, directory: Path) -> None:
        """
        Hides not yet pitched.
        """
        assert directory.is_buildspace()
        tag = abjad.tags.NOT_YET_PITCHED_COLORING
        self.run(abjad.Job.show_tag(directory, tag, undo=True))

    @Command(
        "rash",
        description=f"rhythm annotation spanners - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_rhythm_annotation_spanners(self, directory: Path) -> None:
        """
        Hides rhythm annotation spanners.
        """
        assert directory.is_buildspace()
        name = "rhythm annotation spanners"
        self.run(
            abjad.Job.show_tag(
                directory, abjad.tags.RHYTHM_ANNOTATION_SPANNER, undo=True
            )
        )

    @Command(
        "sph",
        description=f"spacing - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_spacing(self, directory: Path) -> None:
        """
        Hides spacing.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.show_spacing_markup(directory, undo=True))

    @Command(
        "snh",
        description=f"stage numbers - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_stage_numbers(self, directory: Path) -> None:
        """
        Hides stage numbers.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_stage_number_markup(directory, undo=True))

    @Command(
        "th",
        description=f"tag - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_tag(self, directory: Path) -> None:
        """
        Hides arbitrary (user-specified) tag.
        """
        assert directory.is_buildspace()
        tag_ = self.io.get("tag")
        if self.is_navigation(tag_):
            return
        tag = abjad.Tag(tag_)
        self.run(abjad.Job.show_tag(directory, tag, undo=True))

    @Command(
        "bcti",
        description="back-cover.tex - interpret",
        menu_section="back cover",
        score_package_paths=("_segments", "build"),
    )
    def interpret_back_cover_tex(
        self, directory: Path, open_after: bool = True
    ) -> None:
        """
        Interprets ``back-cover.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "back-cover.tex", "interpret"
        paths = self._select_paths_in_buildspace(directory.build, name, verb)
        if self.is_navigation(paths):
            return
        if not paths:
            return
        for path in paths:
            self._interpret_tex_file(path)
        if len(paths) == 1:
            target = path.with_suffix(".pdf")
            if target.is_file() and open_after:
                self._open_files([target])

    @Command(
        "fcti",
        description="front-cover.tex - interpret",
        menu_section="front cover",
        score_package_paths=("_segments", "build"),
    )
    def interpret_front_cover_tex(
        self, directory: Path, open_after: bool = True
    ) -> None:
        """
        Interprets ``front-cover.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "front-cover.tex", "interpret"
        paths = self._select_paths_in_buildspace(directory.build, name, verb)
        if not paths:
            return
        for path in paths:
            self._interpret_tex_file(path)
        if len(paths) == 1:
            target = path.with_suffix(".pdf")
            if target.is_file() and open_after:
                self._open_files([target])

    @Command(
        "ili",
        description="illustration.ly - interpret",
        menu_section="illustration",
        score_package_paths=("illustrationspace",),
    )
    def interpret_illustration_ly(
        self, directory: Path, open_after: bool = True
    ) -> None:
        """
        Interprets ``illustration.ly``.

        Makes ``illustration.pdf``.
        """
        assert directory.is_illustrationspace()
        if directory.is_material() or directory.is_segment():
            self.io.display("interpreting ly ...")
            source = directory / "illustration.ly"
            target = source.with_suffix(".pdf")
            if source.is_file():
                self._run_lilypond(source)
            else:
                self.io.display(f"missing {source.trim()} ...")
            if target.is_file() and open_after:
                self._open_files([target])
        else:
            paths = directory.list_paths()
            path_count = len(paths)
            with abjad.Timer() as timer:
                for i, path in enumerate(paths):
                    self.interpret_illustration_ly(path, open_after=False)
                    if i + 1 < path_count:
                        self.io.display("")
            self.io.display(timer.total_time_message)

    @Command(
        "mli",
        description="music.ly - interpret",
        menu_section="music",
        score_package_paths=("_segments", "build"),
    )
    def interpret_music_ly(
        self,
        directory: Path,
        do_not_collect_segments: bool = False,
        do_not_generate_music: bool = False,
        open_after: bool = True,
    ) -> None:
        """
        Interprets ``music.ly``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "music.ly", "interpret"
        paths = self._select_paths_in_buildspace(directory.build, name, verb)
        if self.is_navigation(paths):
            return
        if not paths:
            return
        path_count = len(paths)
        for i, path in enumerate(paths):
            if path.parent.is_score_build():
                if not do_not_collect_segments or not do_not_generate_music:
                    self.io.display(f"preparing {path.trim()} ...")
                if not do_not_collect_segments:
                    self.collect_segments(path.parent)
                if not do_not_generate_music:
                    self.generate_music_ly(path.parent)
            if path.parent.is_part():
                self.io.display(f"preparing {path.trim()} ...")
                self._activate_part_specific_tags(path)
            music_time_signatures = path.parent.get_time_signature_metadata()
            music_time_signatures = [str(_) for _ in music_time_signatures]
            layout_ly = path.name.replace("music.ly", "layout.ly")
            layout_ly = path.parent / layout_ly
            if layout_ly.exists():
                layout_time_signatures = (
                    layout_ly.get_preamble_time_signatures()
                )
                partial_score = layout_ly.get_preamble_partial_score()
                if not partial_score and (
                    music_time_signatures != layout_time_signatures
                ):
                    message = f"music time signatures"
                    message += f" ({len(music_time_signatures)})"
                    message += " do not match layout time signatures"
                    message += f" ({len(layout_time_signatures)}) ..."
                    if not self.test:
                        self.io.display(message)
                        self.io.display(f"remaking {layout_ly.trim()} ...")
                        layout_py = layout_ly.with_suffix(".py")
                        self._make_layout_ly(layout_py)
                        layout_time_signatures = (
                            layout_ly.get_preamble_time_signatures()
                        )
                        if music_time_signatures != layout_time_signatures:
                            message = "music time signatures"
                            message += f" ({len(music_time_signatures)})"
                            message += " still do not match"
                            message += " layout time signatures"
                            message += f" ({len(layout_time_signatures)}) ..."
                            self.io.display(message)
                            return
            self._run_lilypond(path)
            if 0 < path_count and i + 1 < path_count:
                self.io.display("")
        if len(paths) == 1:
            target = path.with_suffix(".pdf")
            if target.is_file() and open_after:
                self._open_files([target])

    @Command(
        "pti",
        description="part.tex - interpret",
        menu_section="parts",
        score_package_paths=("part", "parts"),
    )
    def interpret_part_tex(
        self, directory: Path, open_after: bool = True
    ) -> None:
        """
        Interprets ``part.tex``.
        """
        assert directory.is_parts() or directory.is_part()
        name, verb = "part.tex", "interpret"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if not paths:
            return
        path_count = len(paths)
        for i, path in enumerate(paths):
            self._interpret_tex_file(path)
            if 1 < path_count and i + 1 < path_count:
                self.io.display("")
        if len(paths) == 1:
            target = path.with_suffix(".pdf")
            if target.is_file() and open_after:
                self._open_files([target])

    @Command(
        "pfti",
        description="preface.tex - interpret",
        menu_section="preface",
        score_package_paths=("_segments", "build"),
    )
    def interpret_preface_tex(
        self, directory: Path, open_after: bool = True
    ) -> None:
        """
        Interprets ``preface.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "preface.tex", "interpret"
        paths = self._select_paths_in_buildspace(directory.build, name, verb)
        if not paths:
            return
        for path in paths:
            self._interpret_tex_file(path)
        if len(paths) == 1:
            target = path.with_suffix(".pdf")
            if target.is_file() and open_after:
                self._open_files([target])

    @Command(
        "sti",
        description="score.tex - interpret",
        menu_section="score",
        score_package_path_blacklist=("parts",),
        score_package_paths=("_segments", "build"),
    )
    def interpret_score_tex(
        self, directory: Path, open_after: bool = True
    ) -> None:
        """
        Interprets ``score.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "score.tex", "interpret"
        paths = self._select_paths_in_buildspace(directory.build, name, verb)
        if not paths:
            return
        for path in paths:
            self._interpret_tex_file(path)
        if len(paths) == 1:
            target = path.with_suffix(".pdf")
            if target.is_file() and open_after:
                self._open_files([target])

    @Command(
        "ilm",
        description="illustration.ly - make",
        menu_section="illustration",
        score_package_paths=("illustrationspace",),
    )
    def make_illustration_ly(self, directory: Path) -> None:
        """
        Makes ``illustration.ly``.
        """
        assert directory.is_illustrationspace()
        if directory.is_material() or directory.is_segment():
            if directory.is_material():
                self._make_material_ly(directory)
            else:
                assert directory.is_segment()
                self._make_segment_ly(directory)
        else:
            paths = directory.list_paths()
            path_count = len(paths)
            with abjad.Timer() as timer:
                for i, path in enumerate(paths):
                    self.make_illustration_ly(path)
                    if 1 < path_count and i + 1 < path_count:
                        self.io.display("")
            self.io.display(timer.total_time_message)

    @Command(
        "ipm",
        description="illustration.pdf - make",
        menu_section="illustration",
        score_package_paths=("illustrationspace",),
    )
    def make_illustration_pdf(
        self, directory: Path, layout: bool = True, open_after: bool = True
    ) -> int:
        """
        Makes ``illustration.pdf``.

        Returns integer exit code for Travis tests.
        """
        assert directory.is_illustrationspace()
        if directory.is_material():
            return self._make_material_pdf(directory, open_after=open_after)
        elif directory.is_segment():
            return self._make_segment_pdf(
                directory, layout=layout, open_after=open_after
            )
        else:
            assert directory.is_materials() or directory.is_segments()
            exit = 0
            paths = directory.list_paths()
            paths = [_ for _ in paths if _.is_dir()]
            path_count = len(paths)
            for i, path in enumerate(paths):
                exit_ = self.make_illustration_pdf(path, open_after=False)
                if i + 1 < len(paths):
                    self.io.display("")
                else:
                    abjad.IOManager.spawn_subprocess('say "done"')
                if exit_ != 0:
                    exit = -1
            return exit
        return 0

    @Command(
        "llm",
        description="layout.ly - make",
        menu_section="layout",
        score_package_paths=("buildspace",),
    )
    def make_layout_ly(self, directory: Path) -> None:
        """
        Makes ``layout.ly``.
        """
        assert directory.is_buildspace()
        if directory.is__segments():
            buildspace = directory.build
        else:
            buildspace = directory
        name, verb = "layout.py", "interpret"
        paths = self._select_paths_in_buildspace(buildspace, name, verb)
        if self.is_navigation(paths):
            return
        if not paths:
            return
        path_count = len(paths)
        for i, layout_py in enumerate(paths):
            self.io.display(f"{verb}ing {layout_py.trim()} ...")
            layout_ly = layout_py.with_suffix(".ly")
            if not layout_py.is_file():
                self.io.display(f"missing {layout_py.trim()} ...")
                continue
            self._make_layout_ly(layout_py)
            if i < path_count - 1:
                self.io.display("")

    @Command(
        "midm",
        description="segment.midi - make",
        menu_section="segment.midi",
        score_package_paths=("segment",),
    )
    def make_segment_midi(
        self, directory: Path, open_after: bool = True
    ) -> int:
        """
        Makes segment MIDI file.

        Returns integer exit code for Travis tests.
        """
        assert directory.is_segment()
        return self._make_segment_midi(directory, open_after=open_after)

    @Command(
        "mypy",
        description="package - mypy",
        external_directories=True,
        menu_section="package",
        score_package_paths=True,
        scores_directory=True,
    )
    def mypy(self, directory: Path) -> None:
        """
        Runs mypy --ignore-missing-imports on package.
        """
        if self.test:
            return
        command = f"mypy --ignore-missing-imports"
        if not directory.is_scores():
            root = directory._get_repository_root()
            if not root:
                self.io.display(f"missing {directory.trim()} repository ...")
                return
            with self.change(root):
                self.io.display(f"Running {command} on {root} ...")
                lines = abjad.IOManager.run_command(f"{command} {root}")
                self.io.display(lines, raw=True, wrap=True)
        else:
            assert directory.is_scores()
            paths = directory.list_paths()
            for i, path in enumerate(paths):
                self.io.display(f"Running {command} on {path} ...")
                lines = abjad.IOManager.run_command(f"{command} {path}")
                self.io.display(lines, raw=True, wrap=True)
                if i + 1 < len(paths):
                    self.io.display("")

    @Command(
        "ipn",
        description="illustration.pdf - nake",
        menu_section="illustration",
        score_package_paths=("illustrationspace",),
    )
    def nake_illustration_pdf(self, directory: Path) -> int:
        """
        Makes ``illustration.pdf``; does not reinterpret ``layout.py``;
        does not open after.

        Returns integer exit code for Travis tests.
        """
        assert directory.is_illustrationspace()
        return self.make_illustration_pdf(
            directory, layout=False, open_after=False
        )

    @Command(
        "new",
        description="path - new",
        external_directories=True,
        menu_section="path",
        score_package_path_blacklist=("contents",),
        score_package_paths=True,
        scores_directory=True,
    )
    def new(self, directory: Path) -> None:
        """
        Makes asset.
        """
        if directory.is_builds():
            type_ = self.io.get("score or parts?")
            if self.is_navigation(type_):
                return
            if type_ == "score":
                self._make_score_build_directory(directory)
            elif type_ == "parts":
                self._make_parts_directory(directory)
        elif directory.is_materials_or_segments():
            self._make_package(directory)
        elif directory.is_scores():
            self._make_score_package()
        else:
            self._make_file(directory)

    @Command(
        "**",
        description="all - pdfs",
        external_directories=True,
        menu_section="all",
        score_package_paths=True,
        scores_directory=True,
    )
    def open_all_pdfs(self, directory: Path, pattern: str = None) -> None:
        """
        Opens all PDFs.
        """
        files, strings = directory._find_pdfs(force=True)
        files = self._match_files(files, strings, pattern, "**")
        self._open_files(files)

    @Command(
        "bcpo",
        description="back-cover.pdf - open",
        menu_section="back cover",
        score_package_paths=("_segments", "build"),
    )
    def open_back_cover_pdf(self, directory: Path) -> None:
        """
        Opens ``back-cover.pdf``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "back-cover.pdf", "open"
        paths = self._select_paths_in_buildspace(directory.build, name, verb)
        if self.is_navigation(paths):
            return
        self._open_files(paths)

    @Command(
        "fcpo",
        description="front-cover.pdf - open",
        menu_section="front cover",
        score_package_paths=("_segments", "build"),
    )
    def open_front_cover_pdf(self, directory: Path) -> None:
        """
        Opens ``front-cover.pdf``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "front-cover.pdf", "open"
        paths = self._select_paths_in_buildspace(directory.build, name, verb)
        if self.is_navigation(paths):
            return
        self._open_files(paths)

    @Command(
        "ipo",
        description="illustration.pdf - open",
        menu_section="illustration",
        score_package_paths=("illustrationspace",),
    )
    def open_illustration_pdf(self, directory: Path) -> None:
        """
        Opens ``illustration.pdf``.
        """
        assert directory.is_illustrationspace()
        if directory.is_material() or directory.is_segment():
            path = directory / "illustration.pdf"
            self._open_files([path])
        else:
            for path in directory.list_paths():
                self.open_illustration_pdf(path)

    @Command(
        "mpo",
        description="music.pdf - open",
        menu_section="music",
        score_package_paths=("_segments", "build"),
    )
    def open_music_pdf(self, directory: Path) -> None:
        """
        Opens ``music.pdf``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "music.pdf", "open"
        paths = self._select_paths_in_buildspace(directory.build, name, verb)
        if self.is_navigation(paths):
            return
        if not paths:
            return
        self._open_files(paths)

    @Command(
        "ppo",
        description="part.pdf - open",
        menu_section="parts",
        score_package_paths=("part", "parts"),
    )
    def open_part_pdf(self, directory: Path) -> None:
        """
        Opens ``part.pdf``.
        """
        assert directory.is_parts() or directory.is_part()
        name, verb = "part.pdf", "open"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._open_files(paths)

    @Command(
        "pfpo",
        description="preface.pdf - open",
        menu_section="preface",
        score_package_paths=("_segments", "build"),
    )
    def open_preface_pdf(self, directory: Path) -> None:
        """
        Opens ``preface.pdf``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "preface.pdf", "open"
        paths = self._select_paths_in_buildspace(directory.build, name, verb)
        if self.is_navigation(paths):
            return
        self._open_files(paths)

    @Command(
        "spo",
        description="score.pdf - open",
        menu_section="score",
        score_package_paths=True,
        scores_directory=True,
    )
    def open_score_pdf(self, directory: Path) -> None:
        """
        Opens ``score.pdf``.
        """
        if directory.is_scores():
            score_pdfs = []
            for path in directory.list_paths():
                score_pdf = path._get_score_pdf()
                if score_pdf:
                    score_pdfs.append(score_pdf)
            self._open_files(score_pdfs)
        elif directory.is_build() and not directory.is_parts():
            name = "score.pdf"
            paths = directory.get_files_ending_with(name)
            if paths:
                self._open_files(paths)
            else:
                self.io.display(f"no files ending in *{name} ...")
        else:
            assert directory.is_score_package_path()
            path = directory._get_score_pdf()
            if path:
                self._open_files([path])
            else:
                message = "missing score PDF"
                message += " in distribution and build directories ..."
                self.io.display(message)

    @Command(
        "cbv",
        description="clipboard - paste",
        external_directories=True,
        menu_section="clipboard",
        score_package_paths=True,
        scores_directory=True,
    )
    def paste_from_clipboard(self, directory: Path) -> None:
        """
        Pastes from clipboard.
        """
        if not bool(self.clipboard):
            self.io.display("showing empty clipboard ...")
            return
        self.io.display("pasting from clipboard ...")
        for i, source in enumerate(self.clipboard[:]):
            self.io.display(f"    {source.trim()} ...")
            target = directory / source.name
            self.io.display(f"    {target.trim()} ...")
            if target.exists():
                self.io.display(["", f"existing {target.trim()} ..."])
                name = self.io.get("enter new name")
                if self.is_navigation(name):
                    return
                if not bool(name):
                    continue
                target = target.with_name(name)
                if target.exists():
                    self.io.display(f"existing {target.trim()} ...")
                    return
                self.io.display(f"    {source.trim()} ...")
                self.io.display(f"    {target.trim()} ...")
            if source.is_dir():
                shutil.copytree(str(source), str(target))
            else:
                shutil.copy(str(source), str(target))
            if i < len(self.clipboard) - 1:
                self.io.display("")

    @Command(
        "lpp",
        description="layout.py - propagate",
        menu_section="layout",
        score_package_paths=("parts",),
    )
    def propagate_layout_py(self, directory: Path) -> None:
        """
        Propagates ``layout.py``.
        """
        assert directory.is_parts() or directory.is_part()
        name, verb = "layout.py", "use as source"
        paths = self._select_paths_in_buildspace(
            directory, name, verb, count=1
        )
        if self.is_navigation(paths):
            return
        if not paths:
            return
        if 1 < len(paths):
            self.io.display("select just 1 layout.py to use as source ...")
            return
        assert len(paths) == 1
        source = paths[0]
        self.io.display(f"using {source.trim()} as source ...")
        self.io.display("")
        source_part_identifier = source._parse_part_identifier()
        if source_part_identifier is None:
            self.io.display(f"no part identifier found in {source.name} ...")
            return
        source_text = source.read_text()
        name, verb = "layout.py", "use as targets"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        if not paths:
            return
        for path in paths:
            part_identifier = path.get_part_identifier()
            target_text = source_text.replace(
                source_part_identifier, part_identifier
            )
            self.io.display(f"writing {path.trim()} ...")
            path.write_text(target_text)

    @Command(
        "++",
        description="all - pytest",
        external_directories=True,
        menu_section="all",
        score_package_paths=True,
        scores_directory=True,
    )
    def pytest_all(self, directory: Path, pattern: str = None) -> None:
        """
        Pytests all.
        """
        files, strings = directory._find_pytest_files(force=True)
        files = self._match_files(files, strings, pattern, "++")
        self._run_pytest(files)

    @Command(
        "q",
        description="go - quit",
        external_directories=True,
        menu_section="go",
        score_package_paths=True,
        scores_directory=True,
    )
    def quit(self) -> None:
        """
        Quits Abjad IDE.
        """
        self._navigation = "q"

    @Command(
        "rm",
        description="path - remove",
        external_directories=True,
        menu_section="path",
        score_package_path_blacklist=("contents",),
        score_package_paths=True,
        scores_directory=True,
    )
    def remove(self, directory: Path) -> None:
        """
        Removes assets.
        """
        paths = self._select_paths(directory, infinitive="to remove")
        if self.is_navigation(paths):
            return
        assert isinstance(paths, list)
        count = len(paths)
        if count == 1:
            self.io.display(f"will remove {paths[0].trim()} ...")
        else:
            self.io.display("will remove ...")
            for path in paths:
                self.io.display(f"    {path.trim()}")
        if count == 1:
            string = "remove"
        else:
            string = f"remove {count}"
        result = self.io.get(f"type {string!r} to proceed")
        if self.is_navigation(result):
            return
        if result != string:
            return
        for path in paths:
            self.io.display(f"removing {path.trim()} ...")
            path.remove()

    @Command(
        "ren",
        description="path - rename",
        external_directories=True,
        menu_section="path",
        score_package_path_blacklist=("contents",),
        score_package_paths=True,
        scores_directory=True,
    )
    def rename(self, directory: Path) -> None:
        """
        Renames file or directory.
        """
        paths = self._select_paths(directory, infinitive="to rename")
        if self.is_navigation(paths):
            return
        assert isinstance(paths, list), repr(paths)
        for source in paths:
            self.io.display(f"renaming {source.trim()} ...")
            name = self.io.get("new name")
            if self.is_navigation(name):
                return
            name_ = directory.coerce(name, suffix=source.suffix)
            target = source.parent / name_
            if target.exists():
                self.io.display(f"existing {target.trim()!r} ...")
                return
            self.io.display("renaming ...")
            self.io.display(f" FROM: {source.trim()}")
            self.io.display(f"   TO: {target.trim()}")
            response = self.io.get("ok?")
            if self.is_navigation(response):
                return
            if response != "y":
                return
            shutil.move(str(source), str(target))
            if target.is_wrapper():
                assert (target / source.name).is_dir()
                shutil.move(str(target / source.name), str(target.contents))
                target.contents.add_metadatum("title", name)
            if not target.is_dir():
                return
            for path in sorted(target.glob("*.py")):
                self._replace_in_file(
                    path, source.name, target.name, whole_words=True
                )

    @Command(
        "rp",
        description="text - replace",
        external_directories=True,
        menu_section="text",
        score_package_paths=True,
        scores_directory=True,
    )
    def replace(self, directory: Path) -> None:
        """
        Replaces search string with replace string.
        """
        search_string = self.io.get("enter search string")
        if self.is_navigation(search_string):
            return
        replace_string = self.io.get("enter replace string")
        if self.is_navigation(replace_string):
            return
        complete_words = False
        response = self.io.get("complete words only?")
        if self.is_navigation(response):
            return
        if response != "y":
            complete_words = True
        if directory.is_score_package_path():
            target = Path(directory.wrapper)
        else:
            target = directory
        lines = self._replace_in_tree(
            target, search_string, replace_string, complete_words
        )
        self.io.display(lines, raw=True)

    @Command(
        "sr",
        description="text - search",
        external_directories=True,
        menu_section="text",
        score_package_paths=True,
        scores_directory=True,
    )
    def search(self, directory: Path) -> None:
        """
        Searches for expression

        Delegates to ack if ack is found.

        Delegates to grep is ack is not found.
        """
        strings = abjad.IOManager.find_executable("ack")
        if not strings:
            strings = abjad.IOManager.find_executable("grep")
        executables = [Path(_) for _ in strings]
        if not executables:
            self.io.display("can not find ack.")
            self.io.display("can not find grep.")
            return
        assert 1 <= len(executables)
        executable = None
        for path in executables:
            if path.is_file():
                executable = path
        if executable is None:
            self.io.display("can not find ack.")
            self.io.display("can not find grep.")
            return
        search_string = self.io.get("enter search string")
        if self.is_navigation(search_string):
            return
        if executable.name == "ack":
            options = "--ignore-dir=_docs --sort-files --type=python"
            command = rf"{executable!s} {options} {search_string}"
            command = command.format(executable, search_string)
        elif executable.name == "grep":
            command = rf"{executable!s} -r {search_string!r} *"
        if directory.wrapper is not None:
            target = directory.wrapper
        else:
            target = directory
        with self.change(target):
            lines = abjad.IOManager.run_command(command)
            self.io.display(lines, raw=True)

    @Command(
        "aims",
        description=f"all invisible music - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_all_invisible_music(self, directory: Path) -> None:
        """
        Shows all invisible music.
        """
        assert directory.is_buildspace()
        tag = abjad.tags.INVISIBLE_MUSIC_COMMAND
        self.run(abjad.Job.show_tag(directory, tag, undo=True))
        tag = abjad.tags.INVISIBLE_MUSIC_COLORING
        self.run(abjad.Job.show_tag(directory, tag))

    @Command(
        "ass",
        description=f"annotation spanners - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_annotation_spanners(self, directory: Path) -> None:
        """
        Shows annotation spanners.
        """
        assert directory.is_buildspace()
        tags_ = abjad.tags.annotation_spanner_tags()

        def match(tags):
            return bool(set(tags) & set(tags_))

        name = "annotation spanners"
        self.run(abjad.Job.show_tag(directory, name, match=match))

    @Command(
        "cbs",
        description="clipboard - show",
        external_directories=True,
        menu_section="clipboard",
        score_package_paths=True,
        scores_directory=True,
    )
    def show_clipboard(self, directory: Path) -> None:
        """
        Shows clipboard.
        """
        if not bool(self.clipboard):
            self.io.display("showing empty clipboard ...")
            return
        self.io.display("showing clipboard ...")
        for path in self.clipboard:
            self.io.display(path.trim(), raw=True)

    @Command(
        "cts",
        description=f"clock time - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_clock_time(self, directory: Path) -> None:
        """
        Shows clock time.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.show_clock_time_markup(directory))

    @Command(
        "fns",
        description=f"figure names - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_figure_names(self, directory: Path) -> None:
        """
        Shows figure names.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.show_figure_name_markup(directory))

    @Command(
        "?",
        description="show - help",
        external_directories=True,
        menu_section="show",
        score_package_paths=True,
        scores_directory=True,
    )
    def show_help(self) -> None:
        """
        Shows help.
        """
        pass

    @Command(
        "lmns",
        description=f"local measure numbers - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_local_measure_numbers(self, directory: Path) -> None:
        """
        Shows local measure numbers.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.show_local_measure_number_markup(directory))

    @Command(
        "mns",
        description=f"measure numbers - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_measure_numbers(self, directory: Path) -> None:
        """
        Shows measure numbers.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.show_measure_number_markup(directory))

    @Command(
        "mms",
        description=f"mock music - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_mock_music(self, directory: Path) -> None:
        """
        Shows mock music.
        """
        assert directory.is_buildspace()
        tag = abjad.tags.MOCK_COLORING
        self.run(abjad.Job.show_tag(directory, tag))

    @Command(
        "mas",
        description=f"music annotations - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_music_annotations(self, directory: Path) -> None:
        """
        Shows music annotations.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.show_music_annotations(directory))

    @Command(
        "nyps",
        description=f"not yet pitched - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_not_yet_pitched(self, directory: Path) -> None:
        """
        Shows not yet pitched.
        """
        assert directory.is_buildspace()
        tag = abjad.tags.NOT_YET_PITCHED_COLORING
        self.run(abjad.Job.show_tag(directory, tag))

    @Command(
        "rass",
        description=f"rhythm annotation spanners - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_rhythm_annotation_spanners(self, directory: Path) -> None:
        """
        Shows rhythm annotation spanners.
        """
        assert directory.is_buildspace()
        name = "rhythm annotation spanners"
        self.run(
            abjad.Job.show_tag(directory, abjad.tags.RHYTHM_ANNOTATION_SPANNER)
        )

    @Command(
        "sps",
        description=f"spacing - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_spacing(self, directory: Path) -> None:
        """
        Shows spacing.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.show_spacing_markup(directory))

    @Command(
        "sns",
        description=f"stage numbers - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_stage_numbers(self, directory: Path) -> None:
        """
        Shows stage numbers.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_stage_number_markup(directory))

    @Command(
        "ts",
        description=f"tag - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_tag(self, directory: Path) -> None:
        """
        Shows arbitrary (user-specified) tag.
        """
        assert directory.is_buildspace()
        tag_ = self.io.get("tag")
        if self.is_navigation(tag_):
            return
        tag = abjad.Tag(tag_)
        self.run(abjad.Job.show_tag(directory, tag))

    @Command(
        "^",
        description="smart - doctest",
        external_directories=True,
        menu_section="smart",
        score_package_paths=True,
        scores_directory=True,
    )
    def smart_doctest(
        self, directory: Path, pattern: str, menu_paths: typing.List
    ) -> None:
        """
        Smart doctest.
        """
        address, file_ = self._match_smart_file(
            directory,
            pattern,
            menu_paths,
            "^",
            Path._find_doctest_files,
            "definition.py",
        )
        if file_:
            self.io.display(f"matching {address!r} to {file_.trim()} ...")
            self._run_doctest([file_])

    @Command(
        "@",
        description="smart - edit",
        external_directories=True,
        menu_section="smart",
        score_package_paths=True,
        scores_directory=True,
    )
    def smart_edit(
        self, directory: Path, pattern: str, menu_paths: typing.List
    ) -> None:
        """
        Smart edit.
        """
        address, file_ = self._match_smart_file(
            directory,
            pattern,
            menu_paths,
            "@",
            Path._find_editable_files,
            "definition.py",
        )
        if file_:
            self._open_files([file_])

    @Command(
        "*",
        description="smart - pdf",
        external_directories=True,
        menu_section="smart",
        score_package_paths=True,
        scores_directory=True,
    )
    def smart_pdf(
        self, directory: Path, pattern: str, menu_paths: typing.List
    ) -> None:
        """
        Smart PDF.
        """
        address, file_ = self._match_smart_file(
            directory,
            pattern,
            menu_paths,
            "*",
            Path._find_pdfs,
            "illustration.pdf",
        )
        if file_:
            self._open_files([file_])

    @Command(
        "+",
        description="smart - pytest",
        external_directories=True,
        menu_section="smart",
        score_package_paths=True,
        scores_directory=True,
    )
    def smart_pytest(
        self, directory: Path, pattern: str, menu_paths: typing.List
    ) -> None:
        """
        Smart pytest.
        """
        address, file_ = self._match_smart_file(
            directory, pattern, menu_paths, "+", Path._find_pytest_files, None
        )
        if file_:
            self.io.display(f"matching {address!r} to {file_.trim()} ...")
            self._run_pytest([file_])

    @Command(
        "bcpt",
        description="back-cover.pdf - trash",
        menu_section="back cover",
        score_package_paths=("_segments", "build"),
    )
    def trash_back_cover_pdf(self, directory: Path) -> None:
        """
        Trashes ``back-cover.pdf``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "back-cover.pdf", "trash"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._trash_files(paths)

    @Command(
        "bctt",
        description="back-cover.tex - trash",
        menu_section="back cover",
        score_package_paths=("_segments", "build"),
    )
    def trash_back_cover_tex(self, directory: Path) -> None:
        """
        Trashes ``back-cover.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "back-cover.tex", "trash"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._trash_files(paths)

    @Command(
        "dpt",
        description="definition.py - trash",
        menu_section="definition",
        score_package_paths=("illustrationspace",),
    )
    def trash_definition_py(self, directory: Path) -> None:
        """
        Trashes ``definition.py``.
        """
        assert directory.is_illustrationspace()
        if directory.is_material() or directory.is_segment():
            path = directory / "definition.py"
            self._trash_files(path)
        else:
            for path in directory.list_paths():
                self.trash_definition_py(path)

    @Command(
        "fcpt",
        description="front-cover.pdf - trash",
        menu_section="front cover",
        score_package_paths=("_segments", "build"),
    )
    def trash_front_cover_pdf(self, directory: Path) -> None:
        """
        Trashes ``front-cover.pdf``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "front-cover.pdf", "trash"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._trash_files(paths)

    @Command(
        "fctt",
        description="front-cover.tex - trash",
        menu_section="front cover",
        score_package_paths=("_segments", "build"),
    )
    def trash_front_cover_tex(self, directory: Path) -> None:
        """
        Trashes ``front-cover.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "front-cover.tex", "trash"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._trash_files(paths)

    @Command(
        "iit",
        description="illustration.ily - trash",
        menu_section="illustration",
        score_package_paths=("illustrationspace",),
    )
    def trash_illustration_ily(self, directory: Path) -> None:
        """
        Trashes ``illustration.ily``.
        """
        assert directory.is_illustrationspace()
        if directory.is_material() or directory.is_segment():
            path = directory / "illustration.ily"
            self._trash_files(path)
        else:
            for path in directory.list_paths():
                self.trash_illustration_ily(path)

    @Command(
        "ilt",
        description="illustration.ly - trash",
        menu_section="illustration",
        score_package_paths=("illustrationspace",),
    )
    def trash_illustration_ly(self, directory: Path) -> None:
        """
        Trashes ``illustration.ly``.
        """
        assert directory.is_illustrationspace()
        if directory.is_material() or directory.is_segment():
            path = directory / "illustration.ly"
            self._trash_files(path)
        else:
            for path in directory.list_paths():
                self.trash_illustration_ly(path)

    @Command(
        "ipt",
        description="illustration.pdf - trash",
        menu_section="illustration",
        score_package_paths=("illustrationspace",),
    )
    def trash_illustration_pdf(self, directory: Path) -> None:
        """
        Trashes ``illustration.pdf``.
        """
        assert directory.is_illustrationspace()
        if directory.is_material() or directory.is_segment():
            path = directory / "illustration.pdf"
            self._trash_files(path)
        else:
            for path in directory.list_paths():
                self.trash_illustration_pdf(path)

    @Command(
        "llt",
        description="layout.ly - trash",
        menu_section="layout",
        score_package_paths=("buildspace",),
    )
    def trash_layout_ly(self, directory: Path) -> None:
        """
        Trashes ``layout.ly``.
        """
        assert directory.is_buildspace()
        name, verb = "layout.ly", "trash"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._trash_files(paths)

    @Command(
        "lpt",
        description="layout.py - trash",
        menu_section="layout",
        score_package_paths=("buildspace",),
    )
    def trash_layout_py(self, directory: Path) -> None:
        """
        Trashes ``layout.py``.
        """
        assert directory.is_buildspace()
        name, verb = "layout.py", "trash"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._trash_files(paths)

    @Command(
        "mlt",
        description="music.ly - trash",
        menu_section="music",
        score_package_paths=("_segments", "build"),
    )
    def trash_music_ly(self, directory: Path) -> None:
        """
        Trashes ``music.ly``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "music.ly", "trash"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._trash_files(paths)

    @Command(
        "mpt",
        description="music.pdf - trash",
        menu_section="music",
        score_package_paths=("_segments", "build"),
    )
    def trash_music_pdf(self, directory: Path) -> None:
        """
        Trashes ``music.pdf``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "music.pdf", "trash"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._trash_files(paths)

    @Command(
        "ppt",
        description="part.pdf - trash",
        menu_section="parts",
        score_package_paths=("part", "parts"),
    )
    def trash_part_pdf(self, directory: Path) -> None:
        """
        Trashes ``part.pdf``.
        """
        assert directory.is_parts() or directory.is_part()
        name, verb = "part.pdf", "trash"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._trash_files(paths)

    @Command(
        "ptt",
        description="part.tex - trash",
        menu_section="parts",
        score_package_paths=("part", "parts"),
    )
    def trash_part_tex(self, directory: Path) -> None:
        """
        Trashes ``part.tex``.
        """
        assert directory.is_parts() or directory.is_part()
        name, verb = "part.tex", "trash"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._trash_files(paths)

    @Command(
        "pfpt",
        description="preface.pdf - trash",
        menu_section="preface",
        score_package_paths=("_segments", "build"),
    )
    def trash_preface_pdf(self, directory: Path) -> None:
        """
        Trashes ``preface.pdf``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "preface.pdf", "trash"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._trash_files(paths)

    @Command(
        "pftt",
        description="preface.tex - trash",
        menu_section="preface",
        score_package_paths=("_segments", "build"),
    )
    def trash_preface_tex(self, directory: Path) -> None:
        """
        Trashes ``preface.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        name, verb = "preface.tex", "trash"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        self._trash_files(paths)

    @Command(
        "spt",
        description="score.pdf - trash",
        menu_section="score",
        score_package_path_blacklist=("parts",),
        score_package_paths=("_segments", "build"),
    )
    def trash_score_pdf(self, directory: Path) -> None:
        """
        Trashes ``score.pdf``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        path = directory.build / "score.pdf"
        self._trash_files(path)

    @Command(
        "stt",
        description="score.tex - trash",
        menu_section="score",
        score_package_path_blacklist=("parts",),
        score_package_paths=("_segments", "build"),
    )
    def trash_score_tex(self, directory: Path) -> None:
        """
        Trashes ``score.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        path = directory.build / "score.tex"
        self._trash_files(path)

    @Command(
        "ssit",
        description="stylesheet.ily - trash",
        menu_section="stylesheet",
        score_package_paths=("_segments", "build"),
    )
    def trash_stylesheet_ily(self, directory: Path) -> None:
        """
        Trashes ``stylesheet.ily``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        path = directory.build / "stylesheet.ily"
        self._trash_files(path)

    @Command(
        "cuc",
        description="clefs - uncolor",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def uncolor_clefs(self, directory: Path) -> None:
        """
        Uncolors clefs.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_clefs(directory, undo=True))

    @Command(
        "duc",
        description="dynamics - uncolor",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def uncolor_dynamics(self, directory: Path) -> None:
        """
        Uncolors dynamics.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_dynamics(directory, undo=True))

    @Command(
        "iuc",
        description="instruments - uncolor",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def uncolor_instruments(self, directory: Path) -> None:
        """
        Uncolors instruments.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_instruments(directory, undo=True))

    @Command(
        "mmuc",
        description="margin markup - uncolor",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def uncolor_margin_markup(self, directory: Path) -> None:
        """
        Uncolors margin markup.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_margin_markup(directory, undo=True))

    @Command(
        "tmuc",
        description="metronome marks - uncolor",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def uncolor_metronome_marks(self, directory: Path) -> None:
        """
        Uncolors metornome marks.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_metronome_marks(directory, undo=True))

    @Command(
        "piuc",
        description="persistent indicators - uncolor",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def uncolor_persistent_indicators(self, directory: Path) -> None:
        """
        Uncolors persistent indicators.
        """
        assert directory.is_buildspace()
        job = abjad.Job.color_persistent_indicators(directory, undo=True)
        self.run(job)

    @Command(
        "sluc",
        description="staff lines - uncolor",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def uncolor_staff_lines(self, directory: Path) -> None:
        """
        Uncolors staff lines.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_staff_lines(directory, undo=True))

    @Command(
        "tsuc",
        description="time signatures - uncolor",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def uncolor_time_signatures(self, directory: Path) -> None:
        """
        Uncolors time signatures.
        """
        assert directory.is_buildspace()
        self.run(abjad.Job.color_time_signatures(directory, undo=True))

    @Command(
        "mlx",
        description="music.ly - xinterpret",
        menu_section="music",
        score_package_paths=("_segments", "build"),
    )
    def xinterpret_music_ly(
        self, directory: Path, open_after: bool = True
    ) -> None:
        """
        Interprets ``music.ly`` without collecting segments, handling
        tags or generating music.
        """
        assert directory.is__segments() or directory.is_build()
        self.interpret_music_ly(
            directory,
            do_not_collect_segments=True,
            do_not_generate_music=True,
            open_after=open_after,
        )
