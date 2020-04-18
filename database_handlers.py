from __future__ import print_function
import os

import datetime
import logging
import numbers
from filelock import FileLock
#####
# .working_with_files
from local_simple_database.working_with_files import \
    check_that_folder_exist_otherwise_create
from local_simple_database.working_with_files import read_whole_file
from local_simple_database.working_with_files import save_whole_file
from local_simple_database.working_with_files import \
    save_list_of_fields_in_file
#####
# .additional_functions
from local_simple_database.additional_functions import \
    get_list_of_fields_from_string
#####


class class_database_handler_general():
    """"""

    def __init__(
            self,
            obj_parent_database,
            str_database_name,
    ):
        """"""
        self.obj_parent_database = obj_parent_database
        self.str_database_name = str_database_name
        self.bool_if_to_use_everyday_rolling = \
            self.obj_parent_database.bool_if_to_use_everyday_rolling

        self.str_file_path_with_db_file = ""
        if not hasattr(self, 'str_database_type'):
            self.str_database_type = ""


    def get_folder_for_databases(self):
        """"""
        if not self.bool_if_to_use_everyday_rolling:
            return self.obj_parent_database.str_path_main_database_dir

        STR_FOLDER_NAME_TEMPLATE = "%Y_%m_%d"
        str_date_for_current_delay = \
            datetime.datetime.today().strftime(STR_FOLDER_NAME_TEMPLATE)
        str_db_folder = os.path.join(
            self.obj_parent_database.str_path_main_database_dir,
            str_date_for_current_delay
        )
        check_that_folder_exist_otherwise_create(
            str_db_folder
        )
        return str_db_folder

    def get_file_path_with_db_file(self):
        """"""
        if (
            not self.str_file_path_with_db_file or
            self.bool_if_to_use_everyday_rolling
        ):
            str_db_folder = self.get_folder_for_databases()
            #####
            # Define file name with db
            if self.str_database_name.startswith(self.str_database_type + "_"):
                str_name_for_file = self.str_database_name + ".txt"
            else:
                str_name_for_file = (
                    self.str_database_type + "_" +
                    self.str_database_name + ".txt"
                )
            #####
            self.str_file_path_with_db_file = os.path.join(
                str_db_folder,
                str_name_for_file
            )
        return self.str_file_path_with_db_file

    def read_file_content(self):
        """"""
        str_db_file = self.get_file_path_with_db_file()
        if not os.path.exists(str_db_file):
            return ""
        with FileLock(str_db_file + ".lock", timeout=30):
            return read_whole_file(str_db_file)

    def save_file_content(self, str_content):
        """"""
        str_db_file = self.get_file_path_with_db_file()
        with FileLock(str_db_file + ".lock", timeout=30):
            save_whole_file(str_db_file, str_content, str_write_mode='w')


class class_str_database_handler(class_database_handler_general):
    """"""

    def __init__(
            self,
            obj_parent_database,
            str_database_name,
    ):
        """"""
        # Init parent class
        super(class_str_database_handler, self).__init__(
            obj_parent_database,
            str_database_name,
        )
        self.str_database_type = "str"

    def get_value(self):
        """"""
        return self.read_file_content()

    def set_value(self, str_value_to_set):
        """"""
        assert isinstance(str_value_to_set, str), (
            "ERROR: You are trying to set value for STR database with " +
            "INCORRECT type: " + str(type(str_value_to_set))
        )
        self.save_file_content(str(str_value_to_set))


class class_int_database_handler(class_database_handler_general):
    """"""

    def __init__(
            self,
            obj_parent_database,
            str_database_name,
    ):
        """"""
        # Init parent class
        super(class_int_database_handler, self).__init__(
            obj_parent_database,
            str_database_name,
        )
        self.str_database_type = "int"

    def get_value(self):
        """"""
        str_file_content = self.read_file_content()
        if not str_file_content:
            return 0
        try:
            return int(str_file_content)
        except ValueError:
            logging.error(
                "For database: " + str(self.str_database_name) +
                " Unable to read INT value from database."
            )
            logging.debug(
                "Current content of database file: " + str_file_content
            )
            raise

    def set_value(self, int_value_to_set):
        """"""
        assert isinstance(int_value_to_set, int), (
            "ERROR: You are trying to set value for INT database with " +
            "INCORRECT type: " + str(type(int_value_to_set))
        )
        str_content = "%d" % int_value_to_set
        self.save_file_content(str_content)
        logging.debug(
            "For database: " + str(self.str_database_name) +
            " Saved value: " + str_content
        )


class class_float_database_handler(class_database_handler_general):
    """"""

    def __init__(
            self,
            obj_parent_database,
            str_database_name,
    ):
        """"""
        # Init parent class
        super(class_float_database_handler, self).__init__(
            obj_parent_database,
            str_database_name,
        )
        self.str_database_type = "float"

    def get_value(self):
        """"""
        str_file_content = self.read_file_content()
        if not str_file_content:
            return 0.0
        try:
            return float(str_file_content)
        except ValueError:
            logging.error(
                "For database: " + str(self.str_database_name) +
                " Unable to read FLOAT value from database."
            )
            logging.debug(
                "Current content of database file: " + str_file_content
            )
            raise

    def set_value(self, float_value_to_set):
        """"""
        assert isinstance(float_value_to_set, float), (
            "ERROR: You are trying to set value for FLOAT database with " +
            "INCORRECT type: " + str(type(int_value_to_set))
        )
        str_content = str(float_value_to_set)
        self.save_file_content(str_content)
        logging.debug(
            "For database: " + str(self.str_database_name) +
            " Saved value: " + str_content
        )


class class_list_database_handler(class_database_handler_general):
    """"""

    def __init__(
            self,
            obj_parent_database,
            str_database_name,
    ):
        """"""
        # Init parent class
        super(class_list_database_handler, self).__init__(
            obj_parent_database,
            str_database_name,
        )
        self.str_database_type = "list"

    def get_value(self):
        """"""
        str_file_content = self.read_file_content()
        if not str_file_content:
            return []
        try:
            list_str_fields = get_list_of_fields_from_string(str_file_content)
            return list_str_fields
        except ValueError:
            logging.error(
                "For database: " + str(self.str_database_name) +
                " Unable to read LIST of values from database."
            )
            logging.debug(
                "Current content of database file: " + str_file_content
            )
            raise

    def set_value(self, list_values_to_set):
        """"""
        assert isinstance(list_values_to_set, list), (
            "ERROR: You are trying to set value for LIST database with " +
            "INCORRECT type: " + str(type(list_values_to_set))
        )

        list_str_values_to_set = list(map(str, list_values_to_set))
        str_content = "\n".join(list_str_values_to_set)
        self.save_file_content(str_content)
        logging.debug(
            "For database: " + str(self.str_database_name) +
            " Saved value: " + str_content
        )



