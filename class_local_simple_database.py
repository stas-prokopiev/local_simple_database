from __future__ import print_function
import os
import logging


from local_simple_database.working_with_files import \
    check_that_folder_exist_otherwise_create
from local_simple_database.working_with_files import \
    get_list_names_of_folders_in_folder

#####
# local_simple_database.database_handlers
from local_simple_database.database_handlers import \
    class_str_database_handler
from local_simple_database.database_handlers import \
    class_int_database_handler
from local_simple_database.database_handlers import \
    class_float_database_handler
from local_simple_database.database_handlers import \
    class_list_database_handler
#####
LIST_ALL_SUPPORTED_TYPES_OF_DB = ["int", "float", "str", "list"]


class class_local_simple_database():
    """"""

    def __init__(
            self,
            str_path_database_dir="",
            bool_if_to_use_everyday_rolling=False,
    ):
        """"""
        if not str_path_database_dir:
            str_path_database_dir = "local_database"
        self.str_path_main_database_dir = \
            os.path.abspath(str_path_database_dir)
        check_that_folder_exist_otherwise_create(
            self.str_path_main_database_dir
        )
        assert os.path.exists(self.str_path_main_database_dir), (
            "ERROR: Can't init folder: " +
            str(self.str_path_main_database_dir) +
            "for local server"
        )
        #####
        self.bool_if_to_use_everyday_rolling = bool_if_to_use_everyday_rolling
        self.dict_db_handler_by_str_db_name = {}

    def __getitem__(self, str_db_name):
        """"""
        if str_db_name not in self.dict_db_handler_by_str_db_name:
            self.init_new_database(str_db_name)
        return self.dict_db_handler_by_str_db_name[str_db_name].get_value()

    def __setitem__(self, str_db_name, value_to_set):
        """"""
        #####
        if str_db_name not in self.dict_db_handler_by_str_db_name:
            self.init_new_database(str_db_name)
        self.dict_db_handler_by_str_db_name[str_db_name].set_value(
            value_to_set
        )

    def init_new_database(self, str_db_name, str_database_type=""):
        """"""
        assert isinstance(str_db_name, str), (
            "ERROR: DataBase name should have type str, now it is: " +
            str(type(str_db_name))
        )
        #####
        # If type is not given directly try to recognize type by database name
        # If DB name starts with type then type is found
        # Else type will be set to default int
        if not str_database_type:
            str_database_type = "int"
            for str_db_type in LIST_ALL_SUPPORTED_TYPES_OF_DB:
                if str_db_name.startswith(str_db_type):
                    str_database_type = str_db_type
                    break
        assert str_database_type in LIST_ALL_SUPPORTED_TYPES_OF_DB, (
            "ERROR: Wrong type of database: " + str(str_database_type) +
            " Only accessible types are: " +
            str(LIST_ALL_SUPPORTED_TYPES_OF_DB)
        )
        logging.info(
            "Initialize new empty database with name " +
            str_db_name +
            " With type of values: " + str(str_database_type).upper()
        )
        if str_database_type == "str":
            self.dict_db_handler_by_str_db_name[str_db_name] = \
                class_str_database_handler(self, str_db_name)
        elif str_database_type == "int":
            self.dict_db_handler_by_str_db_name[str_db_name] = \
                class_int_database_handler(self, str_db_name)
        elif str_database_type == "float":
            self.dict_db_handler_by_str_db_name[str_db_name] = \
                class_float_database_handler(self, str_db_name)
        elif str_database_type == "list":
            self.dict_db_handler_by_str_db_name[str_db_name] = \
                class_list_database_handler(self, str_db_name)





