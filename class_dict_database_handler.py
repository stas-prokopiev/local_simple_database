# Standard library imports
import os
import datetime
from collections import OrderedDict
import logging

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
    ):
        pass