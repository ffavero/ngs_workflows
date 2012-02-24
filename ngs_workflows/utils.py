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

import os, sys, gzip

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
