# -*- coding: utf-8 -*-
'''Abjad IDE installation.

To install the Abjad IDE:

    1. clone the Abjad IDE from GitHub
    2. verify the Abjad IDE directories.
    3. add Abjad IDE scr/ directory to your PATH.
    4. create a scores/ directory.
    5. add the scores/ directory to your Abjad configuration file
    6. start and stop the Abjad IDE.
    7. run doctest.
    8. run pytest.
    9. build the Abjad IDE API.

1. Clone the Abjad IDE from GitHub:

    git clone https://github.com/Abjad/ide.git

2. Verify the Abjad IDE directories. The following directories should appear on
your filesystem after checkout:

    ide/
        ide/
        boilerplate/
        docs/
        etc/
        scores/
        scr/
        test/
        tools/
            idetools/

3. Add the Abjad IDE scr/ directory to your PATH. This tells your shell where
the start-abjad-idetools script is housed:

    export PATH=~/Documents/ide/ide/scr:$PATH

4. Create a scores directory. You can do this anywhere on your filesystem.

    mkdir ~/Scores

5. Open your Abjad IDE configuration file:

    vi ~/.abjad/ide/ide.cfg

Then add the path to your scores directory to your Abjad configuration file:

    composer_scores_directory = ~/Scores

6. Start and stop the Abjad IDE. Type start-abjad-idetools at the commandline.
The Abjad IDE should start. What you see here probably won't be very
interesting because you won't yet have any scores created on your system. But
you should see score management menu options. If the shell can't find
start-abjad-idetools then go back and make sure you added the Abjad IDE scr/
directory to your PATH. After the Abjad IDE starts correctly enter 'q' to quit
the Abjad IDE.

7. Run doctest against the ide directory.

8. Run pytest against the die directory.

9. Build the Abjad IDE API:

    ajv api -I

You're ready to use the Abjad IDE when the docs build and all tests pass.
'''

from ide.tools import idetools
configuration = idetools.AbjadIDEConfiguration()
configuration._add_example_score_to_sys_path()
del(configuration)
del(idetools)