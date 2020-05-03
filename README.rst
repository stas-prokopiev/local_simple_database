========================
LOCAL_SIMPLE_DATABASE
========================

.. contents:: **Table of Contents**


Short Overview.
=========================

local_simple_database is a simple Python package(**py>=2.7 or py>=3.4**) with the main purpose to
help storing and retrieving data from human readable txt files in just with one line of code as
if it were usual python variables. All of this done in process-thread safe manner.


Long Overview.
=========================

This package consists of 2 main classes with which user should interact
#. class_local_simple_database
#. class_local_dict_database

One small example
----------------------

Let's say you want to want store file with int variable with name int_times_I_ve_eaten.

Then you should define handler of databases (E.G. at the top of you python of program)

.. code-block:: python

    from local_simple_database import class_local_simple_database
    DB = class_local_simple_database("folder_with_all_my_databases")

and then just use everywhere in you code DB["int_times_I_ve_eaten"] like as it was usual dict.

.. code-block:: python

    DB["int_times_I_ve_eaten"] += 1  # To increase value in the file
    DB["int_times_I_ve_eaten"]  # To get current value from the file

After running this code in the folder with path = "folder_with_all_my_databases" will be created file "folder_with_all_my_databases/int_times_I_ve_eaten.txt" where value of this database will be stored.

As value is stored in human readable txt file you can always access it and even after restart of computer it'll still be there.

To get it, just use:

.. code-block:: python

    int_value_I_was_afraid_to_lose = DB["int_times_I_ve_eaten"]


How to name database-s
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Name of database should satisfy template "type_name" (E.G. int_balls, float_seconds_left, str_my_name, dict_useless_heap)

So just by name you can define the type of database, isn't it awesome.

Installation
============

* Install via pip:

.. code-block:: bash

    pip install local_simple_database


Diving deeper.
=========================

1) class_local_simple_database
--------------------------------------------------------------------------------------------------

This class was built to handle (saving-retrieving) one value simple data like integer or float.

For now on supported types of databases are: ["int", "float", "str"] (Probably will be enhanced soon)

- This mean that you can use database with one value inside with types of value: integer, float, string

Initialization of databases handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    DB = class_local_simple_database(
        str_path_database_dir=".",
    )

Arguments:

1. **str_path_database_dir**: If explicit path to database-s is not given, then will be used path "./local_database"
    Folder for database-s will be created automatically

A few examples of Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first thing you need to do is to initialize database in some directory.

To do so you need to replace str_path_database_dir from the code below on folder where you would like to store file or leave it blank.

.. code-block:: python

    from local_simple_database import class_local_simple_database
    DB = class_local_simple_database(str_path_database_dir=".")

1) Integer database
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

*If you want to store/access/modify simple int in file*

.. code-block:: python

    # Process 1
    DB["int_red_cars_drove"] += 1
    DB["int_red_cars_drove"] += 2
    # Oh now, last one was burgundy
    DB["int_red_cars_drove"] -= 1

    # Process 2
    print("red cars already found", DB["int_red_cars_drove"])
    # If there was no such DataBase yet, than in will be created and 0 value will be returned.
    DB["int_red_cars_drove"] = 0
    print("red cars already found", DB["int_red_cars_drove"])

2) Float database
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: python

    DB["float_last_price_of_watermelon"] = 7.49
    # Too many watermelons this year, need to apply 30% discount
    DB["float_last_price_of_watermelon"] *= 0.7
    print("Hello my best customer, current price on watermelon is: ", DB["float_last_price_of_watermelon"])


2) class_local_dict_database
--------------------------------------------------------------------------------------------------

This class was built to handle (saving-retrieving) dictionary of data from file.

Work with such database-s is a little different from *class_local_simple_database* so it was necessary to put it in separate class

Initialization of databases handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    DB = class_local_simple_database(
        str_path_database_dir=".",
        default_value=None,
    )

Arguments:

1. **str_path_database_dir**: If explicit path to database-s is not given, then will be used path "./local_database"
    Folder for database-s will be created automatically
2. **default_value**: value to use if key in DB not found.

