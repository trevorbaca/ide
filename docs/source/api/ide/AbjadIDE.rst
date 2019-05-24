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

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __repr__
      activate
      aliases
      black_check
      black_reformat
      build_part_pdf
      build_score_pdf
      call_shell
      change
      check_definition_py
      cleanup
      clipboard
      collect_segments
      color_clefs
      color_dynamics
      color_instruments
      color_margin_markup
      color_metronome_marks
      color_persistent_indicators
      color_staff_lines
      color_time_signatures
      commands
      configuration
      copy_to_clipboard
      current_directory
      cut_to_clipboard
      deactivate
      doctest_all
      duplicate
      edit_aliases_py
      edit_all
      edit_back_cover_tex
      edit_definition_py
      edit_front_cover_tex
      edit_illustration_ily
      edit_illustration_ly
      edit_latex_log
      edit_layout_ly
      edit_layout_py
      edit_lilypond_log
      edit_log
      edit_music_ly
      edit_optimization
      edit_part_tex
      edit_preface_tex
      edit_score_tex
      edit_stylesheet_ily
      edit_text
      empty_clipboard
      example
      force_single_column
      generate_back_cover_tex
      generate_front_cover_tex
      generate_layout_py
      generate_music_ly
      generate_part_tex
      generate_preface_tex
      generate_score_tex
      generate_stylesheet_ily
      get
      git_commit
      git_diff
      git_pull
      git_push
      git_status
      go_back
      go_to_builds_directory
      go_to_contents_directory
      go_to_directory
      go_to_distribution_directory
      go_to_etc_directory
      go_to_materials_directory
      go_to_next_package
      go_to_next_score
      go_to_previous_package
      go_to_previous_score
      go_to_scores_directory
      go_to_segments_directory
      go_to_stylesheets_directory
      go_to_test_directory
      go_to_tools_directory
      go_to_wrapper_directory
      go_up
      hide_clock_time
      hide_figure_names
      hide_local_measure_numbers
      hide_measure_numbers
      hide_music_annotations
      hide_spacing
      hide_stage_numbers
      hide_tag
      interpret_back_cover_tex
      interpret_front_cover_tex
      interpret_illustration_ly
      interpret_music_ly
      interpret_part_tex
      interpret_preface_tex
      interpret_score_tex
      io
      is_navigation
      known_paper_sizes
      make_illustration_ly
      make_illustration_pdf
      make_layout_ly
      make_segment_midi
      mypy
      nake_illustration_pdf
      navigation
      navigations
      new
      open_all_pdfs
      open_back_cover_pdf
      open_front_cover_pdf
      open_illustration_pdf
      open_music_pdf
      open_part_pdf
      open_preface_pdf
      open_score_pdf
      paper_size_to_paper_dimensions
      paste_from_clipboard
      previous_directory
      propagate_layout_py
      pytest_all
      quit
      remove
      rename
      replace
      run
      search
      show_clipboard
      show_clock_time
      show_figure_names
      show_help
      show_local_measure_numbers
      show_measure_numbers
      show_music_annotations
      show_spacing
      show_stage_numbers
      show_tag
      smart_doctest
      smart_edit
      smart_pdf
      smart_pytest
      test
      trash_back_cover_pdf
      trash_back_cover_tex
      trash_definition_py
      trash_front_cover_pdf
      trash_front_cover_tex
      trash_illustration_ily
      trash_illustration_ly
      trash_illustration_pdf
      trash_layout_ly
      trash_layout_py
      trash_music_ly
      trash_music_pdf
      trash_part_pdf
      trash_part_tex
      trash_preface_pdf
      trash_preface_tex
      trash_score_pdf
      trash_score_tex
      trash_stylesheet_ily
      uncolor_clefs
      uncolor_dynamics
      uncolor_instruments
      uncolor_margin_markup
      uncolor_metronome_marks
      uncolor_persistent_indicators
      uncolor_staff_lines
      uncolor_time_signatures
      xinterpret_music_ly

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: AbjadIDE.__call__

   .. automethod:: AbjadIDE.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: AbjadIDE.activate

   .. automethod:: AbjadIDE.black_check

   .. automethod:: AbjadIDE.black_reformat

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

   .. automethod:: AbjadIDE.edit_log

   .. automethod:: AbjadIDE.edit_music_ly

   .. automethod:: AbjadIDE.edit_optimization

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

   .. automethod:: AbjadIDE.hide_clock_time

   .. automethod:: AbjadIDE.hide_figure_names

   .. automethod:: AbjadIDE.hide_local_measure_numbers

   .. automethod:: AbjadIDE.hide_measure_numbers

   .. automethod:: AbjadIDE.hide_music_annotations

   .. automethod:: AbjadIDE.hide_spacing

   .. automethod:: AbjadIDE.hide_stage_numbers

   .. automethod:: AbjadIDE.hide_tag

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

   .. automethod:: AbjadIDE.mypy

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

   .. automethod:: AbjadIDE.show_clock_time

   .. automethod:: AbjadIDE.show_figure_names

   .. automethod:: AbjadIDE.show_help

   .. automethod:: AbjadIDE.show_local_measure_numbers

   .. automethod:: AbjadIDE.show_measure_numbers

   .. automethod:: AbjadIDE.show_music_annotations

   .. automethod:: AbjadIDE.show_spacing

   .. automethod:: AbjadIDE.show_stage_numbers

   .. automethod:: AbjadIDE.show_tag

   .. automethod:: AbjadIDE.smart_doctest

   .. automethod:: AbjadIDE.smart_edit

   .. automethod:: AbjadIDE.smart_pdf

   .. automethod:: AbjadIDE.smart_pytest

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