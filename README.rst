========================
LOCAL_SIMPLE_DATABASE
========================

.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/local_simple_database
   :target: https://img.shields.io/github/last-commit/stas-prokopiev/local_simple_database
   :alt: GitHub last commit

.. image:: https://img.shields.io/github/license/stas-prokopiev/local_simple_database
    :target: https://github.com/stas-prokopiev/local_simple_database/blob/master/LICENSE.txt
    :alt: GitHub license<space><space>

.. image:: https://readthedocs.org/projects/local-simple-database/badge/?version=latest
    :target: https://local-simple-database.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/stas-prokopiev/local_simple_database.svg?branch=master
    :target: https://travis-ci.org/stas-prokopiev/local_simple_database

.. image:: https://img.shields.io/pypi/v/local_simple_database
   :target: https://img.shields.io/pypi/v/local_simple_database
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/local_simple_database
   :target: https://img.shields.io/pypi/pyversions/local_simple_database
   :alt: PyPI - Python Version


.. contents:: **Table of Contents**

Short Overview.
=========================

local_simple_database is a simple Python package(**py>=2.7 or py>=3.4**)
with the main purpose to
help storing and retrieving data from human-readable .txt files with one line of code.
All the interactions with files are being made in a processes-threads safe manner.

Long Overview.
=========================

This package consists of 2 main classes with which user should interact:

#. LocalSimpleDatabase
#. LocalDictDatabase

One small example
----------------------

Let's say you want to store file with int variable with name int_times_I_ve_eaten.

Then, using this package, you can do it like this:

.. code-block:: python

    from local_simple_database import LocalSimpleDatabase
    LSD = LocalSimpleDatabase(path_to_dir_where_to_save_file)

and then just use everywhere in your code **LSD["int_times_I_ve_eaten"]** like if it was usual dictionary.

.. code-block:: python

    LSD["int_times_I_ve_eaten"] += 1  # To increase value in the file
    LSD["int_times_I_ve_eaten"]  # To get current value from the file

| After running this code with:
| *path_to_dir_where_to_save_file = "./folder_with_all_my_databases"*
| Inside directory *./folder_with_all_my_databases*
| will be created file *"int_times_I_ve_eaten.txt"* with current value.

| Value is stored in a human-readable .txt file, so you can always access it.
| To get it some time later or from another process just use:

.. code-block:: python

    int_value_I_was_afraid_to_lose = LSD["int_times_I_ve_eaten"]

How to name databases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Name of database should satisfy template "type_name"

Examples: int_balls, float_seconds_left, str_my_name, dict_useless_heap

So just by the name you can define the type of database, isn't it awesome.

Installation
============

* Install via pip:

.. code-block:: bash

    pip install local_simple_database


Basic usage.
=========================

1) LocalSimpleDatabase
--------------------------------------------------------------------------------------------------

This class is built to handle (saving-retrieving) one value data like integer or float.

For now supported types of databases are:

- ["int", "float", "str", "datetime"] (Probably will be enhanced soon)
- This means that one file with database can handle only type data

Initialization of databases handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from local_simple_database import LocalSimpleDatabase
    LSD = LocalSimpleDatabase(
        str_path_database_dir=".",
    )

Arguments:

1. **str_path_database_dir**:
    | If the explicit path is not given or variable is not set at all,
    | then will be used path "./local_database"
    | Folder for database will be created automatically

A few examples of Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After you've initialized LSD object you can use:

1) Integer database
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

*If you want to store/access/modify simple int in file:*

.. code-block:: python

    # Process 1
    LSD["int_red_cars_drove"] += 1
    LSD["int_red_cars_drove"] += 2
    # Oh now, last one was burgundy
    LSD["int_red_cars_drove"] -= 1

    # Process 2
    print("red cars already found", LSD["int_red_cars_drove"])
    # If there was no such DataBase yet, than in will be created and 0 value will be returned.
    LSD["int_red_cars_drove"] = 5
    print("Red cars already found: ", LSD["int_red_cars_drove"])

2) Float database
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: python

    LSD["float_last_price_of_watermelons"] = 7.49
    # Too many watermelons this year, need to apply 30% discount
    LSD["float_last_price_of_watermelons"] *= 0.7
    print(
        "Hello my best customer, current price on watermelons is: ",
        LSD["float_last_price_of_watermelons"]
    )

3) Datetime database
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
.. code-block:: python

    import datetime
    # Saving datetime in file in ISO format (E.G. 2020-05-16T18:00:41.780534)
    LSD["datetime_now"] = datetime.datetime.now()

    # Load datetime obj from DataBase
    # if DB not found will be retunrs datetime for 1970-01-01
    print("Hour was a moment ago: ", LSD["datetime_now"].hour)

    # Use DataBase value to find timedelta
    int_seconds_gone = (datetime.datetime.now() - LSD["datetime_now"]).seconds
    print("Seconds gone: ", int_seconds_gone)

4) Date database
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Very similar to datetime database, but only date will by saved

.. code-block:: python

    import datetime
    # Saving datetime in file in ISO format (E.G. 2020-05-16)
    LSD["date_now"] = datetime.datetime.now()

    # Load datetime obj from DataBase
    # if DB not found will be retunrs datetime for 1970-01-01
    print("Date today: ", LSD["date_now"])

    # Use DataBase value to find timedelta
    if datetime.datetime.now().date() == LSD["date_now"]:
        int_seconds_gone_today = (datetime.datetime.now() - LSD["date_now"]).seconds
        print("Seconds already gone: ", int_seconds_gone_today)

