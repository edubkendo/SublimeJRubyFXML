# All of SublimeFileTemplates is licensed under the MIT licence.
#
# Copyright (c) 2012 Anders Nklestad
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import os, time, re
import sublime
import sublime_plugin
import glob
import os
import shutil
import pprint
from xml.etree import ElementTree


current_path = None

class CreateJrubyfxProjectCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.doCommand()

    def doCommand(self):
        if not self.find_root():
            self.construct_excluded_pattern()
            self.build_dir_paths()
            self.build_file_paths()
            self.select_dir()
        else:
            self.construct_excluded_pattern()
            self.build_dir_paths()
            self.build_file_paths()
            self.move_current_directory_to_top()
            self.select_dir()

    def find_root(self):
        folders = self.window.folders()
        if len(folders) == 0:
            from os.path import expanduser
            self.root = unicode(expanduser("~"))
            self.rel_path_start = len(self.root) + 1
            return False

        self.root = folders[0]
        self.rel_path_start = len(self.root) + 1
        return True

    def construct_excluded_pattern(self):
        patterns = [pat.replace('|', '\\') for pat in self.get_setting('excluded_dir_patterns')]
        self.excluded = re.compile('^(?:' + '|'.join(patterns) + ')$')

    def get_setting(self, key):
        settings = None
        view = self.window.active_view()

        if view:
            settings = self.window.active_view().settings()

        if settings and settings.has('JRubyFXML') and key in settings.get('JRubyFXML'):
            # Get project-specific setting
            results =settings.get('JRubyFXML')[key]
        else:
            # Get user-specific or default setting
            settings = sublime.load_settings('JRubyFXML.sublime-settings')
            results = settings.get(key)
        return results

    def build_dir_paths(self):
        self.dir_paths = []
        self.dir_paths = [["../", "Go up one level in the directory structure"]]
        self.selected_dir = ""
        for base, dirs, files in os.walk(self.root):
            dirs_copy = dirs[:]
            [dirs.remove(dir) for dir in dirs_copy if self.excluded.search(dir)]

            for dir in dirs:
                dir_path = os.path.join(base, dir)[self.rel_path_start:]
                self.dir_paths.append(dir_path)

    def build_file_paths(self):
        self.directory_files = []
        directory = self.root + "/" + self.selected_dir
        for base, dirs, files in os.walk(directory):
            files_copy = files[:]

            # for file in files:
            #    self.directory_files.append(file)

    def move_current_directory_to_top(self):
        view = self.window.active_view()

        if view:
            cur_dir = os.path.dirname(view.file_name())[self.rel_path_start:]
            for path in self.dir_paths:
                if path == cur_dir:
                    i = self.dir_paths.index(path)
                    self.dir_paths.insert(1, self.dir_paths.pop(i))
                    break

    def select_dir(self):
        self.window.show_quick_panel(self.dir_paths, self.dir_selected, sublime.MONOSPACE_FONT)


    def dir_selected(self, selected_index):
        if selected_index != -1:
            if selected_index == 0:
                self.up_one_level()
            else:
                self.selected_dir = self.dir_paths[selected_index]

            self.build_file_paths()

            # Add aditional menu options
            self.directory_files.insert(0, ["Browse Directories", "go back to browsing directories"])
            self.directory_files.insert(1, ["New JRubyFX Project", "new project in the current directory"])

            # Open window to choose desired action
            self.window.show_quick_panel(self.directory_files, self.file_selected, sublime.MONOSPACE_FONT)

    def file_selected(self, selected_index):
        if selected_index != -1:
            if selected_index == 0:
                self.select_dir()
            elif selected_index == 1:
                self.new_dir()

    def up_one_level(self):
        self.root = os.path.abspath(os.path.join(self.root, os.path.pardir))
        self.rel_path_start = len(self.root) + 1

        self.build_dir_paths()
        self.build_file_paths()
        self.move_current_directory_to_top()
        self.select_dir()

    def new_dir(self):
        self.window.show_input_panel("New project name:", '', self.new_dir_action, None, None)

    def new_dir_action(self, dir_name):
        full_path = os.path.join(self.root, self.selected_dir, dir_name)
        if os.path.lexists(full_path):
            sublime.error_message('Directory already exists:\n%s' % full_path)
            return
        else:
            os.mkdir(full_path)
            os.mkdir(full_path + os.sep + "src")
            os.mkdir(full_path + os.sep + "dist")
            os.mkdir(full_path + os.sep + "package")
            os.mkdir(full_path + os.sep + "package" + os.sep + "linux")
            os.mkdir(full_path + os.sep + "package" + os.sep + "macosx")
            os.mkdir(full_path + os.sep + "package" + os.sep + "windows")
            os.mkdir(full_path + os.sep + "build")
            file_name = dir_name + ".sublime-project"
            self.create_project_file(file_name, full_path)
            # self.remove_window_folders()
            project_file_loc = os.path.join(full_path, file_name)
            sublime_command_line(['-a', project_file_loc])

    def create_project_file(self, file_name, full_path):

        string_full_path = str(full_path).replace("\\","\\\\")
        prj_file_contents = ("{\n"
                            "    \"folders\":\n"
                            "    [\n"
                            "        {\n"
                            "            \"path\": \"%s\"\n"
                            "        }\n"
                            "    ]\n"
                            "}\n" % string_full_path)
        self.project_file = os.path.join(full_path, file_name)
        file_ref = open(self.project_file, "w")
        file_ref.write((prj_file_contents));
        file_ref.close()

    def remove_window_folders(self):
        folders_to_remove = self.window.folders()
        self.window.run_command('remove_folder', {"dirs":folders_to_remove})

