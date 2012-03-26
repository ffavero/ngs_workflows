#!/usr/bin/env python

#    This file is part of ngs_workflows.
#
#    ngs_workflows is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ngs_workflows is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with ngs_workflows.  If not, see <http://www.gnu.org/licenses/>.

import os, sys, gzip, ngs_plugins

class NGSplugin:
   '''
   Define a plugin class, genic in a way that it will be possible to create
   a file describe the function purpose, the needed arguments and the output
   so to present an absract way to execute it to the main program.
   '''
   def __init__(self,plugin_dict):
      self.name         = plugin_dict['NAME']
      self.description  = plugin_dict['DESCRIPTION']
      self.purpose      = plugin_dict['PURPOSE']
      self.input_type   = plugin_dict['INPUT_TYPE']
      self.output_type  = plugin_dict['OUTPUT_TYPE']
      self.executable   = plugin_dict['EXEC']
      self.help_arg     = plugin_dict['HELP_ARG']


def get_plugins(plugins_module=ngs_plugins):
   '''
   Look into the plugins directory and create a list with all the available
   modules.
   '''
   plugins_list = []
   for dirname, dirnames, filenames in walklevel(check_dir(getattr(plugins_module,'__path__')[0]),level=1):
      for filename in filenames:
         if filename.endswith('.ngsp'):
            if filename.startswith('__'):
               pass
            else:
               plugins_list.append(filename.strip())
   return plugins_list



def plugin_parse(plugin,plugins_module=ngs_plugins):
   '''
   Parse the plugin file in the plugin directory, and create the plugin object
   '''
   '''
   FIXME!! the plugin file don't consider the case of multiple
   line argument... and oly conside double quote...
   to lazy to think about it now...
   '''
   plugin_path = check_dir(getattr(plugins_module,'__path__')[0])
   plugin_file = os.path.join(plugin_path,plugin)
   plugin_dict = {'NAME':'','DESCRIPTION':'',
                  'INPUT_TYPE':'','OUTPUT_TYPE':'',
                  'PURPOSE':'','EXEC':'','HELP_ARG':''}
   if os.path.isfile(plugin_file):
      with open(plugin_file,'rb') as ngsp:
         for line in ngsp:
            bottle = ""
            if line.startswith('#'):
               pass
            else:
               quote_open = False
               for letter in line:
                  bottle += letter
                  if quote_open:
                     if letter =='"':
                        break
                  if letter == '"':
                     quote_open = True
            if bottle.strip() != "":
               conf_id, conf_val = bottle.split('=')
               if conf_id in plugin_dict:
                  plugin_dict[conf_id] = conf_val.strip('"')
   return NGSplugin(plugin_dict)


def config_new(directory):
   '''
   Function dedicated to create a new config file in the project directory
   '''

def check_dir(directory):
   '''
   Check the given directory and return the whole path
   or set the default to working directory.
   '''
   if directory == None:
      directory = os.getcwd()
   if os.path.isdir(directory):
      directory = os.path.abspath(directory)
   else:
      sys.exit("Not existing directory, please create the directory first")
   return directory

def walklevel(directory, level=1):
    directory = directory.rstrip(os.path.sep)
    assert os.path.isdir(directory)
    num_sep = directory.count(os.path.sep)
    for root, dirs, files in os.walk(directory):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]
