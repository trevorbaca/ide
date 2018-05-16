.. _ide--AbjadIDE:

AbjadIDE
========

.. automodule:: ide.AbjadIDE

.. currentmodule:: ide.AbjadIDE

.. container:: svg-container

   .. inheritance-diagram:: ide
      :lineage: ide.AbjadIDE

.. autoclass:: AbjadIDE

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: AbjadIDE.__call__

   .. automethod:: AbjadIDE.__format__

   .. automethod:: AbjadIDE.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: AbjadIDE.activate

   .. automethod:: AbjadIDE.build_part_pdf

   .. automethod:: AbjadIDE.build_score_pdf

   .. automethod:: AbjadIDE.call_shell

   .. automethod:: AbjadIDE.check_definition_py

   .. automethod:: AbjadIDE.collect_segments

   .. automethod:: AbjadIDE.color_clefs

   .. automethod:: AbjadIDE.color_dynamics

   .. automethod:: AbjadIDE.color_instruments

   .. automethod:: AbjadIDE.color_margin_markup

   .. automethod:: AbjadIDE.color_metronome_marks

   .. automethod:: AbjadIDE.color_persistent_indicators

   .. automethod:: AbjadIDE.color_staff_lines

   .. automethod:: AbjadIDE.color_time_signatures

   .. automethod:: AbjadIDE.copy_to_clipboard

   .. automethod:: AbjadIDE.cut_to_clipboard

   .. automethod:: AbjadIDE.deactivate

   .. automethod:: AbjadIDE.doctest_all

   .. automethod:: AbjadIDE.duplicate

   .. automethod:: AbjadIDE.edit_aliases_py

   .. automethod:: AbjadIDE.edit_all

   .. automethod:: AbjadIDE.edit_back_cover_tex

   .. automethod:: AbjadIDE.edit_definition_py

   .. automethod:: AbjadIDE.edit_front_cover_tex

   .. automethod:: AbjadIDE.edit_illustration_ily

   .. automethod:: AbjadIDE.edit_illustration_ly

   .. automethod:: AbjadIDE.edit_latex_log

   .. automethod:: AbjadIDE.edit_layout_ly

   .. automethod:: AbjadIDE.edit_layout_py

   .. automethod:: AbjadIDE.edit_lilypond_log

   .. automethod:: AbjadIDE.edit_music_ly

   .. automethod:: AbjadIDE.edit_part_tex

   .. automethod:: AbjadIDE.edit_preface_tex

   .. automethod:: AbjadIDE.edit_score_tex

   .. automethod:: AbjadIDE.edit_stylesheet_ily

   .. automethod:: AbjadIDE.edit_text

   .. automethod:: AbjadIDE.empty_clipboard

   .. automethod:: AbjadIDE.force_single_column

   .. automethod:: AbjadIDE.generate_back_cover_tex

   .. automethod:: AbjadIDE.generate_front_cover_tex

   .. automethod:: AbjadIDE.generate_layout_py

   .. automethod:: AbjadIDE.generate_music_ly

   .. automethod:: AbjadIDE.generate_part_tex

   .. automethod:: AbjadIDE.generate_preface_tex

   .. automethod:: AbjadIDE.generate_score_tex

   .. automethod:: AbjadIDE.generate_stylesheet_ily

   .. automethod:: AbjadIDE.get

   .. automethod:: AbjadIDE.git_commit

   .. automethod:: AbjadIDE.git_diff

   .. automethod:: AbjadIDE.git_pull

   .. automethod:: AbjadIDE.git_push

   .. automethod:: AbjadIDE.git_status

   .. automethod:: AbjadIDE.go_back

   .. automethod:: AbjadIDE.go_to_builds_directory

   .. automethod:: AbjadIDE.go_to_contents_directory

   .. automethod:: AbjadIDE.go_to_directory

   .. automethod:: AbjadIDE.go_to_distribution_directory

   .. automethod:: AbjadIDE.go_to_etc_directory

   .. automethod:: AbjadIDE.go_to_library

   .. automethod:: AbjadIDE.go_to_materials_directory

   .. automethod:: AbjadIDE.go_to_next_package

   .. automethod:: AbjadIDE.go_to_next_score

   .. automethod:: AbjadIDE.go_to_previous_package

   .. automethod:: AbjadIDE.go_to_previous_score

   .. automethod:: AbjadIDE.go_to_scores_directory

   .. automethod:: AbjadIDE.go_to_segments_directory

   .. automethod:: AbjadIDE.go_to_stylesheets_directory

   .. automethod:: AbjadIDE.go_to_test_directory

   .. automethod:: AbjadIDE.go_to_tools_directory

   .. automethod:: AbjadIDE.go_to_wrapper_directory

   .. automethod:: AbjadIDE.go_up

   .. automethod:: AbjadIDE.hide_clock_time_markup

   .. automethod:: AbjadIDE.hide_figure_name_markup

   .. automethod:: AbjadIDE.hide_local_measure_number_markup

   .. automethod:: AbjadIDE.hide_measure_index_markup

   .. automethod:: AbjadIDE.hide_measure_number_markup

   .. automethod:: AbjadIDE.hide_music_annotations

   .. automethod:: AbjadIDE.hide_spacing_markup

   .. automethod:: AbjadIDE.hide_stage_number_markup

   .. automethod:: AbjadIDE.interpret_back_cover_tex

   .. automethod:: AbjadIDE.interpret_front_cover_tex

   .. automethod:: AbjadIDE.interpret_illustration_ly

   .. automethod:: AbjadIDE.interpret_music_ly

   .. automethod:: AbjadIDE.interpret_part_tex

   .. automethod:: AbjadIDE.interpret_preface_tex

   .. automethod:: AbjadIDE.interpret_score_tex

   .. automethod:: AbjadIDE.is_navigation

   .. automethod:: AbjadIDE.make_illustration_ly

   .. automethod:: AbjadIDE.make_illustration_pdf

   .. automethod:: AbjadIDE.make_layout_ly

   .. automethod:: AbjadIDE.make_segment_midi

   .. automethod:: AbjadIDE.nake_illustration_pdf

   .. automethod:: AbjadIDE.new

   .. automethod:: AbjadIDE.open_all_pdfs

   .. automethod:: AbjadIDE.open_back_cover_pdf

   .. automethod:: AbjadIDE.open_front_cover_pdf

   .. automethod:: AbjadIDE.open_illustration_pdf

   .. automethod:: AbjadIDE.open_music_pdf

   .. automethod:: AbjadIDE.open_part_pdf

   .. automethod:: AbjadIDE.open_preface_pdf

   .. automethod:: AbjadIDE.open_score_pdf

   .. automethod:: AbjadIDE.paste_from_clipboard

   .. automethod:: AbjadIDE.propagate_layout_py

   .. automethod:: AbjadIDE.pytest_all

   .. automethod:: AbjadIDE.quit

   .. automethod:: AbjadIDE.remove

   .. automethod:: AbjadIDE.rename

   .. automethod:: AbjadIDE.replace

   .. automethod:: AbjadIDE.run

   .. automethod:: AbjadIDE.search

   .. automethod:: AbjadIDE.show_clipboard

   .. automethod:: AbjadIDE.show_clock_time_markup

   .. automethod:: AbjadIDE.show_figure_name_markup

   .. automethod:: AbjadIDE.show_help

   .. automethod:: AbjadIDE.show_local_measure_number_markup

   .. automethod:: AbjadIDE.show_measure_index_markup

   .. automethod:: AbjadIDE.show_measure_number_markup

   .. automethod:: AbjadIDE.show_music_annotations

   .. automethod:: AbjadIDE.show_spacing_markup

   .. automethod:: AbjadIDE.show_stage_number_markup

   .. automethod:: AbjadIDE.smart_doctest

   .. automethod:: AbjadIDE.smart_edit

   .. automethod:: AbjadIDE.smart_pdf

   .. automethod:: AbjadIDE.smart_pytest

   .. automethod:: AbjadIDE.test_baca_directories

   .. automethod:: AbjadIDE.trash_back_cover_pdf

   .. automethod:: AbjadIDE.trash_back_cover_tex

   .. automethod:: AbjadIDE.trash_definition_py

   .. automethod:: AbjadIDE.trash_front_cover_pdf

   .. automethod:: AbjadIDE.trash_front_cover_tex

   .. automethod:: AbjadIDE.trash_illustration_ily

   .. automethod:: AbjadIDE.trash_illustration_ly

   .. automethod:: AbjadIDE.trash_illustration_pdf

   .. automethod:: AbjadIDE.trash_layout_ly

   .. automethod:: AbjadIDE.trash_layout_py

   .. automethod:: AbjadIDE.trash_music_ly

   .. automethod:: AbjadIDE.trash_music_pdf

   .. automethod:: AbjadIDE.trash_part_pdf

   .. automethod:: AbjadIDE.trash_part_tex

   .. automethod:: AbjadIDE.trash_preface_pdf

   .. automethod:: AbjadIDE.trash_preface_tex

   .. automethod:: AbjadIDE.trash_score_pdf

   .. automethod:: AbjadIDE.trash_score_tex

   .. automethod:: AbjadIDE.trash_stylesheet_ily

   .. automethod:: AbjadIDE.uncolor_clefs

   .. automethod:: AbjadIDE.uncolor_dynamics

   .. automethod:: AbjadIDE.uncolor_instruments

   .. automethod:: AbjadIDE.uncolor_margin_markup

   .. automethod:: AbjadIDE.uncolor_metronome_marks

   .. automethod:: AbjadIDE.uncolor_persistent_indicators

   .. automethod:: AbjadIDE.uncolor_staff_lines

   .. automethod:: AbjadIDE.uncolor_time_signatures

   .. automethod:: AbjadIDE.xinterpret_music_ly

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: AbjadIDE.change

   .. automethod:: AbjadIDE.cleanup

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: AbjadIDE.aliases

   .. autoattribute:: AbjadIDE.clipboard

   .. autoattribute:: AbjadIDE.commands

   .. autoattribute:: AbjadIDE.current_directory

   .. autoattribute:: AbjadIDE.example

   .. autoattribute:: AbjadIDE.io

   .. autoattribute:: AbjadIDE.navigation

   .. autoattribute:: AbjadIDE.navigations

   .. autoattribute:: AbjadIDE.previous_directory

   .. autoattribute:: AbjadIDE.test