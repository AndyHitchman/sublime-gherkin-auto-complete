sublime-gherkin-auto-complete
=============================

Provides auto-completion for Given/When/Then/And/But phrases in feature files

Installation
------------
### ST3

#### Mac OSX

    cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/
    git clone git@github.com:AndyHitchman/sublime-gherkin-auto-complete.git GherkinAutoComplete

### ST2
#### Mac OSX

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages
    git clone git@github.com:AndyHitchman/sublime-gherkin-auto-complete.git GherkinAutoComplete

#### Linux

    cd ~/.config/sublime-text-2/Packages
    git clone git@github.com:AndyHitchman/sublime-gherkin-auto-complete.git GherkinAutoComplete

#### Windows

    cd Users/<user>/AppData/Roaming/Sublime\ Text\ 2/Packages/
    git clone git@github.com:AndyHitchman/sublime-gherkin-auto-complete.git GherkinAutoComplete

Restart Sublime Text 

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
2. Type a few characters from words that matches a phrase above. The auto complete will show matching phrases.
3. Press enter (or tab) to insert. 

Table data for a phrase is also inserted.

Limitations
-----------
2. You need to save a modified file to pick-up updates in that file
3. Changes to feature files made outside of the editor are not detected.
