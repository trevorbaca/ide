import importlib
import typing

import abjad

from .pathclass import Path
from .segments import Part, PartManifest


def _context_name_to_first_appearance_margin_markup(path, context_name):
    module = _import_score_package(path)
    margin_markups = getattr(module, "margin_markups", None)
    if not margin_markups:
        return []
    dictionary = abjad.OrderedDict()
    string = "first_appearance_margin_markup"
    for segment in path.segments.list_paths():
        dictionary_ = segment.get_metadatum(string, [])
        dictionary.update(dictionary_)
    key = dictionary.get(context_name)
    if key is None:
        return []
    margin_markup = margin_markups.get(key)
    if margin_markup is None:
        return []
    markup = margin_markup.markup
    assert markup is not None, repr(margin_markup)
    strings = markup._get_format_pieces()
    strings.insert(0, "shortInstrumentName =")
    indent = abjad.LilyPondFormatBundle.indent
    strings = [indent + _ for _ in strings]
    strings = [r"\with", "{"] + strings + ["}"]
    return strings


def _global_rest_identifier(segment_name: str) -> abjad.String:
    """
    Gets global rest identifier.

    ..  container:: example

        >>> ide.pathx._global_rest_identifier("_")
        'i_Global_Rests'

        >>> ide.pathx._global_rest_identifier("_1")
        'i_a_Global_Rests'

        >>> ide.pathx._global_rest_identifier("_2")
        'i_b_Global_Rests'

        >>> ide.pathx._global_rest_identifier("A")
        'A_Global_Rests'

        >>> ide.pathx._global_rest_identifier("A1")
        'A_a_Global_Rests'

        >>> ide.pathx._global_rest_identifier("A2")
        'A_b_Global_Rests'

    """
    identifier = abjad.String(segment_name).to_segment_lilypond_identifier()
    identifier = abjad.String(f"{identifier}_Global_Rests")
    return identifier


def _global_rest_identifiers(path) -> typing.List[abjad.String]:
    """
    Gets global rest identifiers.
    """
    assert not path.is_external(), repr(path)
    identifiers = []
    if path.segments is not None:
        paths = path.segments.list_paths()
    else:
        paths = []
    for segment in paths:
        identifier = abjad.String(segment.name).to_segment_lilypond_identifier()
        identifier = abjad.String(f"{identifier}_Global_Rests")
        identifiers.append(identifier)
    return identifiers


def _import_score_package(path):
    assert path.is_score_package_path()
    try:
        module = importlib.import_module(path.contents.name)
    except Exception:
        return
    return module


def _import_score_template(path):
    module = _import_score_package(path)
    if not module:
        raise Exception("can not import score package.")
    score_template = getattr(module, "ScoreTemplate", None)
    if not score_template:
        raise Exception("can not import score template.")
    return score_template


def _instrument_to_staff_identifiers(path, instrument: str) -> abjad.OrderedDict:
    """
    Changes ``instrument`` to staff identifiers dictionary.
    """
    assert not path.is_external(), repr(path)
    alive_during_segment = abjad.OrderedDict()
    if path.segments is not None:
        paths = path.segments.list_paths()
    else:
        paths = []
    for segment in paths:
        dictionary = segment.get_metadatum(
            "alive_during_segment", [], file_name="__persist__.py"
        )
        alive_during_segment[segment.name] = dictionary
    staves_in_score: typing.List[abjad.String] = []
    for segment_name, contexts in alive_during_segment.items():
        for context in contexts:
            if context.startswith(instrument):
                words = abjad.String(context).delimit_words()
                if words[-2] == "Staff" and abjad.String(words[-1]).is_roman():
                    if context not in staves_in_score:
                        staves_in_score.append(context)
    staves_in_score = abjad.String.sort_roman(staves_in_score)
    dictionary = abjad.OrderedDict()
    for staff in staves_in_score:
        dictionary[staff] = identifiers = []
        for segment_name, contexts in alive_during_segment.items():
            identifier = abjad.String(segment_name)
            identifier = identifier.to_segment_lilypond_identifier()
            if staff in contexts:
                identifier_ = f"{identifier}_{staff}"
            else:
                identifier_ = f"{identifier}_Global_Rests"
            identifier = abjad.String(identifier_)
            identifiers.append(identifier)
    return dictionary


def _part_name_to_default_clef(path, part_name):
    module = _import_score_package(path)
    instruments = getattr(module, "instruments", None)
    if not instruments:
        raise Exception(f"can not find instruments: {path!r}.")
    words = abjad.String(part_name).delimit_words()
    if words[-1].isdigit():
        words = words[:-1]
    if words[0] in ("First", "Second"):
        words = words[1:]
    key = "".join(words)
    instrument = instruments.get(key, None)
    if not instrument:
        raise Exception(f"can not find {key!r}.")
    clef = abjad.Clef(instrument.allowable_clefs[0])
    return clef


