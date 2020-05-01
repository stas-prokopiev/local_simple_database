# Standard library imports
import os
import datetime
from collections import OrderedDict
import logging

# Third party imports

# Local imports
from local_simple_database.class_local_database import class_local_database
from local_simple_database.class_dict_database_handler import \
    class_dict_database_handler

LOGGER = logging.getLogger("local_simple_database")


class class_local_dict_database(class_local_database):
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
            str_path_database_dir="",
            bool_if_to_use_everyday_rolling=False,
    ):
        """Init DB-s object

        Parameters
        ----------
        str_path_database_dir : str, optional
            Path to main folder with DataBase-s (default is ".")
        bool_if_to_use_everyday_rolling : list, optional
            Flag if to use everyday rolling (default is False)
        """
        # Init class of all local DataBases
        super(class_local_dict_database, self).__init__(
            str_path_database_dir=str_path_database_dir,
            bool_if_to_use_everyday_rolling=bool_if_to_use_everyday_rolling,
        )
        self.dict_db_handler_by_str_db_name = {}

    def __getitem__(self, str_db_name):
        """self[database_name]   method for getting DB current value

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which value to get
        """
        if str_db_name not in self.dict_db_handler_by_str_db_name:
            self.dict_db_handler_by_str_db_name[str_db_name] = \
                class_dict_database_handler(self, str_db_name)
        return self.dict_db_handler_by_str_db_name[str_db_name]

    def __setitem__(self, str_db_name, dict_values_to_set):
        """self[database_name] = {key_1: value_1, ...} for setting DB value

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which value to get
        dict_values_to_set : dict
            Value to set for DB
        """
        assert isinstance(dict_values_to_set, dict), (
            "ERROR: Unable to set for dict DB" +
            " Value with type: " + str(type(dict_values_to_set))
        )
        # Set value for database
        if str_db_name not in self.dict_db_handler_by_str_db_name:
            self.dict_db_handler_by_str_db_name[str_db_name] = \
                class_dict_database_handler(self, str_db_name)
        self.dict_db_handler_by_str_db_name[str_db_name].set_value(
            dict_values_to_set
        )
        LOGGER.debug(
            "For DataBase %s set values: %d",
            str_db_name,
            len(dict_values_to_set)
        )



