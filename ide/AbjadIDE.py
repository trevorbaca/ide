import collections
import difflib
import inspect
import io
import os
import platform
import re
import shutil
import subprocess
import sys
import typing

import abjad

from . import jobs as _jobs
from . import pathx
from . import segments as _segments
from . import tags as _tags
from .Command import Command
from .Configuration import Configuration
from .IO import IO
from .Menu import Menu
from .MenuSection import MenuSection
from .Response import Response
from .segments import Job, Part


def _directory_to_header(directory):
    if directory.is_scores():
        return "Abjad IDE : scores"
    if directory.is_external():
        header = f"Abjad IDE : {directory}"
        if not directory.list_paths():
            header += " (empty)"
        return header
    parts = [directory.contents.get_title()]
    if directory.is_wrapper():
        parts.append("wrapper")
    elif not directory.is_contents():
        parts.extend(directory.relative_to(directory.contents).parts[:-1])
        parts.append(directory.get_identifier())
    if parts and not directory.list_paths():
        parts[-1] += " (empty)"
    return " : ".join(parts)


def _filter_files(files, strings, pattern):
    if isinstance(pattern, str):
        indices = abjad.String.match_strings(strings, pattern)
        files = abjad.Sequence(files).retain(indices)
    return files


def _find_editable_files(path, force=False):
    files, strings = [], []
    if force or not path.is_score_package_path():
        for path_ in sorted(path.glob("**/*")):
            if not path_.is_file():
                continue
            files.append(path_)
            strings.append(path_.name)
    else:
        for path_ in path.segments.list_paths():
            files.append(path_ / "definition.py")
            strings.append(path_.get_identifier())
        for path_ in path.stylesheets.list_paths():
            files.append(path_)
            strings.append(path_.name)
        for path_ in path.etc.list_paths():
            files.append(path_)
            strings.append(path_.name)
    return files, strings


def _get_added_asset_paths(directory):
    paths = []
    git_status_lines = _get_git_status_lines(directory)
    for line in git_status_lines:
        line = str(line)
        if line.startswith("A"):
            path = line.strip("A")
            path = path.strip()
            root = directory.wrapper
            path = root / path
            paths.append(path)
    return paths


def _get_git_status_lines(directory):
    with abjad.TemporaryDirectoryChange(directory=directory.wrapper):
        command = f"git status --porcelain {directory}"
        return abjad.iox.run_command(command)


def _get_repository_root(directory):
    if not directory.exists():
        return
    if directory.wrapper is None:
        path = directory
    else:
        path = directory.wrapper
    while str(path) != str(path.parts[0]):
        for path_ in path.iterdir():
            if path_.name == ".git":
                return type(directory)(path)
        path = path.parent


def _get_unadded_asset_paths(directory):
    assert directory.is_dir()
    paths = []
    root = directory.wrapper
    git_status_lines = _get_git_status_lines(directory)
    for line in git_status_lines:
        line = str(line)
        if line.startswith("?"):
            path = line.strip("?")
            path = path.strip()
            path = root / path
            paths.append(path)
        elif line.startswith("M"):
            path = line.strip("M")
            path = path.strip()
            path = root / path
            paths.append(path)
    paths = [_ for _ in paths]
    return paths


# def _has_pending_commit(directory):
#    assert directory.is_dir()
#    command = f"git status {directory}"
#    with abjad.TemporaryDirectoryChange(directory=directory):
#        lines = abjad.iox.run_command(command)
#    clean_lines = []
#    for line in lines:
#        line = str(line)
#        clean_line = line.strip()
#        clean_line = clean_line.replace(str(directory), "")
#        clean_lines.append(clean_line)
#    for line in clean_lines:
#        if "Changes not staged for commit:" in line:
#            return True
#        if "Changes to be committed:" in line:
#            return True
#        if "Untracked files:" in line:
#            return True


def _is_git_unknown(directory):
    if not directory.exists():
        return False
    git_status_lines = _get_git_status_lines(directory)
    git_status_lines = git_status_lines or [""]
    first_line = git_status_lines[0]
    if first_line.startswith("?"):
        return True
    return False


def _is_prototype(path, prototype):
    if prototype is True:
        return True
    if bool(prototype) is False:
        return False
    return path.is_score_package_path(prototype)


def _make__assets_directory(directory):
    if directory._assets.exists():
        return
    directory._assets.mkdir()
    gitignore = directory._assets / ".gitignore"
    gitignore.write_text("")


def _make__segments_directory(directory):
    if directory._segments.exists():
        return
    directory._segments.mkdir()
    gitignore = directory._segments / ".gitignore"
    gitignore.write_text("*.ily")
    gitignore.write_text("*.ly")


def _parse_part_identifier(path):
    if path.suffix == ".ly":
        part_identifier = None
        with path.open("r") as pointer:
            for line in pointer.readlines():
                if line.startswith("% part_identifier = "):
                    line = line.strip("% part_identifier = ")
                    part_identifier = eval(line)
                    return part_identifier
    elif path.name.endswith("layout.py"):
        part_identifier = None
        with path.open("r") as pointer:
            for line in pointer.readlines():
                if line.startswith("part_identifier = "):
                    line = line.strip("part_identifier = ")
                    part_identifier = eval(line)
                    return part_identifier
    else:
        raise TypeError(path)


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


