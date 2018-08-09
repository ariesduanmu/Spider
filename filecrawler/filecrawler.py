# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import re
import argparse

from textwrap import dedent

from src.crawl import crawl_directories
from src.rules import FileRules

def start_crawl(path, file_extensions, number_of_threads):
    rule = FileRules(file_extensions)
    files = crawl_directories(path, rule, number_of_threads)
    return files

def parse_arguments():
    """Arguments parser."""
    parser = argparse.ArgumentParser(usage='%(prog)s [options] <path>',
                                     description='crawl all files in directory',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=dedent('''Examples:
                                                      python filecrawler.py -e "html,php,py" -t 8 <path>'''))
    parser.add_argument('-e', '--extension', type=str, help='Filename extensions you want to crawl')
    parser.add_argument('-t', '--thread', type=int, default=8, help="number of thread")
    parser.add_argument('path', type=str, help='directory path you want to crawl')
    args = parser.parse_args()

    if not args.extension is None and re.match(r"^(\s*[a-z]+\s*)(,\s*[a-z]+\s*)*$", args.extension.lower()) is None:
        print("[!] Extensions are not valid, will searching for all files")
        args.extension = None

    if not args.extension is None:
        args.extension = re.sub(r"\s+", "", args.extension).split(",")

    return args.path, args.extension, args.thread

if __name__ == '__main__':
    path, file_extensions, number_of_threads = parse_arguments()
    print(start_crawl(path, file_extensions, number_of_threads))