def get_measure_profile_metadata(path) -> typing.Tuple[int, int, list]:
    """
    Gets measure profile metadata.

    Reads segment metadata when path is segment.

    Reads score metadata when path is not segment.

    Returns tuple of three metadata: first measure number; measure count;
    list of fermata measure numbers.
    """
    if path.parent.is_segment():
        string = "first_measure_number"
        first_measure_number = path.parent.get_metadatum(string)
        time_signatures = path.parent.get_metadatum("time_signatures")
        if bool(time_signatures):
            measure_count = len(time_signatures)
        else:
            measure_count = 0
        string = "fermata_measure_numbers"
        fermata_measure_numbers = path.parent.get_metadatum(string)
    else:
        first_measure_number = 1
        dictionary = path.contents.get_metadatum("time_signatures")
        dictionary = dictionary or abjad.OrderedDict()
        measure_count = 0
        for segment, time_signatures in dictionary.items():
            measure_count += len(time_signatures)
        string = "fermata_measure_numbers"
        dictionary = path.contents.get_metadatum(string)
        dictionary = dictionary or abjad.OrderedDict()
        fermata_measure_numbers = []
        for segment, fermata_measure_numbers_ in dictionary.items():
            fermata_measure_numbers.extend(fermata_measure_numbers_)
    return (first_measure_number, measure_count, fermata_measure_numbers)


def get_part_identifier(path) -> typing.Optional[str]:
    """
    Gets part identifier in layout.py only.
    """
    if not path.name.endswith("layout.py"):
        return None
    for line in path.read_text().split("\n"):
        if line.startswith("part_identifier ="):
            globals_ = globals()
            exec(line, globals_)
            part_identifier = globals_["part_identifier"]
            return part_identifier
    return None


def get_part_manifest(path) -> PartManifest:
    """
    Gets part manifest from ``path``.
    """
    assert path.is_score_package_path()
    score_template = _import_score_template(path)
    score_template = score_template()
    part_manifest = score_template.part_manifest
    assert isinstance(part_manifest, PartManifest), repr(part_manifest)
    return part_manifest


def get_preamble_page_count_overview(
    path,
) -> typing.Optional[typing.Tuple[int, int, int]]:
    """
    Gets preamble page count overview.
    """
    assert path.is_file(), repr(path)
    first_page_number, page_count = 1, None
    with open(path) as pointer:
        for line in pointer.readlines():
            if line.startswith("% first_page_number = "):
                line = line.strip("% first_page_number = ")
                first_page_number = eval(line)
            if line.startswith("% page_count = "):
                line = line.strip("% page_count = ")
                page_count = eval(line)
    if isinstance(page_count, int):
        final_page_number = first_page_number + page_count - 1
        return first_page_number, page_count, final_page_number
    return None


def get_preamble_partial_score(path) -> bool:
    """
    Gets preamble time signatures.
    """
    assert path.is_file(), repr(path)
    prefix = "% partial_score ="
    with open(path) as pointer:
        for line in pointer.readlines():
            if line.startswith(prefix):
                line = line[len(prefix) :]
                partial_score = eval(line)
                return partial_score
    return False


def get_preamble_time_signatures(path) -> typing.Optional[typing.List[str]]:
    """
    Gets preamble time signatures.
    """
    assert path.is_file(), repr(path)
    start_line = "% time_signatures = ["
    stop_line = "%  ]"
    lines = []
    with open(path) as pointer:
        for line in pointer.readlines():
            if line.startswith(stop_line):
                lines.append("]")
                break
            if lines:
                lines.append(line.strip("%").strip("\n"))
            elif line.startswith(start_line):
                lines.append("[")
        string = "".join(lines)
        try:
            time_signatures = eval(string)
        except Exception:
            return []
        return time_signatures
    return None


def global_skip_identifiers(path) -> typing.List[abjad.String]:
    """
    Gets global skip identifiers.
    """
    assert not path.is_external(), repr(path)
    identifiers = []
    if path.segments is not None:
        paths = path.segments.list_paths()
    else:
        paths = []
    for segment in paths:
        identifier = abjad.String(segment.name).to_segment_lilypond_identifier()
        identifier = abjad.String(f"{identifier}_GlobalSkips")
        identifiers.append(identifier)
    return identifiers