class AbjadIDE:
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

    abjad_configuration = abjad.Configuration()
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

    known_tags = (
        _tags.CLOCK_TIME,
        _tags.FIGURE_NAME,
        _tags.INVISIBLE_MUSIC_COMMAND,
        _tags.INVISIBLE_MUSIC_COLORING,
        _tags.LOCAL_MEASURE_NUMBER,
        _tags.MATERIAL_ANNOTATION_SPANNER,
        _tags.MEASURE_NUMBER,
        _tags.MOCK_COLORING,
        _tags.NOT_YET_PITCHED_COLORING,
        _tags.PITCH_ANNOTATION_SPANNER,
        _tags.RHYTHM_ANNOTATION_SPANNER,
        _tags.SPACING,
        _tags.SPACING_OVERRIDE,
        _tags.STAGE_NUMBER,
    )

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
        abjad.iox.spawn_subprocess("clear")

    def __repr__(self) -> str:
        """
        Delegates to storage format manager.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

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

    def _check_layout_time_signatures(self, path, indent=0):
        message = "checking layout time signatures ..."
        self.io.display(message, indent=indent)
        layout_ly = path.name.replace("music.ly", "layout.ly")
        layout_ly = path.parent / layout_ly
        if not layout_ly.exists():
            message = f"no {layout_ly.trim()} found ..."
            self.io.display(message, indent=indent + 1)
            return
        self.io.display(f"found {layout_ly.trim()} ...", indent=indent + 1)
        metadata_time_signatures = path.parent.get_time_signature_metadata()
        metadata_time_signatures = [str(_) for _ in metadata_time_signatures]
        if metadata_time_signatures:
            message = "found time signature metadata ..."
            self.io.display(message, indent=indent + 1)
        layout_time_signatures = _segments.get_preamble_time_signatures(layout_ly)
        partial_score = _segments.get_preamble_partial_score(layout_ly)
        if partial_score:
            self.io.display("found partial score ...", indent=indent + 1)
            return
        if layout_time_signatures == metadata_time_signatures:
            message = "layout time signatures"
            message += f" ({len(layout_time_signatures)})"
            message += " match metadata time signatures"
            message += f" ({len(metadata_time_signatures)}) ..."
            self.io.display(message, indent=indent + 1)
            return
        message = "layout time signatures"
        message += f" ({len(layout_time_signatures)})"
        message += " do not match metadata time signatures"
        message += f" ({len(metadata_time_signatures)}) ..."
        self.io.display(message, indent=indent + 1)
        if self.test:
            return
        message = f"remaking {layout_ly.trim()} ..."
        self.io.display(message, indent=indent + 1)
        layout_py = layout_ly.with_suffix(".py")
        self._make_layout_ly(layout_py)
        layout_time_signatures = _segments.get_preamble_time_signatures(layout_ly)
        if layout_time_signatures == metadata_time_signatures:
            message = "layout time signatures"
            message += f" ({len(layout_time_signatures)})"
            message += " match metadata time signatures"
            message += f" ({len(metadata_time_signatures)}) ..."
        else:
            message = "layout time signatures"
            message += f" ({len(layout_time_signatures)})"
            message += " still do not match metadata time signatures"
            message += f" ({len(metadata_time_signatures)}) ..."
        self.io.display(message, indent=indent + 1)

    def _check_out_paths(self, paths):
        assert isinstance(paths, collections.abc.Iterable), repr(paths)
        for path in paths:
            root = _get_repository_root(path)
            if not root:
                self.io.display(f"missing {path.trim()} repository ...")
                return
            with self.change(root):
                command = f"git checkout {path}"
                self.io.display(f"Running {command} ...")
                lines = abjad.iox.run_command(command)
                self.io.display(lines, raw=True)

    def _check_test_scores_directory(self, check=False):
        if not check:
            return
        directory = self.configuration.test_scores_directory
        names = [_.name for _ in directory.iterdir()]
        if "red_score" not in names:
            message = f"Empty test scores directory {directory} ..."
            raise Exception(message)

    def _collect_segment_lys(self, directory):
        paths = directory.segments.list_paths()
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
        boilerplate = pathx.Path(self.configuration.boilerplate_directory)
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
            log = self.abjad_configuration.lilypond_log_file_path
        log = pathx.Path(log)
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
        composer_website = self.abjad_configuration.composer_website or ""
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
        dimensions = _to_paper_dimensions(paper_size, orientation)
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
        paper_size = _to_paper_dimensions(paper_size, orientation)
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
        self._copy_boilerplate(directory, name, target_name=path.name, values=values)

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
        composer = self.abjad_configuration.composer_uppercase_name
        if self.test or self.example:
            composer = "COMPOSER"
        values["composer"] = str(composer)
        paper_size = directory.get_metadatum("paper_size", "letter")
        orientation = directory.get_metadatum("orientation")
        paper_size = _to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f"{{{width}{unit}, {height}{unit}}}"
        values["paper_size"] = paper_size
        target_name = None
        target_name = path
        self._copy_boilerplate(directory, name, target_name=target_name, values=values)

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
        self.io.display(f"generating {path.trim()} ...")
        if path.exists():
            self.io.display(f"removing {path.trim()} ...", indent=indent + 1)
            path.remove()
        segments = path.segments.list_paths()
        if not silent:
            if not segments:
                self.io.display("no segments found ...", indent=indent + 1)
            for segment in segments:
                if not segment.is_segment():
                    continue
                message = f"examining {segment.trim()} ..."
                self.io.display(message, indent=indent + 1)
        names = [_.stem.replace("_", "-") for _ in segments]
        boilerplate = "part-music.ly"
        self._copy_boilerplate(
            path.build, boilerplate, indent=indent + 1, target_name=path.name
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
        lilypond_language_directive = abjad.lilypond(language_token)
        version_token = abjad.LilyPondVersionToken()
        lilypond_version_directive = abjad.lilypond(version_token)
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
            identifiers = _segments.global_skip_identifiers(path)
            identifiers = ["\\" + _ for _ in identifiers]
            newline = "\n" + 24 * " "
            global_skip_identifiers = newline.join(identifiers)
            if self.test:
                segment_ly_include_statements = r"\FOO"
            else:
                dictionary = self._make_container_to_part_assignment(path)
                identifiers = _segments.part_to_identifiers(path, part, dictionary)
                if isinstance(identifiers, str):
                    self.io.display(identifiers + " ...", indent=indent + 1)
                    message = f"removing {path.trim()} ..."
                    self.io.display(message, indent=indent + 1)
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
        paper_size = _to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f"{{{width}{unit}, {height}{unit}}}"
        values["paper_size"] = paper_size
        target_name = path.name
        self._copy_boilerplate(directory, name, target_name=target_name, values=values)

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
        paper_size = _to_paper_dimensions(paper_size, orientation)
        width, height, unit = paper_size
        paper_size = f"{{{width}{unit}, {height}{unit}}}"
        values["paper_size"] = paper_size
        if path.build.is_part():
            name = "part-preface.tex"
            target_name = f"{path.build.name}-preface.tex"
        else:
            name = "score-preface.tex"
            target_name = path.name
        self._copy_boilerplate(directory, name, target_name=target_name, values=values)

    def _generate_score_music_ly(
        self, path, forces_tagline=None, indent=0, silent=None
    ):
        assert path.build.exists(), repr(path)
        self.io.display(f"generating {path.trim()} ...", indent=indent)
        if path.exists():
            self.io.display(f"removing {path.trim()} ...", indent=indent + 1)
            path.remove()
        segments = path.segments.list_paths()
        if not silent:
            if not segments:
                self.io.display("no segments found ...", indent=indent + 1)
            for segment in segments:
                if not segment.is_segment():
                    continue
                message = f"examining {segment.trim()} ..."
                self.io.display(message, indent=indent + 1)
        names = [_.stem.replace("_", "-") for _ in segments]
        score_skeleton = _segments.score_skeleton(path)
        if score_skeleton is None:
            boilerplate = "score-music.ly"
        else:
            boilerplate = "full-score-music.ly"
            text = abjad.lilypond(score_skeleton)
            lines = text.split("\n")
            lines = [lines[0]] + [8 * " " + _ for _ in lines[1:]]
            score_skeleton = "\n".join(lines)
        self._copy_boilerplate(
            path.build, boilerplate, indent=indent + 1, target_name=path.name
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
        lilypond_language_directive = abjad.lilypond(language_token)
        version_token = abjad.LilyPondVersionToken()
        lilypond_version_directive = abjad.lilypond(version_token)
        annotated_title = path.contents.get_title(year=True)
        if annotated_title:
            score_title = annotated_title
        else:
            score_title = path.contents.get_title(year=False)
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

    def _get_score_names(self):
        scores = self._get_scores_directory()
        names = [_.name for _ in scores.list_paths()]
        return names

    def _get_scores_directory(self):
        if self.test or self.example:
            return self.configuration.test_scores_directory
        return pathx.Path(self.configuration.composer_scores_directory)

    def _go_to_directory(
        self,
        directory: pathx.Path,
        pattern: str = None,
        payload: typing.List = None,
    ) -> None:
        assert directory.is_dir()
        # TODO: remove following line?
        address = "%" + (pattern or "")
        if self.aliases and pattern in self.aliases:
            path = pathx.Path(self.aliases[pattern])
            self.io.display(f"matching {address!r} to {path.trim()} ...")
            self._manage_directory(path)
            return
        if isinstance(payload, pathx.Path):
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
            assert all(isinstance(_, pathx.Path) for _ in payload), repr(payload)
            paths = payload
            counter = abjad.String("directory").pluralize(len(paths))
            message = f"matching {address!r} to {len(paths)} {counter} ..."
            self.io.display(message)
            for path in paths:
                self.io.display(path.trim(), raw=True)
            if paths:
                path_ = paths[0]
                if path_.is_dir():
                    self._manage_directory(path_)
                else:
                    self._open_files([path_])
            return
        assert payload is None, repr(payload)
        paths, strings = [], []
        if directory.is_score_package_path():
            root = directory.contents
        else:
            root = directory
        for path in sorted(root.glob("**/*")):
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

    def _handle_part_identifier_tags(self, path, indent=0):
        assert path.parent.is_part()
        parts_directory = path.parent.parent
        part_identifier = _parse_part_identifier(path)
        if part_identifier is None:
            self.io.display(
                f"no part identifier found in {path.name} ...",
                indent=indent,
            )
            return
        self.io.display("handling part identifier tags ...", indent=indent)
        parts_directory_name = abjad.String(
            parts_directory.name,
        )
        parts_directory_name = parts_directory_name.to_shout_case()
        tag = f"+{parts_directory_name}_{part_identifier}"
        self.activate(
            parts_directory,
            tag,
            indent=indent + 1,
            message_zero=True,
        )

    def _interpret_file(self, path):
        path = pathx.Path(path)
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
            stderr_lines = abjad.iox._read_from_pipe(process.stderr)
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
        executables = abjad.iox.find_executable("xelatex")
        executables = [pathx.Path(_) for _ in executables]
        if not executables:
            executable_name = "pdflatex"
        else:
            executable_name = "xelatex"
        log = self.configuration.latex_log_file_path
        command = f"date > {log};"
        command += f" {executable_name} -halt-on-error"
        command += " -interaction=nonstopmode"
        command += f" --jobname={tex.stem}"
        command += f" -output-directory={tex.parent} {tex}"
        command += f" >> {log} 2>&1"
        command_called_twice = f"{command}; {command}"
        with self.change(tex.parent):
            abjad.iox.spawn_subprocess(command_called_twice)
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
            self._interpret_tex_file(source)

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
                and _is_prototype(directory, command.score_package_paths)
                and not _is_prototype(directory, blacklist)
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
        pairs = self._collect_segment_lys(directory.build)
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

    def _make_layout_ly(self, path):
        assert path.suffix == ".py"
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

    def _make_parts_directory(self, directory):
        assert directory.is_builds()
        self.io.display("getting part names from score template ...")
        part_manifest = _segments.get_part_manifest(directory)
        part_names = [_.name for _ in part_manifest]
        for part_name in part_names:
            self.io.display(f"found {part_name} ...")
        self.io.display("")
        name = self.io.get("directory name")
        if self.is_navigation(name):
            return
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
            self.io.display("choose from ...")
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
        self.collect_segment_lys(parts_directory)
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
            part_subtitle = _part_subtitle(part.name, parentheses=True)
            forces_tagline = _part_subtitle(part.name) + " part"
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
        self._copy_boilerplate(build, "score_layout.py", target_name="layout.py")
        self.io.display("")
        self.collect_segment_lys(build)
        self.io.display("")
        self.generate_music_ly(build)
        self.io.display("")
        self.generate_preface_tex(build)
        self.io.display("")
        self.generate_score_tex(build)
        self.io.display("")
        self.generate_stylesheet_ily(build)

    def _make_segment_clicktrack(self, directory, open_after=True):
        assert directory.is_segment(), repr(directory)
        definition = directory / "definition.py"
        if not definition.is_file():
            self.io.display(f"can not find {definition.trim()} ...")
            return -1
        self.io.display("making clicktrack ...")
        score_name = directory.contents.name
        segment_name = directory.name
        ly = directory / f"{score_name}-{segment_name}-clicktrack.ly"
        if ly.exists():
            self.io.display(f"removing {ly.trim()} ...")
            ly.remove()
        midi = directory / f"{score_name}-{segment_name}-clicktrack.midi"
        if midi.exists():
            self.io.display(f"removing {midi.trim()} ...")
            midi.remove()
        maker = directory / "__make_segment_clicktrack__.py"
        maker.remove()
        with self.cleanup([maker]):
            self.io.display(f"writing {maker.trim()} ...")
            self._copy_boilerplate(directory, maker.name)
            previous_segment = directory.get_previous_package()
            if previous_segment is None:
                statement = "previous_metadata = None"
                persist_statement = "previous_persist = None"
            else:
                #                statement = "from {}.segments.{}.__metadata__"
                #                statement += " import metadata as previous_metadata"
                #                statement = statement.format(
                #                    directory.contents.name, previous_segment.name
                #                )
                metadata = previous_segment / "__metadata__.py"
                statement = f'file = ide.Path("{metadata}")'
                statement += "\n        lines = file.read_text()"
                statement += "\n        exec(lines)"
                statement += "\n        previous_metadata = metadata"
                #                persist_statement = "from {}.segments.{}.__persist__"
                #                persist_statement += " import persist as previous_persist"
                #                persist_statement = persist_statement.format(
                #                    directory.contents.name, previous_segment.name
                #                )
                persist = previous_segment / "__persist__.py"
                persist_statement = f'file = ide.Path("{persist}")'
                persist_statement += "\n        lines = file.read_text()"
                persist_statement += "\n        exec(lines)"
                persist_statement += "\n        previous_persist = persist"
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
                #                statement = "from {}.segments.{}.__metadata__"
                #                statement += " import metadata as previous_metadata"
                #                statement = statement.format(
                #                    directory.contents.name, previous_segment.name
                #                )
                metadata = previous_segment / "__metadata__.py"
                statement = f'file = ide.Path("{metadata}")'
                statement += "\n        lines = file.read_text()"
                statement += "\n        exec(lines)"
                statement += "\n        previous_metadata = metadata"
                #                persist_statement = "from {}.segments.{}._persist__"
                #                persist_statement += " import persist as previous_persist"
                #                persist_statement = persist_statement.format(
                #                    directory.contents.name, previous_segment.name
                #                )
                persist = previous_segment / "__persist__.py"
                persist_statement = f'file = ide.Path("{persist}")'
                persist_statement += "\n        lines = file.read_text()"
                persist_statement += "\n        exec(lines)"
                persist_statement += "\n        previous_persist = persist"
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
            self._copy_boilerplate(directory, maker.name)
            previous_segment = directory.get_previous_package()
            if previous_segment is None:
                statement = "previous_metadata = None"
                persist_statement = "previous_persist = None"
            else:
                #                statement = "from {}.segments.{}.__metadata__"
                #                statement += " import metadata as previous_metadata"
                #                statement = statement.format(
                #                    directory.contents.name, previous_segment.name
                #                )
                metadata = previous_segment / "__metadata__.py"
                statement = f'file = ide.Path("{metadata}")'
                statement += "\n        lines = file.read_text()"
                statement += "\n        exec(lines)"
                statement += "\n        previous_metadata = metadata"
                #                persist_statement = "from {}.segments.{}.__persist__"
                #                persist_statement += " import persist as previous_persist"
                #                persist_statement = persist_statement.format(
                #                    directory.contents.name, previous_segment.name
                #                )
                persist = previous_segment / "__persist__.py"
                persist_statement = f'file = ide.Path("{persist}")'
                persist_statement += "\n        lines = file.read_text()"
                persist_statement += "\n        exec(lines)"
                persist_statement += "\n        previous_persist = persist"
            template = maker.read_text()
            template = template.format(
                previous_segment_metadata_import_statement=statement,
                previous_segment_persist_import_statement=persist_statement,
            )
            maker.write_text(template)
            self.io.display(f"interpreting {maker.trim()} ...")
            result = self._interpret_file(maker)
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
                #                statement = "from {}.segments.{}.__metadata__"
                #                statement += " import metadata as previous_metadata"
                #                statement = statement.format(
                #                    directory.contents.name, previous_segment.name
                #                )
                metadata = previous_segment / "__metadata__.py"
                statement = f'file = ide.Path("{metadata}")'
                statement += "\n        lines = file.read_text()"
                statement += "\n        exec(lines)"
                statement += "\n        previous_metadata = metadata"
                #                persist_statement = "from {}.segments.{}.__persist__"
                #                persist_statement += " import persist as previous_persist"
                #                persist_statement = persist_statement.format(
                #                    directory.contents.name, previous_segment.name
                #                )
                persist = previous_segment / "__persist__.py"
                persist_statement = f'file = ide.Path("{persist}")'
                persist_statement += "\n        lines = file.read_text()"
                persist_statement += "\n        exec(lines)"
                persist_statement += "\n        previous_persist = persist"
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
        assert isinstance(directory, pathx.Path), repr(directory)
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
        header = _directory_to_header(directory)
        menu = Menu.from_directory(
            directory,
            header,
            aliases=self.aliases,
            io=self.io,
            navigations=self.navigations,
            sections=sections,
        )
        dimensions = self._get_dimensions()
        response = menu(dimensions=dimensions, redraw=redraw)
        if self.is_navigation(response.string):
            pass
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
                return path, True
            else:
                self.io.display(f"missing {path.trim()} ...")
        else:
            assert response.payload is None, repr(response)
            with self.change(directory):
                abjad.iox.spawn_subprocess(response.string)
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
            return self.current_directory, redraw

    def _match_alias(self, directory, string):
        if not self.aliases:
            return
        if not self.aliases.get(string):
            return
        value = self.aliases.get(string)
        path = pathx.Path(value)
        if path.exists():
            return path
        if directory.is_score_package_path() and not directory.is_scores():
            return directory.contents(value)

    def _match_files(self, files, strings, pattern):
        if pattern:
            files = _filter_files(files, strings, pattern)
        else:
            files = [_ for _ in files if _.name[0].isalpha()]
        address = pattern or ""
        count = len(files)
        counter = abjad.String("file").pluralize(count)
        message = f"matching {address!r} to {count} {counter} ..."
        self.io.display(message)
        return files

    def _open_files(self, paths, force_vim=False, silent=False, warn=100):
        assert isinstance(paths, collections.abc.Iterable), repr(paths)
        for path in paths:
            if not path.exists():
                self.io.display(f"missing {path.trim()} ...")
                return
            if not path.is_file():
                self.io.display(f"not a file {path.trim()} ...")
                return
        string = " ".join([str(_) for _ in paths])
        mode = "e"
        if all(_.suffix in (".mid", ".midi", ".pdf") for _ in paths):
            mode = "o"
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
        if warn <= len(paths):
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
                    abjad.iox.spawn_subprocess(permissions)
                    abjad.iox.spawn_subprocess(str(target))
        abjad.iox.spawn_subprocess(command)

    def _purge_clipboard(self):
        clipboard = []
        for source in self.clipboard:
            if source.exists():
                clipboard.append(source)
        self.clipboard[:] = clipboard

    def _replace_in_tree(
        self, directory, search_string, replace_string, complete_words=False
    ):
        command = f"ajv replace {search_string!r} {replace_string!r} -Y"
        if complete_words:
            command += " -W"
        with self.change(directory):
            lines = abjad.iox.run_command(command)
            lines = [_.strip() for _ in lines if not _ == ""]
            return lines

    def _run_lilypond(self, ly, indent=0):
        assert ly.exists()
        if not abjad.iox.find_executable("lilypond"):
            raise ValueError("cannot find LilyPond executable.")
        self.io.display(f"running LilyPond on {ly.trim()} ...", indent=indent)
        directory = ly.parent
        pdf = ly.with_suffix(".pdf")
        backup_pdf = ly.with_suffix("._backup.pdf")
        log = directory / ".log"
        if backup_pdf.exists():
            backup_pdf.remove()
        if pdf.exists():
            self.io.display(f"removing {pdf.trim()} ...", indent=indent + 1)
            pdf.remove()
        assert not pdf.exists()
        with self.change(directory):
            self.io.display(f"interpreting {ly.trim()} ...", indent=indent + 1)
            abjad.iox.run_lilypond(str(ly), lilypond_log_file_path=str(log))
            _segments.remove_lilypond_warnings(
                log,
                crescendo_too_small=True,
                decrescendo_too_small=True,
                overwriting_glissando=True,
            )
            self._display_lilypond_log_errors(log=log)
            if pdf.is_file():
                self.io.display(f"found {pdf.trim()} ...", indent=indent + 1)
            else:
                self.io.display(f"can not produce {pdf.trim()} ...", indent=indent + 1)

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
            abjad.iox.spawn_subprocess(command)

    def _select_annotation_jobs(self, directory, undo=False):
        def _annotation_spanners(tags):
            tags_ = (
                _tags.MATERIAL_ANNOTATION_SPANNER,
                _tags.PITCH_ANNOTATION_SPANNER,
                _tags.RHYTHM_ANNOTATION_SPANNER,
            )
            return bool(set(tags) & set(tags_))

        annotation_spanners = _jobs.show_tag(
            directory,
            "annotation spanners",
            match=_annotation_spanners,
            undo=undo,
        )

        def _spacing(tags):
            tags_ = (
                _tags.SPACING,
                _tags.SPACING_OVERRIDE,
            )
            return bool(set(tags) & set(tags_))

        spacing = _jobs.show_tag(directory, "spacing", match=_spacing, undo=undo)

        items = [
            ("annotation spanners", annotation_spanners),
            ("clock time", _jobs.show_tag(directory, _tags.CLOCK_TIME, undo=undo)),
            ("figure name", _jobs.show_tag(directory, _tags.FIGURE_NAME, undo=undo)),
            (
                "invisible music",
                [
                    _jobs.show_tag(
                        directory, _tags.INVISIBLE_MUSIC_COMMAND, undo=not undo
                    ),
                    _jobs.show_tag(
                        directory, _tags.INVISIBLE_MUSIC_COLORING, undo=undo
                    ),
                ],
            ),
            (
                "local measure numbers",
                _jobs.show_tag(directory, _tags.LOCAL_MEASURE_NUMBER, undo=undo),
            ),
            (
                "measure numbers",
                _jobs.show_tag(directory, _tags.MEASURE_NUMBER, undo=undo),
            ),
            (
                "mock coloring",
                _jobs.show_tag(directory, _tags.MOCK_COLORING, undo=undo),
            ),
            ("music annotations", _jobs.show_music_annotations(directory, undo=undo)),
            (
                "not yet pitched",
                _jobs.show_tag(directory, _tags.NOT_YET_PITCHED_COLORING, undo=undo),
            ),
            (
                "rhythm annotation spanners",
                _jobs.show_tag(directory, _tags.RHYTHM_ANNOTATION_SPANNER, undo=undo),
            ),
            ("spacing", spacing),
            ("stage number", _jobs.show_tag(directory, _tags.STAGE_NUMBER, undo=undo)),
        ]

        header = "available annotation jobs"
        prompt = "select annotation job"
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
                self.io.display(f"matches no annotation job {response.string!r} ...")
            return
        assert isinstance(response.payload, list), response
        result = response.payload
        return result

    def _select_color_jobs(self):
        items = [
            ("clefs", _jobs.color_clefs),
            ("dynamics", _jobs.color_dynamics),
            ("instruments", _jobs.color_instruments),
            ("margin markup", _jobs.color_margin_markup),
            ("metronome marks", _jobs.color_metronome_marks),
            ("persistent indicators", _jobs.color_persistent_indicators),
            ("staff lines", _jobs.color_staff_lines),
            ("time signatures", _jobs.color_time_signatures),
        ]
        header = "available color jobs"
        prompt = "select color job"
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
                self.io.display(f"matches no color job {response.string!r} ...")
            return
        assert isinstance(response.payload, list), response
        result = response.payload
        return result

    def _select_parts(self, directory, verb=""):
        part_manifest = _segments.get_part_manifest(directory)
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
            prompt = "select parts"
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
    def _test_segment_illustration(directory):
        # only run on Travis because segment illustration usually takes a while
        if not os.getenv("TRAVIS"):
            return
        abjad_ide = AbjadIDE()
        with abjad.FilesystemState(keep=[directory]):
            ly = directory / "illustration.ly"
            ly_old = directory / "illustration.old.ly"
            if ly.exists():
                shutil.copyfile(ly, ly_old)
            ily = directory / "illustration.ily"
            ily_old = directory / "illustration.old.ily"
            if ily.exists():
                shutil.copyfile(ily, ily_old)
            exit_code = abjad_ide.make_illustration_pdf(directory, open_after=False)
            if exit_code != 0:
                sys.exit(exit_code)
            if not ly_old.exists():
                return
            assert ly.exists()
            assert ly_old.exists()
            if not abjad.iox.compare_files(ly_old, ly):
                ly_old_text = ly_old.read_text().splitlines(keepends=True)
                ly_text = ly.read_text().splitlines(keepends=True)
                print("".join(difflib.ndiff(ly_old_text, ly_text)))
                sys.exit(1)
            if not ily_old.exists():
                return
            assert ily.exists()
            assert ily_old.exists()
            if not abjad.iox.compare_files(ily_old, ily):
                ily_old_text = ily_old.read_text().splitlines(keepends=True)
                ily_text = ily.read_text().splitlines(keepends=True)
                print("".join(difflib.ndiff(ily_old_text, ily_text)))
                sys.exit(1)

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
    def current_directory(self) -> typing.Optional[pathx.Path]:
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
        path: pathx.Path,
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
        path: pathx.Path,
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

    def run(
        self,
        job: Job,
        *,
        indent: int = 0,
        quiet: bool = False,
    ) -> None:
        """
        Runs ``job`` on ``path``.
        """
        message_zero = not bool(quiet)
        job = abjad.new(job, message_zero=message_zero)
        messages: typing.List[abjad.String] = job()
        self.io.display(messages, indent=indent)

    ### USER METHODS ###

    @Command(
        "ppb",
        description="part.pdf - build",
        menu_section="parts",
        score_package_paths=("part", "parts"),
    )
    def build_part_pdf(self, directory: pathx.Path) -> None:
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
        path_count = len(paths)
        for i, path in enumerate(paths):
            part = _segments.path_to_part(path)
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
    def build_score_pdf(self, directory: pathx.Path) -> None:
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
        "dpc",
        description="definition.py - check",
        menu_section="definition",
        score_package_paths=("definitionspace",),
    )
    def check_definition_py(self, directory: pathx.Path) -> int:
        """
        Checks ``definition.py``.

        Returns integer exit code for Travis tests.
        """
        assert directory.is_definitionspace()
        if directory.is_segment():
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
        score_package_paths=("segment", "segments"),
    )
    def check_out_optimization(self, directory: pathx.Path) -> None:
        """
        Checks out ``.optimization``.
        """
        assert directory.is_segment() or directory.is_segments()
        if directory.is_segment():
            paths = [directory / ".optimization"]
        else:
            paths = []
            for path in directory.list_paths():
                optimization = pathx.Path(path / ".optimization")
                if optimization.is_file():
                    paths.append(optimization)
        self._check_out_paths(paths)

    @Command(
        "ggc",
        description="segments - collect",
        menu_section="segments",
        score_package_paths=("_segments", "build"),
    )
    def collect_segment_lys(
        self,
        directory: pathx.Path,
        *,
        indent=0,
        skip: bool = False,
    ) -> None:
        """
        Collects segment lys.

        Copies illustration.ly, .ily files from segment directories to
        build/_segments directory.

        Trims top-level comments, header block, paper block from each file.

        Keeps score block in each file.

        Handles build tags.
        """
        assert directory.is_build() or directory.is__segments()
        if skip:
            self.io.display("skipping segment ly collection ...")
            return
        else:
            self.io.display("collecting segment lys ...")
        pairs = self._collect_segment_lys(directory.build)
        if not pairs:
            self.io.display("... no segment lys found.")
            return
        _make__assets_directory(directory.build)
        _make__segments_directory(directory.build)
        fermata_measure_numbers = abjad.OrderedDict()
        time_signatures = abjad.OrderedDict()
        for source, target in pairs:
            source_ily = source.with_suffix(".ily")
            target_ily = target.with_suffix(".ily")
            if target_ily.exists():
                self.io.display(f"Removing {target_ily.trim()} ...", indent=indent + 1)
            if source_ily.is_file():
                self.io.display(
                    f"Writing {target_ily.trim()} ...",
                    indent=indent + 1,
                )
                shutil.copyfile(str(source_ily), target_ily)
            if target.exists():
                self.io.display(
                    f"Removing {target.trim()} ...",
                    indent=indent + 1,
                )
            self.io.display(
                f"Writing {target.trim()} ...",
                indent=indent + 1,
            )
            text = _trim_illustration_ly(source)
            target.write_text(text)
            segment = source.parent
            value = segment.get_metadatum("fermata_measure_numbers")
            if value:
                fermata_measure_numbers[segment.name] = value
            value = segment.get_metadatum("time_signatures")
            if value:
                time_signatures[segment.name] = value
        key = "fermata_measure_numbers"
        if bool(fermata_measure_numbers):
            message = "writing fermata measure numbers to metadata ..."
            self.io.display(message, indent=indent + 1)
            directory.contents.add_metadatum(key, fermata_measure_numbers)
        else:
            message = "removing fermata measure numbers from metadata ..."
            self.io.display(message, indent=indent + 1)
            directory.contents.remove_metadatum(key)
        key = "time_signatures"
        if bool(time_signatures):
            message = "writing time signatures to metadata ..."
            self.io.display(message, indent=indent + 1)
            directory.contents.add_metadatum(key, time_signatures)
        else:
            message = "removing time signatures from metadata ..."
            self.io.display(message, indent=indent + 1)
            directory.contents.remove_metadatum(key)
        self.handle_build_tags(directory, indent=indent)

    @Command(
        "color",
        description="color",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def color(self, directory: pathx.Path) -> None:
        """
        Colors persistent indicators.
        """
        assert directory.is_buildspace()
        color_jobs = self._select_color_jobs()
        if self.is_navigation(color_jobs):
            return
        assert isinstance(color_jobs, list)
        for job in color_jobs:
            job_ = job(directory)
            self.run(job_)

    @Command(
        "cbc",
        description="clipboard - copy",
        external_directories=True,
        menu_section="clipboard",
        score_package_paths=True,
        scores_directory=True,
    )
    def copy_to_clipboard(self, directory: pathx.Path) -> None:
        """
        Copies to clipboard.
        """
        paths = self._select_paths(directory, infinitive="for clipboard")
        if self.is_navigation(paths):
            return
        assert isinstance(paths, list)
        self.io.display("copying to clipboard ...")
        for path in paths:
            self.io.display(f"    {path.trim()}", raw=True)
            self.clipboard.append(path)

    @Command(
        "bcte",
        description="back-cover.tex - edit",
        menu_section="back cover",
        score_package_paths=("_segments", "build"),
    )
    def edit_back_cover_tex(self, directory: pathx.Path) -> None:
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
        score_package_paths=("definitionspace",),
    )
    def edit_definition_py(self, directory: pathx.Path) -> None:
        """
        Edits ``definition.py``.
        """
        assert directory.is_definitionspace()
        paths = []
        if directory.is_segment():
            paths.append(directory / "definition.py")
        else:
            for path in directory.list_paths():
                definition_py = pathx.Path(path / "definition.py")
                if definition_py.is_file():
                    paths.append(definition_py)
        self._open_files(paths)

    @Command(
        "ef",
        description="edit - files",
        external_directories=True,
        menu_section="edit",
        score_package_paths=True,
        scores_directory=True,
    )
    def edit_files(self, directory: pathx.Path, pattern: str = None) -> None:
        """
        Edits all files.
        """
        files, strings = _find_editable_files(directory, force=True)
        pattern = self.io.get("pattern")
        if self.is_navigation(pattern):
            return
        files = self._match_files(files, strings, pattern)
        files = [_ for _ in files if "__pycache__" not in str(_)]
        files = [_ for _ in files if ".mypy_cache" not in str(_)]
        self._open_files(files, warn=1)

    @Command(
        "fcte",
        description="front-cover.tex - edit",
        menu_section="front cover",
        score_package_paths=("_segments", "build"),
    )
    def edit_front_cover_tex(self, directory: pathx.Path) -> None:
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
        score_package_paths=("segment", "segments"),
    )
    def edit_illustration_ily(self, directory: pathx.Path) -> None:
        """
        Edits ``illustration.ily``.
        """
        assert directory.is_segment() or directory.is_segments()
        if directory.is_segment():
            paths = [directory / "illustration.ily"]
        else:
            paths = []
            for path in directory.list_paths():
                illustration_ily = pathx.Path(path / "illustration.ily")
                if illustration_ily.is_file():
                    paths.append(illustration_ily)
        self._open_files(paths)

    @Command(
        "ile",
        description="illustration.ly - edit",
        menu_section="illustration",
        score_package_paths=("segment", "segments"),
    )
    def edit_illustration_ly(self, directory: pathx.Path) -> None:
        """
        Edits ``illustration.ly``.
        """
        assert directory.is_segment() or directory.is_segments()
        if directory.is_segment():
            paths = [directory / "illustration.ly"]
        else:
            paths = []
            for path in directory.list_paths():
                illustration_ly = pathx.Path(path / "illustration.ly")
                if illustration_ly.is_file():
                    paths.append(illustration_ly)
        self._open_files(paths)

    @Command(
        "lle",
        description="layout.ly - edit",
        menu_section="layout",
        score_package_paths=("buildspace",),
    )
    def edit_layout_ly(self, directory: pathx.Path) -> None:
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
    def edit_layout_py(self, directory: pathx.Path) -> None:
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
        "le",
        description=".log - edit",
        menu_section="illustration",
        score_package_paths=("buildspace",),
    )
    def edit_log(self, directory: pathx.Path) -> None:
        """
        Edits ``.log``.
        """
        assert directory.is_buildspace()
        if directory.is_segment() or directory.is_build():
            paths = [directory / ".log"]
        else:
            paths = []
            for path in directory.list_paths():
                illustration_ily = pathx.Path(path / ".log")
                if illustration_ily.is_file():
                    paths.append(illustration_ily)
        self._open_files(paths, force_vim=True)

    @Command(
        "mle",
        description="music.ly - edit",
        menu_section="music",
        score_package_paths=("_segments", "build"),
    )
    def edit_music_ly(self, directory: pathx.Path) -> None:
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
        score_package_paths=("segment", "segments"),
    )
    def edit_optimization(self, directory: pathx.Path) -> None:
        """
        Edits ``.optimization``.
        """
        assert directory.is_segment() or directory.is_segments()
        if directory.is_segment():
            paths = [directory / ".optimization"]
        else:
            paths = []
            for path in directory.list_paths():
                optimization = pathx.Path(path / ".optimization")
                if optimization.is_file():
                    paths.append(optimization)
        self._open_files(paths, force_vim=True)

    @Command(
        "pte",
        description="part.tex - edit",
        menu_section="parts",
        score_package_paths=("part", "parts"),
    )
    def edit_part_tex(self, directory: pathx.Path) -> None:
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
    def edit_preface_tex(self, directory: pathx.Path) -> None:
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
    def edit_score_tex(self, directory: pathx.Path) -> None:
        """
        Edits ``score.tex``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        path = directory.build / "score.tex"
        self._open_files([path])

    @Command(
        "es",
        description="edit - string",
        external_directories=True,
        menu_section="edit",
        score_package_paths=True,
        scores_directory=True,
    )
    def edit_string(self, directory: pathx.Path) -> None:
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
            command = f"vim -c \"grep '{search_string}' {options}\""
            self.io.display(command, raw=True)
            abjad.iox.spawn_subprocess(command)

    @Command(
        "ssie",
        description="stylesheet.ily - edit",
        menu_section="stylesheet",
        score_package_paths=("_segments", "build"),
    )
    def edit_stylesheet_ily(self, directory: pathx.Path) -> None:
        """
        Edits ``stylesheet.ily``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        path = directory.build / "stylesheet.ily"
        self._open_files([path])

    @Command(
        "cbe",
        description="clipboard - empty",
        external_directories=True,
        menu_section="clipboard",
        score_package_paths=True,
        scores_directory=True,
    )
    def empty_clipboard(self, directory: pathx.Path) -> None:
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
    def generate_back_cover_tex(self, directory: pathx.Path) -> None:
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
        total_parts = len(_segments.get_part_manifest(directory.build))
        path_count = len(paths)
        for i, path in enumerate(paths):
            part = _segments.path_to_part(path)
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
    def generate_front_cover_tex(self, directory: pathx.Path) -> None:
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
            part = _segments.path_to_part(path)
            forces_tagline = _part_subtitle(part.name, parentheses=False)
            self._generate_front_cover_tex(path, forces_tagline=forces_tagline)
            if i + 1 < path_count:
                self.io.display("")

    @Command(
        "lpg",
        description="layout.py - generate",
        menu_section="layout",
        score_package_paths=("buildspace",),
    )
    def generate_layout_py(self, directory: pathx.Path) -> None:
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
            part = _segments.path_to_part(path)
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
    def generate_music_ly(self, directory: pathx.Path, *, skip: bool = None) -> None:
        """
        Generates ``music.ly``.
        """
        assert directory.is__segments() or directory.is_build()
        assert directory.build is not None
        name = "music.ly"
        if skip:
            path = directory.build / name
            self.io.display(f"skipping {path.trim()} generation ...")
            return
        if not (directory.build.is_parts() or directory.is_part()):
            path = directory.build / name
            self._generate_score_music_ly(path)
            return
        name, verb = "music.ly", "generate"
        paths = self._select_paths_in_buildspace(directory, name, verb)
        if self.is_navigation(paths):
            return
        if not paths:
            return
        path_count = len(paths)
        for i, path in enumerate(paths):
            part = _segments.path_to_part(path)
            assert isinstance(part, Part)
            dashed_part_name = abjad.String(part.name).to_dash_case()
            file_name = f"{dashed_part_name}-{name}"
            assert path.build is not None
            path = path.build / file_name
            forces_tagline = _part_subtitle(part.name) + " part"
            part_subtitle = _part_subtitle(part.name, parentheses=True)
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
    def generate_part_tex(self, directory: pathx.Path) -> None:
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
            part = _segments.path_to_part(path)
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
    def generate_preface_tex(self, directory: pathx.Path) -> None:
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
    def generate_score_tex(self, directory: pathx.Path) -> None:
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
    def generate_stylesheet_ily(self, directory: pathx.Path) -> None:
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
        self._copy_boilerplate(directory.build, "stylesheet.ily", values=values)

    #    @Command(
    #        "ci",
    #        description="git - commit",
    #        external_directories=True,
    #        menu_section="git",
    #        score_package_paths=True,
    #        scores_directory=True,
    #    )
    #    def git_commit(self, directory: pathx.Path, commit_message: str = None) -> None:
    #        """
    #        Commits working copy.
    #        """
    #        if not directory.is_scores():
    #            root = _get_repository_root(directory)
    #            if not root:
    #                self.io.display(f"missing {directory.trim()} repository ...")
    #                return
    #            with self.change(root):
    #                if not _has_pending_commit(root):
    #                    self.io.display("nothing to commit ...")
    #                    return
    #                if self.test:
    #                    return
    #                command = f"git add -A {root}"
    #                self.io.display(f"Running {command} ...")
    #                lines = abjad.iox.run_command(command)
    #                self.io.display(lines, raw=True)
    #                if commit_message is None:
    #                    commit_message = self.io.get("commit message")
    #                    assert isinstance(commit_message, str)
    #                    if self.is_navigation(commit_message):
    #                        return
    #                command = f'git commit -m "{commit_message}" {root}'
    #                command += "; git push"
    #                lines = abjad.iox.run_command(command)
    #                self.io.display(lines, raw=True)
    #        else:
    #            assert directory.is_scores()
    #            commit_message = self.io.get("commit message")
    #            assert isinstance(commit_message, str)
    #            if self.is_navigation(commit_message):
    #                return
    #            paths = directory.list_paths()
    #            for i, path in enumerate(paths):
    #                self.io.display(f"{path} ...")
    #                self.git_commit(path, commit_message=commit_message)
    #                if i + 1 < len(paths):
    #                    self.io.display("")

    @Command(
        "diff",
        description="git - diff",
        external_directories=True,
        menu_section="git",
        score_package_paths=True,
        scores_directory=True,
    )
    def git_diff(self, directory: pathx.Path) -> None:
        """
        Displays Git diff of working copy.
        """
        if not directory.is_scores():
            if not _get_repository_root(directory):
                self.io.display(f"missing {directory.trim()} repository ...")
                return
            with self.change(directory):
                command = "git diff ."
                self.io.display(f"Running {command} ...")
                abjad.iox.spawn_subprocess(command)
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
    def git_pull(self, directory: pathx.Path) -> None:
        """
        Pulls working copy.
        """
        if not directory.is_scores():
            root = _get_repository_root(directory)
            if not root:
                self.io.display(f"missing {directory.trim()} repository ...")
                return
            with self.change(root):
                command = "git pull"
                self.io.display(f"Running {command} ...")
                if self.test:
                    return
                lines = abjad.iox.run_command(command)
                if lines and "Already up to date" in lines[-1]:
                    lines = lines[-1:]
                self.io.display(lines)
                command = "git submodule foreach git pull origin master"
                self.io.display(f"Running {command} ...")
                lines = abjad.iox.run_command(command)
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
    def git_push(self, directory: pathx.Path) -> None:
        """
        Pushes working copy.
        """
        if not directory.is_scores():
            root = _get_repository_root(directory)
            if not root:
                self.io.display(f"missing {directory.trim()} repository ...")
                return
            with self.change(root):
                command = "git push"
                self.io.display(f"Running {command} ...")
                if self.test:
                    return
                abjad.iox.spawn_subprocess(command)
        else:
            assert directory.is_scores()
            paths = directory.list_paths()
            for i, path in enumerate(paths):
                self.io.display(f"{path} ...")
                self.git_push(path)
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
    def go_to_builds_directory(self, directory: pathx.Path) -> None:
        """
        Goes to builds directory.
        """
        assert directory.is_score_package_path()
        assert directory.builds is not None
        assert directory.builds._assets is not None
        if not directory.builds._assets.exists():
            _make__assets_directory(directory.builds)
        if not (directory.builds / "__metadata__.py").is_file():
            directory.builds.write_metadata_py(abjad.OrderedDict())
        self._manage_directory(directory.builds)

    @Command(
        "cc",
        description="directory - contents",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_contents_directory(self, directory: pathx.Path) -> None:
        """
        Goes to contents directory.
        """
        assert directory.is_score_package_path()
        self._manage_directory(directory.contents)

    @Command(
        "dd",
        description="directory - distribution",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_distribution_directory(self, directory: pathx.Path) -> None:
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
    def go_to_etc_directory(self, directory: pathx.Path) -> None:
        """
        Goes to etc directory.
        """
        assert directory.is_score_package_path()
        assert directory.etc is not None
        self._manage_directory(directory.etc)

    @Command(
        ">",
        description="hop - next package",
        menu_section="hop",
        score_package_paths=("segment", "segments"),
    )
    def go_to_next_package(self, directory: pathx.Path) -> None:
        """
        Goes to next package.
        """
        assert directory.is_segment() or directory.is_segments()
        next_package = directory.get_next_package(cyclic=True)
        self._manage_directory(next_package)

    @Command(
        ">>",
        description="hop - next score",
        menu_section="hop",
        score_package_paths=True,
        scores_directory=True,
    )
    def go_to_next_score(self, directory: pathx.Path) -> None:
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
        score_package_paths=("segment", "segments"),
    )
    def go_to_previous_package(self, directory: pathx.Path) -> None:
        """
        Goes to previous package.
        """
        assert directory.is_segment() or directory.is_segments()
        previous_package = directory.get_previous_package(cyclic=True)
        self._manage_directory(previous_package)

    @Command(
        "<<",
        description="hop - previous score",
        menu_section="hop",
        score_package_paths=True,
        scores_directory=True,
    )
    def go_to_previous_score(self, directory: pathx.Path) -> None:
        """
        Goes to previous score.
        """
        assert directory.is_score_package_path() or directory.is_scores()
        wrapper = directory.get_previous_score(cyclic=True)
        assert wrapper is not None
        self._manage_directory(wrapper.contents)

    @Command(
        "ss",
        description="directory - scores",
        external_directories=True,
        menu_section="directory",
        score_package_paths=True,
        scores_directory=True,
    )
    def go_to_scores_directory(self) -> None:
        """
        Goes to scores directory.
        """
        directory = pathx.Path(self.configuration.composer_scores_directory)
        if self.test or self.example:
            directory = self.configuration.test_scores_directory
        self._manage_directory(directory)

    @Command(
        "gg",
        description="directory - segments",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_segments_directory(self, directory: pathx.Path) -> None:
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
    def go_to_stylesheets_directory(self, directory: pathx.Path) -> None:
        """
        Goes to stylesheets directory.
        """
        assert directory.is_score_package_path()
        assert directory.stylesheets is not None
        self._manage_directory(directory.stylesheets)

    @Command(
        "ww",
        description="directory - wrapper",
        menu_section="directory",
        score_package_paths=True,
    )
    def go_to_wrapper_directory(self, directory: pathx.Path) -> None:
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
        "btags",
        description="segments - handle build tags",
        menu_section="segments",
        score_package_paths=("_segments", "build"),
    )
    def handle_build_tags(
        self,
        directory: pathx.Path,
        *,
        indent=0,
        skip: bool = False,
    ) -> None:
        """
        Handles build tags.
        """
        assert directory.is_build() or directory.is__segments()
        if skip:
            self.io.display("skipping build tags ...")
            return
        else:
            self.io.display("handling build tags ...")
        pairs = self._collect_segment_lys(directory.build)
        final_source, final_target = list(pairs)[-1]
        final_file_name = final_target.with_suffix(".ily").name

        def match_left_broken_should_deactivate(tags):
            if _tags.LEFT_BROKEN in tags and _tags.SPANNER_START in tags:
                return True
            if (
                _tags.LEFT_BROKEN in tags
                and _tags.SPANNER_STOP in tags
                and _tags.EXPLICIT_DYNAMIC in tags
            ):
                return True
            return False

        def match_phantom_should_activate(tags):
            if _tags.PHANTOM not in tags:
                return False
            if _tags.ONE_VOICE_COMMAND in tags:
                return True
            if _tags.SHOW_TO_JOIN_BROKEN_SPANNERS in tags:
                return True
            if _tags.SPANNER_STOP in tags:
                return True
            return False

        def match_phantom_should_deactivate(tags):
            if _tags.PHANTOM not in tags:
                return False
            if _tags.SPANNER_START in tags and _tags.LEFT_BROKEN in tags:
                return True
            if _tags.SPANNER_STOP in tags and _tags.RIGHT_BROKEN in tags:
                return True
            if _tags.HIDE_TO_JOIN_BROKEN_SPANNERS in tags:
                return True
            return False

        _segments = directory._segments
        for job in [
            _jobs.handle_edition_tags(_segments),
            _jobs.handle_fermata_bar_lines(directory),
            _jobs.handle_shifted_clefs(_segments),
            _jobs.handle_mol_tags(_segments),
            _jobs.color_persistent_indicators(_segments, undo=True),
            _jobs.show_music_annotations(_segments, undo=True),
            _jobs.join_broken_spanners(_segments),
            _jobs.show_tag(
                _segments,
                "left-broken-should-deactivate",
                match=match_left_broken_should_deactivate,
                undo=True,
            ),
            _jobs.show_tag(_segments, _tags.PHANTOM, skip_file_name=final_file_name),
            _jobs.show_tag(
                _segments,
                _tags.PHANTOM,
                prepend_empty_chord=True,
                skip_file_name=final_file_name,
                undo=True,
            ),
            _jobs.show_tag(
                _segments,
                "phantom-should-activate",
                match=match_phantom_should_activate,
                skip_file_name=final_file_name,
            ),
            _jobs.show_tag(
                _segments,
                "phantom-should-deactivate",
                match=match_phantom_should_deactivate,
                skip_file_name=final_file_name,
                undo=True,
            ),
            _jobs.show_tag(
                _segments,
                _tags.EOS_STOP_MM_SPANNER,
                skip_file_name=final_file_name,
            ),
            _jobs.show_tag(
                _segments,
                _tags.METRIC_MODULATION_IS_STRIPPED,
                undo=True,
            ),
            _jobs.show_tag(
                _segments,
                _tags.METRIC_MODULATION_IS_SCALED,
                undo=True,
            ),
        ]:
            self.run(job, indent=1, quiet=False)

    @Command(
        "ptags",
        description="segments - handle part tags",
        menu_section="segments",
        score_package_paths=("_segments", "build"),
    )
    def handle_part_tags(
        self,
        directory: pathx.Path,
        *,
        indent=0,
        skip: bool = False,
    ) -> None:
        """
        Handles part tags.
        """
        assert directory.is_part(), repr(directory)
        parts_directory = directory.parent
        if skip:
            self.io.display("skipping part tags ...", indent=indent)
            return
        else:
            self.io.display("handling part tags ...", indent=indent)
        name = "music.ly"
        paths = self._select_paths_in_buildspace(directory.build, name, "foo")
        if not paths:
            message = "can not find {directory.trim()} music.ly file ..."
            self.io.display(message, indent=indent + 1)
        music_ly = paths[0]
        self.activate(
            parts_directory,
            "+PARTS",
            indent=indent + 1,
            message_zero=True,
        )
        self.deactivate(
            parts_directory,
            "-PARTS",
            indent=indent + 1,
            message_zero=True,
        )
        self.deactivate(
            parts_directory,
            "HIDE_IN_PARTS",
            indent=indent + 1,
            message_zero=True,
        )
        part_identifier = _parse_part_identifier(music_ly)
        if part_identifier is None:
            message = f"no part identifier found in {music_ly.trim()} ..."
            self.io.display(message, indent=indent + 1)
            return
        parts_directory_name = abjad.String(parts_directory.name)
        parts_directory_name = parts_directory_name.to_shout_case()
        name = f"{parts_directory_name}_{part_identifier}"
        self.activate(
            parts_directory,
            f"+{name}",
            indent=indent + 1,
            message_zero=True,
        )
        self.deactivate(
            parts_directory,
            f"-{name}",
            indent=indent + 1,
            message_zero=True,
        )
        self.deactivate(
            parts_directory,
            str(_tags.METRIC_MODULATION_IS_SCALED),
            indent=indent + 1,
            message_zero=True,
        )
        self.deactivate(
            parts_directory,
            str(_tags.METRIC_MODULATION_IS_NOT_SCALED),
            indent=indent + 1,
            message_zero=True,
        )
        self.activate(
            parts_directory,
            str(_tags.METRIC_MODULATION_IS_STRIPPED),
            indent=indent + 1,
            message_zero=True,
        )
        # HACK TO HIDE ALL POST-FERMATA-MEASURE TRANSPARENT BAR LINES;
        # this only works if parts contain no EOL fermata measure:
        self.deactivate(
            parts_directory,
            str(_tags.FERMATA_MEASURE),
            indent=indent + 1,
            message_zero=True,
        )
        self.activate(
            parts_directory,
            "NOT_TOPMOST",
            indent=indent + 1,
            message_zero=True,
        )
        self.deactivate(
            parts_directory,
            "FERMATA_MEASURE_EMPTY_BAR_EXTENT",
            indent=indent + 1,
            message_zero=True,
        )
        self.deactivate(
            parts_directory,
            "FERMATA_MEASURE_NEXT_BAR_EXTENT",
            indent=indent + 1,
            message_zero=True,
        )
        self.deactivate(
            parts_directory,
            "FERMATA_MEASURE_RESUME_BAR_EXTENT",
            indent=indent + 1,
            message_zero=True,
        )
        self.deactivate(
            parts_directory,
            str(_tags.EXPLICIT_BAR_EXTENT),
            indent=indent + 1,
            message_zero=True,
        )

    @Command(
        "hide",
        description="hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide(self, directory: pathx.Path) -> None:
        """
        Hides annotations.
        """
        assert directory.is_buildspace()
        jobs = self._select_annotation_jobs(directory, undo=True)
        if self.is_navigation(jobs):
            return
        assert isinstance(jobs, list)
        for item in jobs:
            if isinstance(item, list):
                for item_ in item:
                    self.run(item_)
            else:
                self.run(item)

    @Command(
        "th",
        description="tag - hide",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def hide_tag(self, directory: pathx.Path) -> None:
        """
        Hides arbitrary (user-specified) tag.
        """
        assert directory.is_buildspace()
        tag_ = self.io.get("tag")
        if self.is_navigation(tag_):
            return
        tag = abjad.Tag(tag_)
        self.run(_jobs.show_tag(directory, tag, undo=True))

    @Command(
        "bcti",
        description="back-cover.tex - interpret",
        menu_section="back cover",
        score_package_paths=("_segments", "build"),
    )
    def interpret_back_cover_tex(
        self, directory: pathx.Path, open_after: bool = True
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
        self, directory: pathx.Path, open_after: bool = True
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
        score_package_paths=("segment", "segments"),
    )
    def interpret_illustration_ly(
        self, directory: pathx.Path, open_after: bool = True
    ) -> None:
        """
        Interprets ``illustration.ly``.

        Makes ``illustration.pdf``.
        """
        assert directory.is_segment() or directory.is_segments()
        if directory.is_segment():
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
        directory: pathx.Path,
        *,
        open_after: bool = True,
        skip_segment_ly_collection: bool = False,
        skip_tags: bool = False,
    ) -> None:
        """
        Interprets ``music.ly`` (after first collecting segments and handling
        tags).
        """
        assert directory.is__segments() or directory.is_build()
        build = directory.build
        assert build is not None, repr(directory)
        message = f"interpreting {build.trim()} music.ly files ..."
        self.io.display(message)
        name, verb = "music.ly", "interpret"
        paths = self._select_paths_in_buildspace(directory.build, name, verb)
        if self.is_navigation(paths):
            return
        if not paths:
            self.generate_music_ly(directory)
            paths = self._select_paths_in_buildspace(directory.build, name, verb)
        path_count = len(paths)
        for path in paths:
            self.io.display(f"found {path.trim()} ...")
        self.collect_segment_lys(
            directory.build,
            skip=skip_segment_ly_collection,
        )
        for i, path in enumerate(paths):
            if path.parent.is_part():
                self.handle_part_tags(directory, skip=skip_tags)
            self._check_layout_time_signatures(path)
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
        self, directory: pathx.Path, open_after: bool = True
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
        self, directory: pathx.Path, open_after: bool = True
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
        self, directory: pathx.Path, open_after: bool = True
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
        score_package_paths=("segment", "segments"),
    )
    def make_illustration_ly(self, directory: pathx.Path) -> None:
        """
        Makes ``illustration.ly``.
        """
        assert directory.is_segment() or directory.is_segments()
        if directory.is_segment():
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
        score_package_paths=("segment", "segments"),
    )
    def make_illustration_pdf(
        self, directory: pathx.Path, layout: bool = True, open_after: bool = True
    ) -> int:
        """
        Makes ``illustration.pdf``.

        Returns integer exit code for Travis tests.
        """
        assert directory.is_segment() or directory.is_segments()
        if directory.is_segment():
            return self._make_segment_pdf(
                directory, layout=layout, open_after=open_after
            )
        else:
            assert directory.is_segments()
            exit = 0
            paths = directory.list_paths()
            paths = [_ for _ in paths if _.is_dir()]
            for i, path in enumerate(paths):
                exit_ = self.make_illustration_pdf(path, open_after=False)
                if i + 1 < len(paths):
                    self.io.display("")
                else:
                    abjad.iox.spawn_subprocess('say "done"')
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
    def make_layout_ly(self, directory: pathx.Path) -> None:
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
            if not layout_py.is_file():
                self.io.display(f"missing {layout_py.trim()} ...")
                continue
            self._make_layout_ly(layout_py)
            if i < path_count - 1:
                self.io.display("")

    @Command(
        "ctm",
        description="clicktrack - make",
        menu_section="segment.midi",
        score_package_paths=("segment", "segments"),
    )
    def make_segment_clicktrack(
        self, directory: pathx.Path, open_after: bool = True
    ) -> int:
        """
        Makes segment clicktrack file.

        Returns integer exit code for Travis tests.
        """
        assert directory.is_segment() or directory.is_segments()
        paths: typing.List[pathx.Path] = []
        if directory.is_segment():
            paths.append(directory)
        else:
            for path in directory.list_paths():
                if path.is_dir():
                    paths.append(path)
        for path in paths:
            result = self._make_segment_clicktrack(path, open_after=False)
        if len(paths) == 1:
            path = paths[0]
            score_name = path.contents.name
            segment_name = path.name
            midi = directory / f"{score_name}-{segment_name}-clicktrack.midi"
            if midi.is_file() and open_after:
                self._open_files([midi])
        return result

    @Command(
        "midm",
        description="segment.midi - make",
        menu_section="segment.midi",
        score_package_paths=("segment", "segments"),
    )
    def make_segment_midi(self, directory: pathx.Path, open_after: bool = True) -> int:
        """
        Makes segment MIDI file.

        Returns integer exit code for Travis tests.
        """
        assert directory.is_segment() or directory.is_segments()
        if directory.is_segment():
            return self._make_segment_midi(directory, open_after=open_after)
        else:
            assert directory.is_segments()
            exit = 0
            paths = directory.list_paths()
            paths = [_ for _ in paths if _.is_dir()]
            for i, path in enumerate(paths):
                exit_ = self._make_segment_midi(path, open_after=False)
                if i + 1 < len(paths):
                    self.io.display("")
                else:
                    abjad.iox.spawn_subprocess('say "done"')
                if exit_ != 0:
                    exit = -1
            return exit
        return 0

    @Command(
        "ipn",
        description="illustration.pdf - nake",
        menu_section="illustration",
        score_package_paths=("segment", "segments"),
    )
    def nake_illustration_pdf(self, directory: pathx.Path) -> int:
        """
        Makes ``illustration.pdf``; does not reinterpret ``layout.py``;
        does not open after.

        Returns integer exit code for Travis tests.
        """
        assert directory.is_segment() or directory.is_segments()
        return self.make_illustration_pdf(directory, layout=False, open_after=False)

    @Command(
        "new",
        description="path - new",
        menu_section="path",
        score_package_paths=("builds",),
    )
    def new(self, directory: pathx.Path) -> None:
        """
        Makes asset.
        """
        assert directory.is_builds(), repr(directory)
        type_ = self.io.get("score or parts?")
        if self.is_navigation(type_):
            return
        if type_ == "score":
            self._make_score_build_directory(directory)
        elif type_ == "parts":
            self._make_parts_directory(directory)

    @Command(
        "bcpo",
        description="back-cover.pdf - open",
        menu_section="back cover",
        score_package_paths=("_segments", "build"),
    )
    def open_back_cover_pdf(self, directory: pathx.Path) -> None:
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
    def open_front_cover_pdf(self, directory: pathx.Path) -> None:
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
        score_package_paths=("segment", "segments"),
    )
    def open_illustration_pdf(self, directory: pathx.Path) -> None:
        """
        Opens ``illustration.pdf``.
        """
        assert directory.is_segment() or directory.is_segments()
        if directory.is_segment():
            path = directory / "illustration.pdf"
            self._open_files([path])
        else:
            for path_ in directory.list_paths():
                self.open_illustration_pdf(path_)

    @Command(
        "mpo",
        description="music.pdf - open",
        menu_section="music",
        score_package_paths=("_segments", "build"),
    )
    def open_music_pdf(self, directory: pathx.Path) -> None:
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
    def open_part_pdf(self, directory: pathx.Path) -> None:
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
    def open_preface_pdf(self, directory: pathx.Path) -> None:
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
    def open_score_pdf(self, directory: pathx.Path) -> None:
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
    def paste_from_clipboard(self, directory: pathx.Path) -> None:
        """
        Pastes from clipboard.
        """
        self._purge_clipboard()
        if not bool(self.clipboard):
            self.io.display("showing empty clipboard ...")
            return
        self.io.display("pasting from clipboard ...")
        for i, source in enumerate(self.clipboard[:]):
            if not source.exists():
                continue
            target = directory / source.name
            if source == target:
                self.io.display(f"    Skipping {source.trim()} ...")
                continue
            self.io.display(f"    {source.trim()} ...")
            self.io.display(f"    {target.trim()} ...")
            if source.is_dir():
                shutil.copytree(str(source), str(target))
            else:
                shutil.copy(str(source), str(target))
            if i < len(self.clipboard) - 1:
                self.io.display("")
        self.clipboard[:] = []

    @Command(
        "lpp",
        description="layout.py - propagate",
        menu_section="layout",
        score_package_paths=("parts",),
    )
    def propagate_layout_py(self, directory: pathx.Path) -> None:
        """
        Propagates ``layout.py``.
        """
        assert directory.is_parts() or directory.is_part()
        name, verb = "layout.py", "use as source"
        paths = self._select_paths_in_buildspace(directory, name, verb, count=1)
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
        source_part_identifier = _parse_part_identifier(source)
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
            part_identifier = _segments.get_part_identifier(path)
            target_text = source_text.replace(source_part_identifier, part_identifier)
            self.io.display(f"writing {path.trim()} ...")
            path.write_text(target_text)

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
    def remove(self, directory: pathx.Path) -> None:
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
    def rename(self, directory: pathx.Path) -> None:
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
            name_ = name
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
                _replace_in_file(path, source.name, target.name, whole_words=True)

    @Command(
        "show",
        description="show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show(self, directory: pathx.Path) -> None:
        """
        Shows annotations.
        """
        assert directory.is_buildspace()
        jobs = self._select_annotation_jobs(directory)
        if self.is_navigation(jobs):
            return
        assert isinstance(jobs, list)
        for item in jobs:
            if isinstance(item, list):
                for item_ in item:
                    self.run(item_)
            else:
                self.run(item)

    @Command(
        "cbs",
        description="clipboard - show",
        external_directories=True,
        menu_section="clipboard",
        score_package_paths=True,
        scores_directory=True,
    )
    def show_clipboard(self, directory: pathx.Path) -> None:
        """
        Shows clipboard.
        """
        self._purge_clipboard()
        if not bool(self.clipboard):
            self.io.display("showing empty clipboard ...")
            return
        self.io.display("showing clipboard ...")
        for path in self.clipboard:
            self.io.display(path.trim(), raw=True)

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
        "ts",
        description="tag - show",
        menu_section="music annotations",
        score_package_paths=("buildspace",),
    )
    def show_tag(self, directory: pathx.Path) -> None:
        """
        Shows arbitrary (user-specified) tag.
        """
        assert directory.is_buildspace()
        tag_ = self.io.get("tag")
        if self.is_navigation(tag_):
            return
        tag = abjad.Tag(tag_)
        self.run(_jobs.show_tag(directory, tag))

    @Command(
        "uncolor",
        description="uncolor",
        menu_section="persistent indicators",
        score_package_paths=("buildspace",),
    )
    def uncolor(self, directory: pathx.Path) -> None:
        """
        Uncolors persistent indicators.
        """
        assert directory.is_buildspace()
        color_jobs = self._select_color_jobs()
        if self.is_navigation(color_jobs):
            return
        assert isinstance(color_jobs, list)
        for job in color_jobs:
            job_ = job(directory, undo=True)
            self.run(job_)

    @Command(
        "mlx",
        description="music.ly - xinterpret",
        menu_section="music",
        score_package_paths=("_segments", "build"),
    )
    def xinterpret_music_ly(
        self, directory: pathx.Path, open_after: bool = True
    ) -> None:
        """
        Interprets ``music.ly`` without collecting segment.lys or handling
        tags.
        """
        assert directory.is__segments() or directory.is_build()
        self.interpret_music_ly(
            directory,
            open_after=open_after,
            skip_segment_ly_collection=True,
            skip_tags=True,
        )
