.. _ide--Path:

Path
====

.. automodule:: ide.Path

.. currentmodule:: ide.Path

.. container:: svg-container

   .. inheritance-diagram:: ide
      :lineage: ide.Path

.. autoclass:: Path

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __new__
      address_characters
      configuration
      document_names
      get_eol_measure_numbers
      get_header
      is_external
      is_prototype
      scores
      test_score_names

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Path.__bytes__

   .. container:: inherited

      .. automethod:: Path.__call__

   .. container:: inherited

      .. automethod:: Path.__enter__

   .. container:: inherited

      .. automethod:: Path.__eq__

   .. container:: inherited

      .. automethod:: Path.__exit__

   .. container:: inherited

      .. automethod:: Path.__fspath__

   .. container:: inherited

      .. automethod:: Path.__ge__

   .. container:: inherited

      .. automethod:: Path.__gt__

   .. container:: inherited

      .. automethod:: Path.__hash__

   .. container:: inherited

      .. automethod:: Path.__le__

   .. container:: inherited

      .. automethod:: Path.__lt__

   .. automethod:: Path.__new__

   .. container:: inherited

      .. automethod:: Path.__repr__

   .. container:: inherited

      .. automethod:: Path.__rtruediv__

   .. container:: inherited

      .. automethod:: Path.__str__

   .. container:: inherited

      .. automethod:: Path.__truediv__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Path.absolute

   .. container:: inherited

      .. automethod:: Path.activate

   .. container:: inherited

      .. automethod:: Path.add_buildspace_metadatum

   .. container:: inherited

      .. automethod:: Path.add_metadatum

   .. container:: inherited

      .. automethod:: Path.as_posix

   .. container:: inherited

      .. automethod:: Path.as_uri

   .. container:: inherited

      .. automethod:: Path.chmod

   .. container:: inherited

      .. automethod:: Path.coerce

   .. container:: inherited

      .. automethod:: Path.count

   .. container:: inherited

      .. automethod:: Path.deactivate

   .. container:: inherited

      .. automethod:: Path.exists

   .. container:: inherited

      .. automethod:: Path.expanduser

   .. container:: inherited

      .. automethod:: Path.extern

   .. container:: inherited

      .. automethod:: Path.get_asset_type

   .. automethod:: Path.get_eol_measure_numbers

   .. container:: inherited

      .. automethod:: Path.get_files_ending_with

   .. automethod:: Path.get_header

   .. container:: inherited

      .. automethod:: Path.get_identifier

   .. container:: inherited

      .. automethod:: Path.get_measure_profile_metadata

   .. container:: inherited

      .. automethod:: Path.get_metadata

   .. container:: inherited

      .. automethod:: Path.get_metadatum

   .. container:: inherited

      .. automethod:: Path.get_name_predicate

   .. container:: inherited

      .. automethod:: Path.get_next_package

   .. container:: inherited

      .. automethod:: Path.get_next_score

   .. container:: inherited

      .. automethod:: Path.get_part_identifier

   .. container:: inherited

      .. automethod:: Path.get_preamble_partial_score

   .. container:: inherited

      .. automethod:: Path.get_preamble_time_signatures

   .. container:: inherited

      .. automethod:: Path.get_previous_package

   .. container:: inherited

      .. automethod:: Path.get_previous_score

   .. container:: inherited

      .. automethod:: Path.get_time_signature_metadata

   .. container:: inherited

      .. automethod:: Path.get_title

   .. container:: inherited

      .. automethod:: Path.glob

   .. container:: inherited

      .. automethod:: Path.global_rest_identifiers

   .. container:: inherited

      .. automethod:: Path.global_skip_identifiers

   .. container:: inherited

      .. automethod:: Path.group

   .. container:: inherited

      .. automethod:: Path.instrument_to_staff_identifiers

   .. container:: inherited

      .. automethod:: Path.is__assets

   .. container:: inherited

      .. automethod:: Path.is__segments

   .. container:: inherited

      .. automethod:: Path.is_absolute

   .. container:: inherited

      .. automethod:: Path.is_block_device

   .. container:: inherited

      .. automethod:: Path.is_build

   .. container:: inherited

      .. automethod:: Path.is_builds

   .. container:: inherited

      .. automethod:: Path.is_buildspace

   .. container:: inherited

      .. automethod:: Path.is_char_device

   .. container:: inherited

      .. automethod:: Path.is_contents

   .. container:: inherited

      .. automethod:: Path.is_dir

   .. container:: inherited

      .. automethod:: Path.is_distribution

   .. container:: inherited

      .. automethod:: Path.is_etc

   .. automethod:: Path.is_external

   .. container:: inherited

      .. automethod:: Path.is_fifo

   .. container:: inherited

      .. automethod:: Path.is_file

   .. container:: inherited

      .. automethod:: Path.is_illustrationspace

   .. container:: inherited

      .. automethod:: Path.is_introduction_segment

   .. container:: inherited

      .. automethod:: Path.is_library

   .. container:: inherited

      .. automethod:: Path.is_material

   .. container:: inherited

      .. automethod:: Path.is_material_or_segment

   .. container:: inherited

      .. automethod:: Path.is_materials

   .. container:: inherited

      .. automethod:: Path.is_materials_or_segments

   .. container:: inherited

      .. automethod:: Path.is_part

   .. container:: inherited

      .. automethod:: Path.is_parts

   .. automethod:: Path.is_prototype

   .. container:: inherited

      .. automethod:: Path.is_reserved

   .. container:: inherited

      .. automethod:: Path.is_score_build

   .. container:: inherited

      .. automethod:: Path.is_score_package_path

   .. container:: inherited

      .. automethod:: Path.is_scores

   .. container:: inherited

      .. automethod:: Path.is_segment

   .. container:: inherited

      .. automethod:: Path.is_segments

   .. container:: inherited

      .. automethod:: Path.is_socket

   .. container:: inherited

      .. automethod:: Path.is_stylesheets

   .. container:: inherited

      .. automethod:: Path.is_symlink

   .. container:: inherited

      .. automethod:: Path.is_test

   .. container:: inherited

      .. automethod:: Path.is_tools

   .. container:: inherited

      .. automethod:: Path.is_wrapper

   .. container:: inherited

      .. automethod:: Path.iterdir

   .. container:: inherited

      .. automethod:: Path.joinpath

   .. container:: inherited

      .. automethod:: Path.lchmod

   .. container:: inherited

      .. automethod:: Path.list_paths

   .. container:: inherited

      .. automethod:: Path.list_secondary_paths

   .. container:: inherited

      .. automethod:: Path.lstat

   .. container:: inherited

      .. automethod:: Path.match

   .. container:: inherited

      .. automethod:: Path.mkdir

   .. container:: inherited

      .. automethod:: Path.open

   .. container:: inherited

      .. automethod:: Path.owner

   .. container:: inherited

      .. automethod:: Path.part_to_identifiers

   .. container:: inherited

      .. automethod:: Path.read_bytes

   .. container:: inherited

      .. automethod:: Path.read_text

   .. container:: inherited

      .. automethod:: Path.relative_to

   .. container:: inherited

      .. automethod:: Path.remove

   .. container:: inherited

      .. automethod:: Path.remove_lilypond_warnings

   .. container:: inherited

      .. automethod:: Path.remove_metadatum

   .. container:: inherited

      .. automethod:: Path.rename

   .. container:: inherited

      .. automethod:: Path.replace

   .. container:: inherited

      .. automethod:: Path.resolve

   .. container:: inherited

      .. automethod:: Path.rglob

   .. container:: inherited

      .. automethod:: Path.rmdir

   .. container:: inherited

      .. automethod:: Path.samefile

   .. container:: inherited

      .. automethod:: Path.score_skeleton

   .. container:: inherited

      .. automethod:: Path.segment_number_to_path

   .. container:: inherited

      .. automethod:: Path.stat

   .. container:: inherited

      .. automethod:: Path.symlink_to

   .. container:: inherited

      .. automethod:: Path.to_part

   .. container:: inherited

      .. automethod:: Path.touch

   .. container:: inherited

      .. automethod:: Path.trim

   .. container:: inherited

      .. automethod:: Path.unlink

   .. container:: inherited

      .. automethod:: Path.update_order_dependent_segment_metadata

   .. container:: inherited

      .. automethod:: Path.with_name

   .. container:: inherited

      .. automethod:: Path.with_parent

   .. container:: inherited

      .. automethod:: Path.with_score

   .. container:: inherited

      .. automethod:: Path.with_suffix

   .. container:: inherited

      .. automethod:: Path.write_bytes

   .. container:: inherited

      .. automethod:: Path.write_metadata_py

   .. container:: inherited

      .. automethod:: Path.write_text

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Path.cwd

   .. container:: inherited

      .. automethod:: Path.global_rest_identifier

   .. container:: inherited

      .. automethod:: Path.home

   .. container:: inherited

      .. automethod:: Path.is_segment_name

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: Path.anchor

   .. container:: inherited

      .. autoattribute:: Path.build

   .. container:: inherited

      .. autoattribute:: Path.builds

   .. container:: inherited

      .. autoattribute:: Path.contents

   .. container:: inherited

      .. autoattribute:: Path.distribution

   .. autoattribute:: Path.document_names

   .. container:: inherited

      .. autoattribute:: Path.drive

   .. container:: inherited

      .. autoattribute:: Path.etc

   .. container:: inherited

      .. autoattribute:: Path.materials

   .. container:: inherited

      .. autoattribute:: Path.name

   .. container:: inherited

      .. autoattribute:: Path.parent

   .. container:: inherited

      .. autoattribute:: Path.parents

   .. container:: inherited

      .. autoattribute:: Path.parts

   .. container:: inherited

      .. autoattribute:: Path.root

   .. autoattribute:: Path.scores

   .. container:: inherited

      .. autoattribute:: Path.segments

   .. container:: inherited

      .. autoattribute:: Path.stem

   .. container:: inherited

      .. autoattribute:: Path.stylesheets

   .. container:: inherited

      .. autoattribute:: Path.suffix

   .. container:: inherited

      .. autoattribute:: Path.suffixes

   .. container:: inherited

      .. autoattribute:: Path.test

   .. container:: inherited

      .. autoattribute:: Path.tools

   .. container:: inherited

      .. autoattribute:: Path.wrapper