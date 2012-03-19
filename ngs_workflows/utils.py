#!/usr/bin/env python

#    This file is part of ngs_workflow.
#
#    ngs_workflow is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ngs_workflow is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with ngs_workflow.  If not, see <http://www.gnu.org/licenses/>.

import os, sys, gzip, ngs_plugins

class NGSplugin:
   '''
   Define a plugin class, genic in a way that it will be possible to create
   a file describe the function purpose, the needed arguments and the output
   so to present an absract way to execute it to the main program.
   '''
   def __init__(self,purpose,input_type,output_type):
      self.purpose      = purpose
      self.input_type   = input_type
      self.output_type  = output_type
      self.plugins_list = get_plugins(ngs_plugins)


def get_plugins(plugins_module):
   '''
   Look into the plugins directory and create a list with all the available
   modules.
   '''
   plugins_list = []
   for dirname, dirnames, filenames in walklevel(check_dir(getattr(plugins_module,'__path__')[0]),level=1):
      for filename in filenames:
         if filename.endswith('.py'):
            if filename.startswith('__'):
               pass
            else:
               plugins_list.append(filename.strip()[:-3])
   return plugins_list



def config_parse(plugin):
   '''
   Parse the config file in the project directory, and find the plugin specific
   configuration. If the config file is not found a new one with sdandard
   parameters will be created
   '''

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
