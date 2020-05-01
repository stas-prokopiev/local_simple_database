# Standard library imports
import os
import datetime
from collections import OrderedDict
import logging

# Third party imports
from filelock import FileLock

# Local imports
from local_simple_database.constants import LIST_ALL_SUPPORTED_TYPES_OF_DB

LOGGER = logging.getLogger("local_simple_database")



class class_local_database():
    """
    This class was built to handle all DataBase-s in one folder

    ...

    Attributes
    ----------
    self.str_path_main_database_dir : str
        Path to main folder with DataBase-s
    """

    def __init__(
            self,
            str_path_database_dir="",

            str_datetime_template_rolling=None,


    ):
        """Init DB-s object

        Parameters
        ----------
        str_path_database_dir : str, optional
            Path to main folder with DataBase-s (default is ".")
        """
        if not str_path_database_dir:
            str_path_database_dir = "local_database"
        self.str_path_main_database_dir = \
            os.path.abspath(str_path_database_dir)
        # If dir with database doesn't exists, then create it
        if (not os.path.isdir(self.str_path_main_database_dir)):
            os.makedirs(self.str_path_main_database_dir)
        #####
        self.str_datetime_template_rolling = str_datetime_template_rolling

    def read_file_content(self, str_db_name):
        """Read whole content of file with DataBase

        Parameters
        ----------
        """
        str_db_file = self.get_file_path_with_db_file(str_db_name)
        if not os.path.exists(str_db_file):
            return ""
        with FileLock(str_db_file + ".lock", timeout=30):
            with open(str_db_file, 'r', encoding="utf8", errors='ignore') as f:
                str_whole_file = f.read()
            return str_whole_file

    def save_file_content(self, str_content, str_db_name):
        """Save content to file with DataBase

        Parameters
        ----------
        """
        str_db_file = self.get_file_path_with_db_file(str_db_name)
        with FileLock(str_db_file + ".lock", timeout=30):
            with open(str_db_file, "w", encoding="utf8", errors='ignore') as f:
                f.write(str_content)

    def get_folder_for_databases(self):
        """Getting folder where should be file with database

        Parameters
        ----------
        """
        if not self.str_datetime_template_rolling:
            return self.str_path_main_database_dir
        str_folder_name = datetime.datetime.today().strftime(
            self.str_datetime_template_rolling
        )
        str_db_folder = os.path.join(
            self.str_path_main_database_dir,
            str_folder_name
        )
        if (not os.path.isdir(str_db_folder)):
            os.makedirs(str_db_folder)
        return str_db_folder

    def define_type_of_db_by_name(self, str_db_name):
        """"""
        str_db_type = str_db_name.split("_")[0]
        return str_db_type

    def get_file_path_with_db_file(self, str_db_name):
        """Get path to file with DataBase

        Parameters
        ----------
        """
        str_db_folder = self.get_folder_for_databases()
        str_db_type = self.define_type_of_db_by_name(str_db_name)
        #####
        # Define file name with db
        if str_db_name.startswith(str_db_type + "_"):
            str_name_for_file = str_db_name + ".txt"
        else:
            str_name_for_file = (
                str_db_type + "_" +
                str_db_name + ".txt"
            )
        #####
        str_file_path_with_db_file = os.path.join(
            str_db_folder,
            str_name_for_file
        )
        return str_file_path_with_db_file

    def get_names_of_files_in_DBs_dir(self):
        """"""
        str_db_folder = self.get_folder_for_databases()
        if not os.path.exists(str_db_folder):
            LOGGER.warning(
                "Folder to get filenames doesn't exist: %s",
                str_db_folder
            )
            return []
        list_all_filenames = []
        for str_filename in os.listdir(str_db_folder):
            str_full_path = os.path.join(str_db_folder, str_filename)
            if not os.path.isfile(str_full_path):
                continue
            if not str_filename.endswith(".txt"):
                continue
            list_all_filenames.append(str_filename.replace(".txt", ""))
        LOGGER.debug(
            "Found files that can be considered as DB file: %d",
            len(list_all_filenames)
        )
        return list_all_filenames

    def get_list_names_of_all_files_with_DBs_in_dir(self):
        """Getting all names of databases in DB-handler folder

        Parameters
        ----------
        """
        list_names_of_DB_files = self.get_names_of_files_in_DBs_dir()
        # For every file with DB get data from file
        for str_filename in list_names_of_DB_files:
            LOGGER.debug("Get data from: %s", str_filename)
            for str_type in LIST_ALL_SUPPORTED_TYPES_OF_DB:
                if str_filename.startswith(str_type):
                    LOGGER.debug(
                        "For file with name: %s  Found type: %s",
                        str_filename,
                        str_type
                    )
                    list_names_of_DB_files.append(str_filename)
                    break
            else:
                LOGGER.warning(
                    "Not DataBase file in DataBase-s folder with name: %s",
                    str_filename
                )
        return list_names_of_DB_files

    def get_dir_names_of_all_dirs_with_daily_DBs(self):
        """Getting names of dir-s with daily results of DB-handler

        Parameters
        ----------
        """
        # Get sorted list of names with dirs with DB data
        if not os.path.exists(self.str_path_main_database_dir):
            logging.warning(
                "Folder to get dir names inside doesn't exist: " +
                self.str_path_main_database_dir
            )
            return []
        list_dir_names = [
            os.path.basename(f.path)
            for f in os.scandir(self.str_path_main_database_dir)
            if f.is_dir()
        ]
        #####
        # Clean list of dirs to leave only ones that satisfy name_template condition
        list_dir_names_cleared = []
        for str_dir_name in list_dir_names:
            try:
                datetime.datetime.strptime(
                    str_dir_name,
                    self.str_datetime_template_rolling
                )
                list_dir_names_cleared.append(str_dir_name)
            except ValueError:
                LOGGER.warning(
                    "Folder name doesn't satisfy template %s: %s",
                    self.str_datetime_template_rolling,
                    str_dir_name
                )
        return list_dir_names_cleared




