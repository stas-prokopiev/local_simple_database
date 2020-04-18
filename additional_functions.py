from __future__ import print_function
import os


import logging



def get_list_of_fields_from_string(str_content):
    """"""
    # Delete empty lines
    list_file_splitted_by_lines = [
        str_one_line
        for str_one_line in str_content.splitlines()
        if str_one_line
    ]
    list_of_fields = []
    for str_one_line in list_file_splitted_by_lines:
        list_of_fields += [elem for elem in str_one_line.split(" ") if elem]
    return list_of_fields