def part_to_identifiers(
    path, part: Part, container_to_part_assignment: abjad.OrderedDict
) -> typing.Union[str, typing.List[str]]:
    """
    Changes ``part`` to (part container) identifiers (using
    ``container_to_part_assignment`` dictionary).
    """
    assert not path.is_external(), repr(path)
    if not isinstance(part, Part):
        raise TypeError(f"must be part (not {part!r}).")
    identifiers = []
    default_clef = _part_name_to_default_clef(path, part.name)
    clef_string = default_clef._get_lilypond_format()
    assert clef_string.startswith("\\"), repr(clef_string)
    clef_string = clef_string[1:]
    identifiers.append(clef_string)
    dictionary = container_to_part_assignment
    if not dictionary:
        message = "empty container-to-part-assignment dictionary"
        return message
    for i, (segment_name, dictionary_) in enumerate(dictionary.items()):
        pairs = []
        for identifier, (part_assignment, timespan) in dictionary_.items():
            if part in part_assignment:
                pairs.append((identifier, timespan))
        if pairs:
            pairs.sort(key=lambda pair: pair[1])
            identifiers_ = [_[0] for _ in pairs]
            identifiers.extend(identifiers_)
        else:
            identifier = _global_rest_identifier(segment_name)
            identifiers.append(identifier)
    return identifiers


def path_to_part(path: Path) -> Part:
    """
    Changes path to part.
    """
    assert path.parent.is_part(), repr(path)
    words = path.parent.name.split("-")
    part_manifest = get_part_manifest(path)
    if not part_manifest:
        raise Exception(f"no part manifest: {path}.")
    assert isinstance(part_manifest, PartManifest), repr(part_manifest)
    words = [abjad.String(_).capitalize_start() for _ in words]
    part_name = "".join(words)
    for part in part_manifest:
        if part.name == part_name:
            return part
    raise Exception(f"can not find {part_name!r} in part manifest.")


def remove_lilypond_warnings(
    path,
    crescendo_too_small: bool = None,
    decrescendo_too_small: bool = None,
    overwriting_glissando: bool = None,
) -> None:
    """
    Removes LilyPond warnings from ``.log``.
    """
    assert path.name == ".log", repr(path)
    lines = []
    skip = 0
    with open(path) as pointer:
        for line in pointer.readlines():
            if 0 < skip:
                skip -= 1
                continue
            if crescendo_too_small and "crescendo too small" in line:
                skip = 2
                continue
            if decrescendo_too_small and "decrescendo too small" in line:
                skip = 2
                continue
            if overwriting_glissando and "overwriting glissando" in line:
                skip = 1
                continue
            lines.append(line)
    text = "".join(lines)
    path.write_text(text)


def score_skeleton(path) -> typing.Optional[abjad.Score]:
    """
    Makes score skeleton.

    Only works when score template defines ``skeleton()`` method.
    """
    assert not path.is_external(), repr(path)
    score_template = _import_score_template(path)
    if not hasattr(score_template, "skeleton"):
        return None
    skeleton = score_template.skeleton()
    indent = abjad.LilyPondFormatBundle.indent
    context = skeleton["Global_Skips"]
    identifiers = global_skip_identifiers(path)
    strings = ["\\" + _ for _ in identifiers]
    literal = abjad.LilyPondLiteral(strings)
    abjad.attach(literal, context)
    context = skeleton["Global_Rests"]
    identifiers = _global_rest_identifiers(path)
    strings = ["\\" + _ for _ in identifiers]
    literal = abjad.LilyPondLiteral(strings)
    abjad.attach(literal, context)
    module = _import_score_package(path)
    instruments = getattr(module, "instruments", None)
    for staff_group in abjad.Iteration(skeleton).components(abjad.StaffGroup):
        if staff_group:
            continue
        assert len(staff_group) == 0, repr(staff_group)
        instrument = staff_group.name
        words = abjad.String(staff_group.name).delimit_words()
        if words[-3:] == ["Square", "Staff", "Group"]:
            words = words[:-3]
        elif words[-2:] == ["Piano", "Staff"]:
            words = words[:-2]
        elif words == ["Percussion", "Staff", "Group"]:
            words = [abjad.String("Percussion")]
        else:
            raise ValueError(staff_group)
        instrument = "".join(words)
        dictionary = _instrument_to_staff_identifiers(path, instrument)
        if instrument in ("FirstViolin", "SecondViolin"):
            key = "Violin"
        else:
            key = instrument
        abjad_instrument = instruments.get(key, None)
        if not abjad_instrument:
            raise Exception(f"can not find {key!r}.")
        clef = abjad.Clef(abjad_instrument.allowable_clefs[0])
        clef_string = clef._get_lilypond_format()
        strings = []
        method = _context_name_to_first_appearance_margin_markup
        for staff_name, identifiers in dictionary.items():
            strings.append("{")
            for i, identifier in enumerate(identifiers):
                string = indent + rf'\context Staff = "{staff_name}"'
                strings.append(string)
                if i == 0:
                    margin_markup_strings = method(path, staff_name)
                    for string_ in margin_markup_strings:
                        strings.append(indent + string_)
                    strings.append(indent + clef_string)
                string = indent + "\\" + identifier
                strings.append(string)
            strings.append("}")
        literal = abjad.LilyPondLiteral(strings)
        abjad.attach(literal, staff_group)
    return skeleton