A few examples of Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first thing you need to do is to initialize database in some directory.

To do so you need to replace str_path_database_dir from the code below on folder where you would like to store file or leave it blank.

.. code-block:: python

    from local_simple_database import class_local_simple_database
    DB = class_local_simple_database(str_path_database_dir=".")


1) Basic Save-Get data from dict database.
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: python

    # Set methods
    # Set value for whole DB:
    DB["dict_very_useful_heap"] = Any dictionary here

    ## Set keys for one DB with dict
    DB["dict_useless_heap"]["random_key"] = 1
    DB["dict_useless_heap"]["random_key"] += 3
    DB["dict_useless_heap"][2] = ["Oh my God, what a list is doing here", "Aaa"]
    DB["dict_useless_heap"][99] = {"Are you serious?": {"You'd better be!": "Bbb"}}

    # Get methods
    ## To get whole dict for DB use:
    DB["dict_useless_heap"].get_value()  # Sorry for that, I don't know how to get rid of this additional method

    ## To get string representation of whole dict:
    str(DB["dict_useless_heap"])
    print(DB["dict_useless_heap"])

    ## To get one key from dict:
    int_random_key = DB["dict_useless_heap"]["random_key"]


2) Set default value:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: python

    # You can set default value for all databases OR for only one

    ## 1) Set default value for all database-s:
    DB.change_default_value(0)

    ## 2) Set default value for one database:
    DB["cars"].change_default_value(0)

    # They you can use DB similarly as collections.defaultdict
    DB["cars"]["red"] += 1
    # Oh no, that was burgundy one
    DB["cars"]["red"] -= 1
    DB["cars"]["burgundy"] += 1



Advanced usage.
=========================

1) class database additional arguments
--------------------------------------------------------------------------------------------------

Both 2 main classes (**class_local_simple_database**, **class_local_dict_database**) have additional arguments.

float_max_seconds_per_file_operation=0.05
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This variable necessary for multiprocessing safe work.

It set time in which accessed by process file can't be accessed by any other process.
By default it set to 50 ms.

If your operation from accessing value till setting new value need more time, you are more than welcome to increase this value.

You can set it to 0.0 if you are not using threads-processes.

str_datetime_template_for_rolling=""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

This variable allow to set rolling save of database results using datetime template.

If value is not empty, then saving/retrieving results will be done from deeper folders with names satisfy datetime evaluation of string given.

E.G. To save daily results use "%Y%m%d" (Then deeper folder names will be like "20191230", "20191231", ...)

E.G. To save hourly results use "%Y%m%d_%H" (Then deeper folder names will be like "20191230_0", "20191230_23", ...)


2) Get values in ALL databases in the directory.
--------------------------------------------------------------------------------------------------

To get dictionary with data in all databases by database name, use:

.. code-block:: python

    DB.get_dict_DBs_data_by_DB_name()

If you were using rolling, then you can get dictionary with results like {"datetime_1": dict_all_DBs_data_1, }

.. code-block:: python

    DB.get_dict_every_DB_by_datetime()


If you were using rolling, and interested only in one database. {"datetime_1": database_value_1, ...}

.. code-block:: python
    DB.get_one_DB_data_daily(
        str_db_name,
        value_to_use_if_DB_not_found=None
    )



Links
=====

    * `Pypi <https://pypi.org/project/local_simple_database/>`_
    * `GitHub <https://github.com/stas-prokopiev/local_simple_database>`_

Releases
========

See `CHANGELOG <https://github.com/stas-prokopiev/local_simple_database/blob/master/CHANGELOG.rst>`_.

Contributing
============

- Fork it (<https://github.com/stas-prokopiev/local_simple_database/fork>)
- Create your feature branch (`git checkout -b feature/fooBar`)
- Commit your changes (`git commit -am 'Add some fooBar'`)
- Push to the branch (`git push origin feature/fooBar`)
- Create a new Pull Request

Contacts
========

    * Email: stas.prokopiev@gmail.com

    * `vk.com <https://vk.com/stas.prokopyev>`_

    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_

License
=======

This project is licensed under the MIT License.