2) LocalDictDatabase
--------------------------------------------------------------------------------------------------

This class was built to handle (saving-retrieving) dictionary with data from a file.

Work with such database is a little different from **LocalSimpleDatabase** so it was necessary to put it in a separate class

Initialization of databases handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from local_simple_database import LocalDictDatabase
    LDD = LocalDictDatabase(
        str_path_database_dir=".",
        default_value=None,
    )

Arguments:

#. **str_path_database_dir**:
    | If the explicit path is not given or variable is not set at all,
    | then will be used path "./local_database"
    | Folder for databases will be created automatically
#. **default_value**: value to use for any database if key in it is not found.
    | LDD[database_name][key] = default_value

A few examples of Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1) Basic store/access/modify data from a dict database.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: python

    # Set methods
    ## Set value for whole LDD:
    LDD["dict_very_useful_heap"] = {"Mike": 50, "Stan": 1000000}

    ## Set keys for one dictionary LDD
    ## If there is no file with asked dict database then it will be created automatically
    LDD["dict_useless_heap"]["random_key"] = 1
    LDD["dict_useless_heap"]["random_key"] += 3
    LDD["dict_useless_heap"][2] = ["Oh my God, what a list is doing here", "Aaa"]
    LDD["dict_useless_heap"][99] = {"Are you serious?": {"You'd better be!": "Bbb"}}

    # Get methods
    ## To get whole dict for LDD, please use:
    LDD["dict_useless_heap"].get_value()  # Sorry for that, I don't know how to do it without additional method

    ## To get string representation of whole dict:
    print(LDD["dict_useless_heap"])

    ## To get one key from dict:
    int_random_key = LDD["dict_useless_heap"]["random_key"]


2) Set default value:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: python

    # You can set the default value for all databases OR for only one:

    ## 1) Set default value for any database when can't find key:
    LDD.change_default_value(0)

    ## 2) Set default value for one database:
    LDD["cars"].change_default_value(0)

    # They you can use LDD similarly to collections.defaultdict
    LDD["cars"]["red"] += 1
    # Oh no, that was burgundy once again
    LDD["cars"]["red"] -= 1
    LDD["cars"]["burgundy"] += 1


Advanced usage (can be skipped, you already know enough to use it)
===================================================================

1) class database additional arguments
--------------------------------------------------------------------------------------------------

Both 2 main classes (**LocalSimpleDatabase**, **LocalDictDatabase**) have additional arguments:

1) **str_datetime_template_for_rolling=""**

    | This variable allows setting rolling save of database results using the DateTime template.
    | If the value is not empty, then saving/retrieving results will be done from deeper folders with names satisfy the evaluation of the DateTime string template.
    | E.G. To save daily results use "%Y%m%d" (Then deeper folder names will be like "20191230", "20191231", ...)
    | E.G. To save hourly results use "%Y%m%d_%H" (Then deeper folder names will be like "20191230_0", "20191230_23", ...)

2) **float_max_seconds_per_file_operation=0.01**

    | This variable is necessary for multiprocessing safe work.
    | It setting time in which LSD file accessed by process can't be accessed by any other process.
    |    By default, it is set to 10 ms for simple database and 20 ms for dict database.
    | If you use operations which from accessing value till setting new value needs more time, you are more than welcome to increase it.
    | You can set it to 0.0 if you are not using threads-processes and want the maximum speed.


.. code-block:: python

    # Full definition of LocalSimpleDatabase
    LSD = LocalSimpleDatabase(
        str_path_database_dir=".",
        float_max_seconds_per_file_operation=0.05,
        str_datetime_template_for_rolling=""
    )

.. code-block:: python

    # Full definition of LocalDictDatabase
    LDD = LocalDictDatabase(
        str_path_database_dir=".",
        default_value=None,
        float_max_seconds_per_file_operation=0.05,
        str_datetime_template_for_rolling=""
    )

2) Rolling example
--------------------------------------------------------------------------------------------------

.. code-block:: python

    LSD_daily_rolling = LocalSimpleDatabase(
        str_path_database_dir=".",
        str_datetime_template_for_rolling="%Y%m%d"
    )

3) Get values for ALL databases in the directory.
--------------------------------------------------------------------------------------------------

To get a dictionary with data in all databases by database name, use:

.. code-block:: python

    LSD.get_dict_data_by_db_name()

If you were using rolling, then you can get dictionary with results like {"datetime_1": dict_all_DBs_date_1, }

.. code-block:: python

    LSD.get_dict_every_DB_by_datetime()


If you were using rolling, and interested only in one database. {"datetime_1": database_value_1, ...}

.. code-block:: python

    # Please replace *str_database_name* on name of LSD which values you want to get
    LSD.get_one_db_data_daily(
        str_database_name,
        value_to_use_if_db_not_found=None
    )

Links
=====

    * `PYPI <https://pypi.org/project/local_simple_database/>`_
    * `readthedocs <https://local-simple-database.readthedocs.io/en/latest/>`_
    * `GitHub <https://github.com/stas-prokopiev/local_simple_database>`_

Project local Links
===================

    * `CHANGELOG <https://github.com/stas-prokopiev/local_simple_database/blob/master/CHANGELOG.rst>`_.
    * `CONTRIBUTING <https://github.com/stas-prokopiev/local_simple_database/blob/master/CONTRIBUTING.rst>`_.

Contacts
========

    * Email: stas.prokopiev@gmail.com
    * `vk.com <https://vk.com/stas.prokopyev>`_
    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_

License
=======

This project is licensed under the MIT License.
