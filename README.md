sublime-gherkin-auto-complete
=============================

Provides auto-completion for Given/When/Then/And/But phrases in feature files

Installation
------------
Available in Sublime Text Package Control

Features
--------
Makes Gherkin phrases in cucumber feature files available as auto completions in Sublime Text.

For example:

    Scenario: Auto-complete phrases in feature files
        Given a sublime text editor instance open in a cucumber folder
        When the user presses '<Ctrl>-Space'
        Then the auto-completion will show all phrases for Given/When/Then statements in all feature files
        And the user can type letters from the phrases to quickly find and re-use the phrase

1. Press `<ctrl>-space` to show the auto-complete box.
2. Type pf. The auto complete will show two matching phrases.
3. Press enter (or tab) to insert. 

Table data for a phrase is also inserted.

Limitations
-----------
1. You need to save a feature file to start indexing
2. You need to save a modified file to pick-up updates in that file
3. Changes to feature files made outside of the editor are not detected.