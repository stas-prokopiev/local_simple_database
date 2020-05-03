# Standard library imports
import logging
import json

# Third party imports

# Local imports

LOGGER = logging.getLogger("local_simple_database")

class class_dict_database_handler():
    """
    This class was built to handle one DICT DataBase

    ...

    Attributes
    ----------
    self.local_dict_database_obj : object of class: class_local_dict_database
        Handler of all DICT database-s in the folder
    self.str_db_name : str
        Name of DataBase which to use
    self.default_value : object
        Value to use if key in database is not found
    """

    def __init__(
            self,
            local_dict_database_obj,
            str_db_name,
            default_value=None,
    ):
        """Initialize handler object

        Parameters
        ----------
        local_dict_database_obj : object of class: class_local_dict_database
            Handler of all DICT database-s in the folder
        str_db_name : str
            Name of DataBase which to use
        default_value : object, optional
            Value to use if key in database is not found (default is None)
        """
        self.local_dict_database_obj = local_dict_database_obj
        # Check that DB name starts with dict_ otherwise and dict_
        if str_db_name.startswith("dict_"):
            self.str_db_name = str_db_name
        else:
            self.str_db_name = "dict_" + str_db_name
        self.default_value = default_value

    def __repr__(self):
        """Nice representation of object

        Parameters
        ----------
        """
        return self.local_dict_database_obj.read_file_content(self.str_db_name)

    def __getitem__(self, key_to_get):
        """dict_database_handler[key_to_get] method for getting value for key

        Parameters
        ----------
        key_to_get : str
            key from DB to get
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
            key of database dict for which to set value
        value_to_set : object
            Value to set for given key
        """
        dict_current_db_value = self.get_value()
        dict_current_db_value[key_to_set] = value_to_set
        self.set_value(dict_current_db_value)

    def get_value(self):
        """Get current dict value of whole DataBase

        Parameters
        ----------
        """
        str_db_content = \
            self.local_dict_database_obj.read_file_content(self.str_db_name)
        if not str_db_content:
            return {}
        return json.loads(str_db_content)

    def set_value(self, dict_values_to_set):
        """Setting whole value of DataBase to given dictionary

        Parameters
        ----------
        dict_values_to_set : dict
            Any dictionary
        """
        self.local_dict_database_obj.save_file_content(
            json.dumps(dict_values_to_set, sort_keys=True, indent=3),
            self.str_db_name
        )

    def change_default_value(self, new_default_value):
        """Change default value for exactly one DataBase

        Parameters
        ----------
        new_default_value : object
            Value to use if key in database is not found
        """
        self.default_value = new_default_value




