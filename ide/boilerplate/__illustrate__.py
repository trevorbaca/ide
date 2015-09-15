# -*- coding: utf-8 -*-
from abjad import *
from {score_package_name}.materials.{material_package_name}.definition import {material_package_name}


score = Score({material_package_name})
illustration = lilypondfiletools.make_basic_lilypond_file(score)