# Standard library imports
import os
import datetime
from collections import OrderedDict
import logging
import json

# Third party imports

# Local imports
from local_simple_database.class_local_database import class_local_database

LOGGER = logging.getLogger("local_simple_database")

class class_dict_database_handler():
    """
    This class was built to handle all DataBase-s in one folder

    ...

    Attributes
    ----------
    self.str_path_main_database_dir : str
        Path to main folder with DataBase-s
    self.bool_if_to_use_everyday_rolling : bool
        Flag if to use everyday rolling and save DB-s in folders like 20200101
    self.dict_db_handler_by_str_db_name : dict
        {str_db_name_1: handler_to_process_db_data, ...}
    """

    def __init__(
            self,
            local_dict_database_obj,
            str_db_name,
            default_value=None,
    ):
        self.local_dict_database_obj = local_dict_database_obj
        # Check that DB name starts with dict_ otherwise and dict_
        if str_db_name.startswith("dict_"):
            self.str_db_name = str_db_name
        else:
            self.str_db_name = "dict_" + str_db_name
        self.default_value = default_value

    def __repr__(self):
        """"""
        return self.local_dict_database_obj.read_file_content(self.str_db_name)

    def __getitem__(self, key_to_get):
        """self[database_name]   method for getting DB current value

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which value to get
        """
        dict_current_db_value = self.get_value()
        if key_to_get not in dict_current_db_value:
            if self.default_value is not None:
                return self.default_value
        return dict_current_db_value[key_to_get]

    def __setitem__(self, key_to_set, value_to_set):
        """self[key_to_set] = value_to_set   method for setting DB value

        Parameters
        ----------
        key_to_set : obj
            Name of DataBase which value to get
        value_to_set : object
            Value to set for DB
        """
        dict_current_db_value = self.get_value()
        dict_current_db_value[key_to_set] = value_to_set
        self.set_value(dict_current_db_value)

    def get_value(self):
        """"""
        str_db_content = \
            self.local_dict_database_obj.read_file_content(self.str_db_name)
        if not str_db_content:
            return {}
        return json.loads(str_db_content)

    def set_value(self, dict_values_to_set):
        """"""
        self.local_dict_database_obj.save_file_content(
            json.dumps(dict_values_to_set, sort_keys=True, indent=3),
            self.str_db_name
        )

    def change_default_value(self, new_default_value):
        """"""
        self.default_value = new_default_value




