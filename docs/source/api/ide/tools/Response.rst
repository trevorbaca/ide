.. _ide--tools--Response:

Response
========

.. automodule:: ide.tools.Response

.. currentmodule:: ide.tools.Response

.. container:: svg-container

   .. inheritance-diagram:: ide
      :lineage: ide.tools.Response

.. autoclass:: Response

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Response.__format__

   .. automethod:: Response.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Response.get_path

   .. automethod:: Response.is_address

   .. automethod:: Response.is_command

   .. automethod:: Response.is_path

   .. automethod:: Response.is_segment_name

   .. automethod:: Response.is_shell

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: Response.pair

   .. autoattribute:: Response.pattern

   .. autoattribute:: Response.payload

   .. autoattribute:: Response.prefix

   .. autoattribute:: Response.string