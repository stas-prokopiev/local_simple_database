# Standard library imports
import os
import datetime
from collections import OrderedDict
import logging

# Third party imports

# Local imports
from local_simple_database import LIST_SIMPLE_DB_TYPES
from local_simple_database.class_local_database import class_local_database

LOGGER = logging.getLogger("local_simple_database")

class class_local_simple_database(class_local_database):
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
        super(class_local_simple_database, self).__init__(
            str_path_database_dir=str_path_database_dir,
            bool_if_to_use_everyday_rolling=bool_if_to_use_everyday_rolling,
        )
        self.dict_func_db_getter_by_str_db_name = {}
        self.dict_func_db_setter_by_str_db_name = {}
        self.dict_str_db_type_by_str_db_name = {}
        self.dict_list_db_allowed_types_by_str_db_name = {}

    def __getitem__(self, str_db_name):
        """self[database_name]   method for getting DB current value

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which value to get
        """
        if str_db_name not in self.dict_func_db_getter_by_str_db_name:
            self.init_new_simple_database(str_db_name)
        str_db_content = self.read_file_content(str_db_name)
        func_getter = self.dict_func_db_getter_by_str_db_name[str_db_name]
        return func_getter(str_db_content)

    def __setitem__(self, str_db_name, value_to_set):
        """self[database_name] = x   method for setting DB value

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which value to get
        value_to_set : object
            Value to set for DB
        """
        #####
        if str_db_name not in self.dict_func_db_setter_by_str_db_name:
            self.init_new_simple_database(str_db_name)
        # Check that value to set has suitable type
        list_allowed_type = \
            self.dict_list_db_allowed_types_by_str_db_name[str_db_name]
        assert isinstance(value_to_set, list_allowed_type), (
            "ERROR: Unable to set for DB with type: " +
            str(self.dict_str_db_type_by_str_db_name[str_db_name]) +
            " Value with type: " + str(type(value_to_set))
            )
        # Get setter converter and save value
        func_setter = self.dict_func_db_setter_by_str_db_name[str_db_name]
        str_value_to_save = func_setter(value_to_set)
        self.save_file_content(
            str_value_to_save,
            str_db_name
        )
        LOGGER.debug(
            "For DataBase %s set value: %s", str_db_name, str_value_to_save
        )

    def init_new_simple_database(self, str_db_name):
        """Method for setting/creating a new database and add handler

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which value to get
        str_database_type : str
            Type of values that will be processed by new database
        """
        assert isinstance(str_db_name, str), (
            "ERROR: DataBase name should have type str, now it is: " +
            str(type(str_db_name))
        )
        assert str_db_name, "ERROR: Database name should not be empty"
        #####
        # If DB already initialized then finish execution
        if str_db_name not in self.dict_str_db_type_by_str_db_name:
            return None
        #####
        # Check that name of DataBase is correct
        str_db_type = self.define_type_of_db_by_name(str_db_name)
        if str_db_type not in LIST_SIMPLE_DB_TYPES:
            raise KeyError(
                "Unable to init database with name: " + str_db_name +
                " As database type: " + str_db_type +
                " NOT in the list of allowed types:  " +
                str(LIST_SIMPLE_DB_TYPES)
            )
        #####
        # Init new DataBase
        self.dict_str_db_type_by_str_db_name[str_db_name] = str_db_type
        LOGGER.info(
            "Initialize new database with name " +
            str_db_name +
            " With type of values: " + str(str_db_type).upper()
        )
        #####
        # int
        if str_db_type == "int":
            self.dict_list_db_allowed_types_by_str_db_name[str_db_name] = \
                [int]
            self.dict_func_db_getter_by_str_db_name[str_db_name] = \
                lambda str_file_content: int(str_file_content)
            self.dict_func_db_setter_by_str_db_name[str_db_name] = \
                lambda value_to_set: "%d" % value_to_set
        #####
        # str
        elif str_db_type == "str":
            self.dict_list_db_allowed_types_by_str_db_name[str_db_name] = \
                [str]
            self.dict_func_db_getter_by_str_db_name[str_db_name] = \
                lambda str_file_content: str(str_file_content)
            self.dict_func_db_setter_by_str_db_name[str_db_name] = \
                lambda value_to_set: str(value_to_set)
        #####
        # float
        elif str_db_type == "float":
            self.dict_list_db_allowed_types_by_str_db_name[str_db_name] = \
                [int, float]
            self.dict_func_db_getter_by_str_db_name[str_db_name] = \
                lambda str_file_content: float(str_file_content)
            self.dict_func_db_setter_by_str_db_name[str_db_name] = \
                lambda value_to_set: "%d" % value_to_set

    def get_dict_DBs_data_by_DB_name(self):
        """Getting dict with data of every database in the folder of DB-handler

        Parameters
        ----------
        """
        dict_data_by_str_db_name = {}
        LOGGER.debug("Collect all DB data as dict.")
        list_names_of_DB_files = \
            self.get_list_names_of_all_files_with_DBs_in_dir()
        for str_db_name in list_names_of_DB_files:
            dict_data_by_str_db_name[str_db_name] = self[str_db_name]
        return dict_data_by_str_db_name

    def get_dict_every_DB_by_date(self):
        """
        Getting {date_1: dict_results_of_all_DBs_for_date_1, date_2: ...}

        Parameters
        ----------
        """
        dict_dict_DBs_data_by_DB_name_by_date = OrderedDict()
        list_int_dir_names = self.get_dir_names_of_all_dirs_with_daily_DBs()
        #####
        # Get data from every day
        for int_dir_name in sorted(list_int_dir_names):
            str_dir_path = os.path.join(
                self.str_path_main_database_dir,
                str(int_dir_name)
            )
            db_obj = class_local_simple_database(str_dir_path)
            dict_dict_DBs_data_by_DB_name_by_date[str(int_dir_name)] = \
                db_obj.get_dict_DBs_data_by_DB_name()
        return dict_dict_DBs_data_by_DB_name_by_date

    def get_one_DB_data_daily(
            self,
            str_db_name,
            value_to_use_if_DB_not_found=None
    ):
        """
        Getting {date_1: value_1, date_2: value_2, ...} for one database

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which value to get
        value_to_use_if_DB_not_found : object
            value to set if results for some days not found
        """
        dict_DBs_results_by_date = OrderedDict()
        list_int_dir_names = self.get_dir_names_of_all_dirs_with_daily_DBs()
        #####
        # Get data from every day
        for int_dir_name in sorted(list_int_dir_names):
            str_dir_path = os.path.join(
                self.str_path_main_database_dir,
                str(int_dir_name)
            )
            db_obj = class_local_simple_database(str_dir_path)
            list_DBs_names = \
                db_obj.get_list_names_of_all_files_with_DBs_in_dir()

            if str_db_name in list_DBs_names:
                dict_DBs_results_by_date[str(int_dir_name)] = \
                    db_obj[str_db_name]
            elif value_to_use_if_DB_not_found is not None:
                dict_DBs_results_by_date[str(int_dir_name)] = \
                    value_to_use_if_DB_not_found
        return dict_DBs_results_by_date




