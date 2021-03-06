import abjad
import ide

metadata = abjad.OrderedDict(
    [
        ("bol_measure_numbers", [1]),
        ("duration", "0'08''"),
        ("fermata_measure_numbers", [2]),
        ("final_measure_is_fermata", True),
        ("final_measure_number", 2),
        ("first_measure_number", 1),
        (
            "persistent_indicators",
            abjad.OrderedDict(
                [
                    (
                        "BassClarinetMusicStaff",
                        [
                            ide.Momento(
                                context="BassClarinetMusicVoice",
                                prototype="abjad.Clef",
                                value="treble",
                            ),
                            ide.Momento(
                                context="BassClarinetMusicVoice",
                                prototype="abjad.Instrument",
                                value="BassClarinet",
                            ),
                            ide.Momento(
                                context="BassClarinetMusicVoice",
                                prototype="baca.StaffLines",
                                value=5,
                            ),
                        ],
                    ),
                    (
                        "CelloMusicStaff",
                        [
                            ide.Momento(
                                context="CelloMusicVoice",
                                prototype="abjad.Clef",
                                value="treble",
                            ),
                            ide.Momento(
                                context="CelloMusicVoice",
                                prototype="baca.StaffLines",
                                value=5,
                            ),
                        ],
                    ),
                    (
                        "CelloMusicVoice",
                        [
                            ide.Momento(
                                context="CelloMusicVoice",
                                prototype="abjad.Dynamic",
                                value="sfz",
                            )
                        ],
                    ),
                    (
                        "CelloRHMusicStaff",
                        [
                            ide.Momento(
                                context="CelloRHMusicVoice",
                                prototype="abjad.Clef",
                                value="percussion",
                            ),
                            ide.Momento(
                                context="CelloRHMusicVoice",
                                prototype="baca.StaffLines",
                                value=1,
                            ),
                        ],
                    ),
                    (
                        "CelloStaffGroup",
                        [
                            ide.Momento(
                                context="CelloMusicVoice",
                                prototype="abjad.Instrument",
                                value="Cello",
                            )
                        ],
                    ),
                    (
                        "Score",
                        [
                            ide.Momento(
                                context="GlobalSkips",
                                prototype="abjad.MetronomeMark",
                                value="incisions",
                            ),
                            ide.Momento(
                                context="GlobalSkips",
                                prototype="abjad.TimeSignature",
                                value="1/4",
                            ),
                        ],
                    ),
                    (
                        "ViolaMusicStaff",
                        [
                            ide.Momento(
                                context="ViolaMusicVoice",
                                prototype="abjad.Clef",
                                value="alto",
                            ),
                            ide.Momento(
                                context="ViolaMusicVoice",
                                prototype="baca.StaffLines",
                                value=5,
                            ),
                        ],
                    ),
                    (
                        "ViolaRHMusicStaff",
                        [
                            ide.Momento(
                                context="ViolaRHMusicVoice",
                                prototype="abjad.Clef",
                                value="percussion",
                            ),
                            ide.Momento(
                                context="ViolaRHMusicVoice",
                                prototype="baca.StaffLines",
                                value=1,
                            ),
                        ],
                    ),
                    (
                        "ViolaStaffGroup",
                        [
                            ide.Momento(
                                context="ViolaMusicVoice",
                                prototype="abjad.Instrument",
                                value="Viola",
                            )
                        ],
                    ),
                    (
                        "ViolinMusicStaff",
                        [
                            ide.Momento(
                                context="ViolinMusicVoice",
                                prototype="abjad.Clef",
                                value="percussion",
                            ),
                            ide.Momento(
                                context="ViolinMusicVoice",
                                prototype="baca.StaffLines",
                                value=1,
                            ),
                        ],
                    ),
                    (
                        "ViolinMusicVoice",
                        [
                            ide.Momento(
                                context="ViolinMusicVoice",
                                prototype="abjad.Dynamic",
                                value="\\effort_mf",
                            )
                        ],
                    ),
                    (
                        "ViolinRHMusicStaff",
                        [
                            ide.Momento(
                                context="ViolinRHMusicVoice",
                                prototype="abjad.Clef",
                                value="percussion",
                            ),
                            ide.Momento(
                                context="ViolinRHMusicVoice",
                                prototype="baca.StaffLines",
                                value=1,
                            ),
                        ],
                    ),
                    (
                        "ViolinStaffGroup",
                        [
                            ide.Momento(
                                context="ViolinMusicVoice",
                                prototype="abjad.Instrument",
                                value="Violin",
                            )
                        ],
                    ),
                ]
            ),
        ),
        ("segment_number", 1),
        ("start_clock_time", "0'00''"),
        ("stop_clock_time", "0'08''"),
        ("time_signatures", ["7/4", "1/4"]),
    ]
)
