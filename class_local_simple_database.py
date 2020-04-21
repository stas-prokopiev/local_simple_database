import os
import datetime
from collections import OrderedDict
#####
from local_simple_database import working_with_files
from local_simple_database import database_handlers
#####
STR_FOLDER_NAME_TEMPLATE = "%Y%m%d"
import logging
LOGGER = logging.getLogger("local_simple_database")
LIST_ALL_SUPPORTED_TYPES_OF_DB = ["int", "float", "str", "list"]


class class_local_simple_database():
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
        if not str_path_database_dir:
            str_path_database_dir = "local_database"
        self.str_path_main_database_dir = \
            os.path.abspath(str_path_database_dir)
        working_with_files.check_that_folder_exist_otherwise_create(
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
        """self[database_name]   method for getting DB current value

        Parameters
        ----------
        str_db_name : str
            Name of DataBase which value to get
        """
        if str_db_name not in self.dict_db_handler_by_str_db_name:
            self.init_new_database(str_db_name)
        return self.dict_db_handler_by_str_db_name[str_db_name].get_value()

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
        if str_db_name not in self.dict_db_handler_by_str_db_name:
            self.init_new_database(str_db_name)
        self.dict_db_handler_by_str_db_name[str_db_name].set_value(
            value_to_set
        )

    def init_new_database(self, str_db_name, str_database_type=""):
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
        LOGGER.info(
            "Initialize new empty database with name " +
            str_db_name +
            " With type of values: " + str(str_database_type).upper()
        )
        if str_database_type == "str":
            self.dict_db_handler_by_str_db_name[str_db_name] = \
                database_handlers.class_str_database_handler(self, str_db_name)
        elif str_database_type == "int":
            self.dict_db_handler_by_str_db_name[str_db_name] = \
                database_handlers.class_int_database_handler(self, str_db_name)
        elif str_database_type == "float":
            self.dict_db_handler_by_str_db_name[str_db_name] = \
                database_handlers.class_float_database_handler(
                    self,
                    str_db_name
                )
        elif str_database_type == "list":
            self.dict_db_handler_by_str_db_name[str_db_name] = \
                database_handlers.class_list_database_handler(
                    self,
                    str_db_name
                )

    def get_folder_for_databases(self):
        """Getting folder where should be file with database

        Parameters
        ----------
        """
        if not self.bool_if_to_use_everyday_rolling:
            return self.str_path_main_database_dir

        str_date_for_current_delay = \
            datetime.datetime.today().strftime(STR_FOLDER_NAME_TEMPLATE)
        str_db_folder = os.path.join(
            self.str_path_main_database_dir,
            str_date_for_current_delay
        )
        working_with_files.check_that_folder_exist_otherwise_create(
            str_db_folder
        )
        return str_db_folder

    def get_list_names_of_all_files_with_DBs_in_dir(self):
        """Getting all names of databases in DB-handler folder

        Parameters
        ----------
        """
        list_names_of_DB_files = []
        str_db_folder = self.get_folder_for_databases()
        list_str_filenames = \
            working_with_files.get_names_of_files_in_the_folder(
                str_db_folder,
                str_extension=".txt"
            )
        list_str_filenames = [
            str_filename.replace(".txt", "")
            for str_filename in list_str_filenames
        ]
        LOGGER.debug(
            "Found files that can be considered as DB file: %d"
            % len(list_str_filenames)
        )
        # For every file with DB get data from file
        for str_filename in list_str_filenames:
            LOGGER.debug("Get data from: " + str_filename)
            for str_type in LIST_ALL_SUPPORTED_TYPES_OF_DB:
                if str_filename.startswith(str_type):
                    LOGGER.debug(
                        "For file with name: " + str_filename +
                        " Found type: " + str_type
                    )
                    list_names_of_DB_files.append(str_filename)
                    break
            else:
                LOGGER.warning(
                    "Strange file in DataBase folder with name: " +
                    str_filename +
                    " Unable to get data for it."
                )
        return list_names_of_DB_files

    def get_dir_names_of_all_dirs_with_daily_DBs(self):
        """Getting names of dir-s with daily results of DB-handler

        Parameters
        ----------
        """
        # Get sorted list of names with dirs with DB data
        list_dir_names_with_daily_data = \
            working_with_files.get_list_names_of_folders_in_folder(
                self.str_path_main_database_dir
            )
        list_int_dir_names = []
        for str_dir_name in list_dir_names_with_daily_data:
            try:
                list_int_dir_names.append(int(str_dir_name))
            except ValueError:
                LOGGER.warning(
                    "Unable to define date for folder: " + str_dir_name
                )
        return list_int_dir_names

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




