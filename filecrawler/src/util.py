# -*- coding: utf-8 -*-
import os
from datetime import datetime

class UtilFile():
    @staticmethod
    def create_data_files(base_url, queue_filename, crawled_filename, path_filename):
        UtilFile.write_file(queue_filename,base_url)
        UtilFile.write_file(crawled_filename,'')
        UtilFile.write_file(path_filename,'')

    @staticmethod
    def write_file(path, data):
        fd = open(path, 'w+', encoding="utf-8")
        fd.write(data)
        fd.close()
    
    @staticmethod
    def append_to_file(path, data):
        fd = open(path,'a+',encoding="utf-8")
        fd.write(data + '\n')
        fd.close()

    @staticmethod
    def delete_file_contents(path):
        open(path,'w').close()

    @staticmethod
    def delete_file(path):
        os.remove(path)
        
    @staticmethod
    def file_to_set(file_name):
        result = set()
        fd = open(file_name,'rt', encoding="utf-8")
        for line in fd.readlines():
            result.add(line.replace('\n',''))
        fd.close()
        return result

    @staticmethod
    def set_to_file(path, file_name):
        fd = open(file_name,'w', encoding="utf-8")
        for l in sorted(path):
            fd.write(l+'\n')
        fd.close()

    @staticmethod
    def current_path(base_path, subpath):
        return f"{base_path}/{subpath}"

    @staticmethod
    def directories_in_path(path):
        return [name for name in os.listdir(path) \
                if os.path.isdir(os.path.join(path, name))]

    @staticmethod
    def files_in_path(path):
        return [name for name in os.listdir(path) \
                if not os.path.isdir(os.path.join(path, name))]

    @staticmethod
    def files_in_paths(paths):
        files = []
        for path in paths:
            files += UtilFile.files_in_path(path)
        return files
