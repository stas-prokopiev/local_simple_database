from __future__ import print_function
import os

from local_data_server.working_with_files import \
    check_that_folder_exist_otherwise_create
from local_data_server.working_with_files import \
    get_list_names_of_folders_in_folder


import logging


class class_local_simple_database():
    """"""

    def __init__(self, str_path_database_dir=""):
        """"""
        if not str_path_database_dir:
            str_path_database_dir = "local_database"


        self.str_path_database_dir = os.path.abspath(str_path_database_dir)


        check_that_folder_exist_otherwise_create(self.str_path_database_dir)
        assert os.path.exists(self.str_path_database_dir), (
            "ERROR: Can't init folder: " + str(str_path_database_dir) +
            "for local server"
        )




        #####
        self.dict_cached_data_by_database_name = {}
        self.str_database_name = ""  # should be set by every child class






class class_database_for_integers(class_local_simple_database):
    """"""

    def __init__(self, str_path_database_dir=""):
        """"""
        pass


    def get_value(self, )


