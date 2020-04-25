import os

import datetime
import numbers
from filelock import FileLock
#####
from local_simple_database import working_with_files
#####
import logging
LOGGER = logging.getLogger("local_simple_database")


class class_database_handler_general():
    """This class was built to handle one(any) DataBase

    ...

    Attributes
    ----------
    self.obj_parent_database : object
        Handler of all DataBases in the folder
    self.str_database_name : str
        Name of current DataBase
    self.str_file_path_with_db_file : str
        Path to file with database (If rolling is on, then will be updated)
    self.str_database_type : str
        Type of DataBase, which values it contains
    """
    def __init__(
            self,
            obj_parent_database,
            str_database_name,
    ):
        """Constructor. Initialization of common variables for every DataBase

        Parameters
        ----------
        self.obj_parent_database : object
            Handler of all DataBases in the folder
        self.str_database_name : str
            Name of current DataBase
        """
        self.obj_parent_database = obj_parent_database
        self.str_database_name = str_database_name
        self.str_file_path_with_db_file = ""
        self.str_database_type = ""

    def get_file_path_with_db_file(self):
        """Get path to file with DataBase

        Parameters
        ----------
        """
        if (
            not self.str_file_path_with_db_file or
            self.obj_parent_database.bool_if_to_use_everyday_rolling
        ):
            str_db_folder = self.obj_parent_database.get_folder_for_databases()
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
        """Read whole content of file with DataBase

        Parameters
        ----------
        """
        str_db_file = self.get_file_path_with_db_file()
        if not os.path.exists(str_db_file):
            return ""
        with FileLock(str_db_file + ".lock", timeout=30):
            return working_with_files.read_whole_file(str_db_file)

    def save_file_content(self, str_content):
        """Save content to file with DataBase

        Parameters
        ----------
        """
        str_db_file = self.get_file_path_with_db_file()
        with FileLock(str_db_file + ".lock", timeout=30):
            working_with_files.save_whole_file(
                str_db_file,
                str_content,
                str_write_mode='w'
            )


class class_str_database_handler(class_database_handler_general):
    """This class was built to handle DataBase with strings"""
    def __init__(
            self,
            obj_parent_database,
            str_database_name,
    ):
        """Constructor. Initialization of common variables for every DataBase

        Parameters
        ----------
        self.obj_parent_database : object
            Handler of all DataBases in the folder
        self.str_database_name : str
            Name of current DataBase
        """
        # Init parent class
        super(class_str_database_handler, self).__init__(
            obj_parent_database,
            str_database_name,
        )
        self.str_database_type = "str"

    def get_value(self):
        """Get current value in DataBase

        Parameters
        ----------
        """
        return self.read_file_content()

    def set_value(self, str_value_to_set):
        """"""
        assert isinstance(str_value_to_set, str), (
            "ERROR: You are trying to set value for STR database with " +
            "INCORRECT type: " + str(type(str_value_to_set))
        )
        self.save_file_content(str(str_value_to_set))


class class_int_database_handler(class_database_handler_general):
    """This class was built to handle DataBase with Integers"""

    def __init__(
            self,
            obj_parent_database,
            str_database_name,
    ):
        """Constructor. Initialization of common variables for every DataBase

        Parameters
        ----------
        self.obj_parent_database : object
            Handler of all DataBases in the folder
        self.str_database_name : str
            Name of current DataBase
        """
        # Init parent class
        super(class_int_database_handler, self).__init__(
            obj_parent_database,
            str_database_name,
        )
        self.str_database_type = "int"

    def get_value(self):
        """Get current value in DataBase

        Parameters
        ----------
        """
        str_file_content = self.read_file_content()
        if not str_file_content:
            return 0
        try:
            return int(str_file_content)
        except ValueError:
            LOGGER.error(
                "For database: " + str(self.str_database_name) +
                " Unable to read INT value from database."
            )
            LOGGER.debug(
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
        LOGGER.debug(
            "For database: " + str(self.str_database_name) +
            " Saved value: " + str_content
        )


class class_float_database_handler(class_database_handler_general):
    """This class was built to handle DataBase with Floats"""

    def __init__(
            self,
            obj_parent_database,
            str_database_name,
    ):
        """Constructor. Initialization of common variables for every DataBase

        Parameters
        ----------
        self.obj_parent_database : object
            Handler of all DataBases in the folder
        self.str_database_name : str
            Name of current DataBase
        """
        # Init parent class
        super(class_float_database_handler, self).__init__(
            obj_parent_database,
            str_database_name,
        )
        self.str_database_type = "float"

    def get_value(self):
        """Get current value in DataBase

        Parameters
        ----------
        """
        str_file_content = self.read_file_content()
        if not str_file_content:
            return 0.0
        try:
            return float(str_file_content)
        except ValueError:
            LOGGER.error(
                "For database: " + str(self.str_database_name) +
                " Unable to read FLOAT value from database."
            )
            LOGGER.debug(
                "Current content of database file: " + str_file_content
            )
            raise

    def set_value(self, float_value_to_set):
        """"""
        assert isinstance(float_value_to_set, float), (
            "ERROR: You are trying to set value for FLOAT database with " +
            "INCORRECT type: " + str(type(float_value_to_set))
        )
        str_content = str(float_value_to_set)
        self.save_file_content(str_content)
        LOGGER.debug(
            "For database: " + str(self.str_database_name) +
            " Saved value: " + str_content
        )


class class_list_database_handler(class_database_handler_general):
    """This class was built to handle DataBase with List of values"""

    def __init__(
            self,
            obj_parent_database,
            str_database_name,
    ):
        """Constructor. Initialization of common variables for every DataBase

        Parameters
        ----------
        self.obj_parent_database : object
            Handler of all DataBases in the folder
        self.str_database_name : str
            Name of current DataBase
        """
        # Init parent class
        super(class_list_database_handler, self).__init__(
            obj_parent_database,
            str_database_name,
        )
        self.str_database_type = "list"

    def get_value(self):
        """Get current value in DataBase

        Parameters
        ----------
        """
        str_file_content = self.read_file_content()
        if not str_file_content:
            return []
        try:
            # Delete empty lines
            list_file_splitted_by_lines = [
                str_one_line
                for str_one_line in str_file_content.splitlines()
                if str_one_line
            ]
            list_str_fields = []
            for str_one_line in list_file_splitted_by_lines:
                list_str_fields += [
                    elem for elem in str_one_line.split(" ") if elem
                ]
            return list_str_fields
        except ValueError:
            LOGGER.error(
                "For database: " + str(self.str_database_name) +
                " Unable to read LIST of values from database."
            )
            LOGGER.debug(
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
        LOGGER.debug(
            "For database: " + str(self.str_database_name) +
            " Saved value: " + str_content
        )