# hack to add folders to sidebar (stolen from wbond)
def get_sublime_path():
    if sublime.platform() == 'osx':
        return '/Applications/Sublime Text 2.app/Contents/SharedSupport/bin/subl'
    elif sublime.platform() == 'linux':
        return open('/proc/self/cmdline').read().split(chr(0))[0]
    elif sublime.platform() == "windows":
        return 'sublime_text.exe'
    else:
        return sys.executable

def sublime_command_line(args):
    import subprocess
    args.insert(0, get_sublime_path())
    return subprocess.Popen(args)

class CreateFxmlTemplateCommand(sublime_plugin.WindowCommand):
    ROOT_DIR_PREFIX = '[root: '
    ROOT_DIR_SUFFIX = ']'
    INPUT_PANEL_CAPTION = 'File name:'

    def run(self):

        if not self.find_root():
            return

        self.find_templates()
        self.window.show_quick_panel(self.templates, self.template_selected)

    def refresh_folders(self):
        try:
            sublime.set_timeout(lambda:sublime.active_window().run_command('refresh_folder_list'), 200);
            sublime.set_timeout(lambda:sublime.active_window().run_command('refresh_folder_list'), 600);
            sublime.set_timeout(lambda:sublime.active_window().run_command('refresh_folder_list'), 1300);
            sublime.set_timeout(lambda:sublime.active_window().run_command('refresh_folder_list'), 2300);
        except:
            pass

    def create_and_open_file(self, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        open(path, 'w')

        global template
        template = {
            'content': self.replace_variables(self.get_content(path)),
            'filename': os.path.basename(path),
            'path': os.path.dirname(path)
        }
        global current_path

        view = self.window.open_file(path)
        current_path = view.file_name()

        if not view.is_loading():
            populate_file(view)
            self.refresh_folders()

    def get_content(self, path):
        content = ''

        try:
            content = self.template.find("content").text
        except:
            pass

        try:
            path = os.path.abspath(os.path.join(os.path.dirname(self.template_path), self.template.find("file").text))
            content = open(path).read()
            print content
        except:
            pass

        return content


    def find_root(self):
        folders = self.window.folders()
        if len(folders) == 0:
            sublime.error_message('Could not find project root')
            return False

        self.root = folders[0]
        self.rel_path_start = len(self.root) + 1
        return True

    def construct_excluded_pattern(self):
        patterns = [pat.replace('|', '\\') for pat in self.get_setting('excluded_dir_patterns')]
        self.excluded = re.compile('^(?:' + '|'.join(patterns) + ')$')

    def get_setting(self, key):
        settings = None
        view = self.window.active_view()

        if view:
            settings = self.window.active_view().settings()

        if settings and settings.has('FileTemplates') and key in settings.get('FileTemplates'):
            # Get project-specific setting
            results = settings.get('FileTemplates')[key]
        else:
            # Get user-specific or default setting
            settings = sublime.load_settings('JRubyFXML.sublime-settings')
            results = settings.get(key)
        return results

    def find_templates(self):
        self.templates = []
        self.template_paths = []

        for root, dirnames, filenames in os.walk(sublime.packages_path()):
            for filename in filenames:
                if filename.endswith(".fxml-template"):
                    self.template_paths.append(os.path.join(root, filename))
                    self.templates.append(os.path.basename(root) + ": " + os.path.splitext(filename)[0])

    def template_selected(self, selected_index):
        if selected_index != -1:
            self.template_path = self.template_paths[selected_index]
            #print self.template_path
            from elementtree import SimpleXMLTreeBuilder
            ElementTree.XMLTreeBuilder = SimpleXMLTreeBuilder.TreeBuilder
            tree = ElementTree.parse(open(self.template_path))
            self.template = tree

            self.construct_excluded_pattern()
            self.build_relative_paths()
            #self.move_current_directory_to_top()
            self.window.show_quick_panel(self.relative_paths, self.dir_selected)

    def build_relative_paths(self):
        self.relative_paths = []

        try:
            path = self.template.find("path").text
        except:
            path = ""

        if len(path) > 0:
            self.relative_paths = [ "Default: " + self.template.find("path").text ]

        self.relative_paths.append( self.ROOT_DIR_PREFIX + os.path.split(self.root)[-1] + self.ROOT_DIR_SUFFIX )

        for base, dirs, files in os.walk(self.root):
            dirs_copy = dirs[:]
            [dirs.remove(dir) for dir in dirs_copy if self.excluded.search(dir)]

            for dir in dirs:
                relative_path = os.path.join(base, dir)[self.rel_path_start:]
                self.relative_paths.append(relative_path)

    def move_current_directory_to_top(self):
        view = self.window.active_view()

        if view:
            cur_dir = os.path.dirname(view.file_name())[self.rel_path_start:]
            for path in self.relative_paths:
                if path == cur_dir:
                    i = self.relative_paths.index(path)
                    self.relative_paths.insert(0, self.relative_paths.pop(i))
                    break

    def dir_selected(self, selected_index):
        if selected_index != -1:
            self.selected_dir = self.relative_paths[selected_index]

            filename = ''
            if len(self.template.find("filename").text) > 0:
                filename = self.template.find("filename").text

            try:
                self.arguments = list(self.template.find("arguments"))
            except:
                self.arguments = []

            self.variables = {}
            self.next_argument()

    def next_argument(self):
        if len(self.arguments) > 0 :
            self.argument = self.arguments.pop(0)
            caption = self.argument.text
            self.window.show_input_panel(caption, '', self.process_argument, None, None)
        else:
            self.file_name_input()

    def process_argument(self, value):
        self.variables[self.argument.tag] = value
        self.next_argument()

    def replace_variables(self, text):
        for variable in self.variables.keys():
            text = text.replace( "$" + variable, self.variables[variable] )
        return text

    def file_name_input(self):
        file_name = self.template.find("filename").text
        file_name = self.replace_variables(file_name)

        dir = self.selected_dir
        if self.selected_dir.startswith(self.ROOT_DIR_PREFIX):
            dir = ''
        if self.selected_dir.startswith("Default: "):
            dir = self.template.find("path").text

        dir = self.replace_variables(dir)

        full_path = os.path.join(self.root, dir, file_name)
        if os.path.lexists(full_path):
            sublime.error_message('File already exists:\n%s' % full_path)
            return
        else:
            self.create_and_open_file(full_path)

class FileTemplatesListener(sublime_plugin.EventListener):
    def on_load(self, view):
        global current_path
        if view.file_name() == current_path:
            populate_file(view)
            current_path = None

def populate_file(view):
    global template
    view.run_command("insert_snippet", {'contents': template["content"]})
    view.window().run_command("refresh_folder_list")

class BuildAndDeployCommand(sublime_plugin.WindowCommand):

    def run(self, cmd = [], file_regex = "", line_regex = "", working_dir = "",
            encoding = "utf-8", env = {}, quiet = False, kill = False,
            # Catches "path" and "shell"
            **kwargs):

        self.window.run_command("exec", {"cmd": cmd, "working_dir": working_dir})

class WindowShowOverlayCommand(sublime_plugin.WindowCommand):
    """Wrap show_overlay command because I can't call this from a build system.
    """
    def run(self, *args, **kwargs):
        self.window.run_command('show_overlay', kwargs)