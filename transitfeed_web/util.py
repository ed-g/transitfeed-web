import os
from os.path import exists, join, abspath
from os import pathsep
from string import split

def search_file(filename, search_path):
   """Given a search path, find file
   https://code.activestate.com/recipes/52224-find-a-file-given-a-search-path/
   """
   file_found = 0
   paths = split(search_path, pathsep)
   for path in paths:
      if exists(join(path, filename)):
          file_found = 1
          break
   if file_found:
      return abspath(join(path, filename))
   else:
      return None

def search_path(filename):
    return search_file(filename, os.environ['PATH'])


