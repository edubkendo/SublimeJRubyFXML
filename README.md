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

### Create a new JRubyFX project
*This will remove all folders from the current window's project, so open a new window if concerned. Otherwise, continue.*

Press `ctrl-shift-p` to bring up the Command Palette. Select "Create JRubyFX Project." It will open a list of directories either in your current directory, or the user's home directory if the window has no project. Use [Fuzzy Searching](http://docs.sublimetext.info/en/latest/file_management/file_management.html) to select the directory within which you'd like to create the new project. Choose "New JRubyFX Project" and you will be prompted for a name. After naming your project, a new project will be created for you, with an appropriate directory structure already generated. Place all code inside "src". If you need any library code or vendor code, just create a folder for them inside src. Keeping everything in src will make it easy for the other tools to work with.

The `package` directory and folders within is for customizing native installers. See below for more information.

### Using fx-generator
Create a folder with your projects name and cd into it, open sublime text from this directory so that it is your current project. Now create your fxml file, either by hand, or using [SceneBuilder](http://www.oracle.com/technetwork/java/javafx/tools/index.html). Open the completed fxml file in sublime text, and then select Tools/Build System/fx-generator. Now choose Build from the menu, or `ctrl-b`. This should generate a ruby file correctly stubbed out for working with the selected FXML.

For more information on working with JRubyFX and the fx-generator, see [JRubyFX: Getting Started](https://github.com/byteit101/JRubyFXML/blob/master/Getting%20Started.md).


### Generate FXML templates
  Use `ctrl-shift-p` to open up the Command Palette. Select "Create FXML Template". Next, select the root element for the FXML you would like to generate. If you're unsure, use "AnchorPane". Select the directory you'd like the file placed in(within the current project), and when prompted select a name for the fxml file (.fxml will be appended for you). If the FXML file doesn't show up in the sidebar immediately after generation, just refresh the sidebar.

### Build Executable Jar and Native Bundle/Installer
Ensure all your code is in the `src` folder, that your currently editing your "main" ruby script and select Tools/Build System/JRubyFX. Now press `ctrl-b` and JRubyFX's amazing build tools will construct an executable jar in your `dist` folder, and the appropriate native installer and bundle (based on your current OS and currently installed third-party-tools-- [see here for details](http://docs.oracle.com/javafx/2/deployment/self-contained-packaging.htm#A1324980) ) in the `build` folder.

This will probably work best if you generate your project using the plugin, because that sets up the appropriate folder structure and ensures you have a sublime-project file. You can use the `package` folder to customize the generated installer. For more information on using the build tool, or to customize your app's icons, etc. Please see the [JRubyFX README](https://github.com/nahi/jrubyfx/blob/master/README.md) and this article in the JRuby wiki: [Packaging Native Installers with the JavaFX Ant Tasks](https://github.com/jruby/jruby/wiki/Packaging-Native-Installers-with-the-JavaFX-Ant-Tasks), as well as the [Official Oracle Documentation](http://docs.oracle.com/javafx/2/deployment/self-contained-packaging.htm)

## TODO

- Open FXML with SceneBuilder
- Make the JRubyFX Build's more configurable (ie. let the user pick the directory, main script, output dir, etc)
- Do something with the awesome GUI REPL, scratchpad.rb.
- More completions for DSL
- Syntax highlighting and eventually completions for FX-CSS


## Special Notes
- The code for the FXML templates was largely borrowed from @mneuhaus ' [SublimeFileTemplate](https://github.com/mneuhaus/SublimeFileTemplates) plugin. Other plugins which have contributed inspiration to this project are:
[SideBarEnhancements](https://github.com/titoBouzout/SideBarEnhancements), and [Sublime-File-Navigator](https://github.com/belike81/Sublime-File-Navigator)