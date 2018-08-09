# -*- coding: utf-8 -*-
import os

from src.util import UtilFile


def next_files(base_path, rule):
    if os.path.isdir(base_path):
        directories = UtilFile.directories_in_path(base_path)
        directories = list(set(directories) - rule.filter_directors())
        files = UtilFile.files_in_path(base_path)
        return [filter_file([os.path.join(base_path, file) for file in files], rule),
                [os.path.join(base_path, directory) for directory in directories]]
    else:
        return [filter_file([base_path], rule),[]]

def filter_file(files, rule):
    if rule.extensions is not None:
        filted_files = []
        for file in files:
            filename = os.path.basename(file)
            filename = filename.split(".")
            if len(filename) >= 2 and filename[-1] in rule.extensions:
                filted_files.append(file)
        return filted_files
    return files