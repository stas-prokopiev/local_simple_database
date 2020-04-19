from __future__ import print_function
import os

import logging


STR_LOG_STDOUT_FORMAT = '%(asctime)s  [%(levelname)s]::  %(message)s'


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


def get_library_logger(int_log_level):
    """
    DEBUG=10   INFO=20   WARNING=30   ERROR=40   CRITICAL=50
    """
    LOGGER = logging.getLogger("local_simple_database")
    LOGGER.propagate = False
    if (LOGGER.hasHandlers()):
        LOGGER.handlers.clear()
    LOGGER.setLevel(level=10)
    #####
    # Create formats of LOGs
    stdout_format = logging.Formatter(STR_LOG_STDOUT_FORMAT, "%H:%M:%S")
    #####
    # 1) Stdout Handler
    stdout_handler = logging.StreamHandler()
    if int_log_level:
        stdout_handler.setLevel(level=int_log_level)
    stdout_handler.setFormatter(stdout_format)
    LOGGER.addHandler(stdout_handler)
    return LOGGER



