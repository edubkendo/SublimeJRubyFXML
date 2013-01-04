# JRubyFXML

A collection of snippets, completions and utilities for working with [JRubyFX](https://github.com/nahi/jrubyfx)/FXML (a Ruby DSL for working with JavaFX).


## The Problem

FXML didn't have syntax highlighting in Sublime Text. None of the current code completion solutions work properly with the JRubyFX gem (ie. [SublimeCodeIntel](https://github.com/Kronuz/SublimeCodeIntel) )


## Getting Started

Install via [Package Manager](http://wbond.net/sublime_packages/package_control) or simply clone into your packages directory:

    $ cd ~/.config/sublime-text-2/Packages
    $ git clone https://github.com/edubkendo/SublimeJRubyFXML.git


## How to Use
FXML's syntax highlighting should just work. To trigger the snippets and completions, simply begin typing the appropriate JRubyFX methods.

### Using fx-generator
Create a folder with your projects name and cd into it, open sublime text from this directory so that it is your current project. Now create your fxml file, either by hand, or using [SceneBuilder](http://www.oracle.com/technetwork/java/javafx/tools/index.html). Open the completed fxml file in sublime text, and then select Tools/Build System/fx-generator. Now choose Build from the menu, or `ctrl-b`. This should generate a ruby file correctly stubbed out for working with the selected FXML.

For more information on working with JRubyFX and the fx-generator, see [JRubyFX: Getting Started](https://github.com/byteit101/JRubyFXML/blob/master/Getting%20Started.md).

### Generate FXML templates
  Use `ctrl-shift-p` to open up the Command Palette. Select "Create FXML Template". Next, select the root element for the FXML you would like to generate. If you're unsure, use "AnchorPane". Select the directory you'd like the file placed in(within the current project), and when prompted select a name for the fxml file (.fxml will be appended for you).

## TODO

- Commands for running and building project
- More completions for DSL
- Syntax highlighting and eventually completions for FX-CSS
- Generate a new FXML(select root element)

## Special Notes
- The code for the FXML templates came almost unchanged from @mneuhaus ' [SublimeFileTemplate](https://github.com/mneuhaus/SublimeFileTemplates) plugin. I made one minor change to get it working on my system, and cosmetic changes to allow users to target the various FXML root elements without being intermingled with any other .file-template files they might have on their machine.