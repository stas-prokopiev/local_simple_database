========================
LOCAL_SIMPLE_DATABASE
========================

.. contents:: **Table of Contents**

Short Overview.
=========================

local_simple_database is a simple Python package(**py>=2.7 or py>=3.4**) with the main purpose to
help storing and retrieving data from human readable txt files just with one line of code.

Long Overview.
=========================

The main reason of building this package was to create universal
tool for dealing with data in files in process-thread protected way.

It's very useful when you want to store in txt file some simple data like integer number and have easy access to it from different places in your program.

---

One small example, let's say you want to want store file with int variable with name times_I_ve_eaten.

Then you should define handler of databases (E.G. at the top of you python of program)

.. code-block:: python

    from local_simple_database import class_local_simple_database
    DB = class_local_simple_database("folder_with_all_my_databases")

and then just use everywhere in you code DB["times_I_ve_eaten"] like as it was usual dict.

If new database type is not recognizable (check More info paragraph) then by default it will be considered as int-database.

.. code-block:: python

    DB["times_I_ve_eaten"] += 1  # To increase value in the file
    DB["times_I_ve_eaten"]  # To get current value from the file

After running this code in the folder with path = "folder_with_all_my_databases" will be created file "folder_with_all_my_databases/int_times_I_ve_eaten.txt" where value of this database will be stored.

As value is stored in human readable txt file you can always access it and even after restart of computer it'll still be there.

To get it, just use:

.. code-block:: python

    int_value_I_was_afraid_to_lose = DB["times_I_ve_eaten"]


More info.
=========================

1) Supported types
--------------------------------------------------------------------------------------------------

For now on supported types of databases are: ["int", "float", "str", "list"] (probably will be enhanced soon)

- This mean that you can use database with one value inside with types of value: integer, float, string
- Or You can use database with list of values (every value will be converted to string). For more info check section: **Typical examples of Usage**

2) Initialization of databases handler
--------------------------------------------------------------------------------------------------

.. code-block:: python

    DB = class_local_simple_database(str_path_database_dir="", bool_if_to_use_everyday_rolling=False)

As you can see initialization has 2 optional arguments

1. If explicit path to database is not given, then will be used path "./local_database"
    Folder for database-s will be created automaticaly
2. If flag bool_if_to_use_everyday_rolling set to True, 
    then inside database folder will be created additional folders with names YYYYMMDD. 
    Add with every access to DB you will be getting todays database data.

3) How to name database-s
--------------------------------------------------------------------------------------------------

To set type of database you have to use type as prefix for the name of database. 

Examples: int_times_cat_purred, float_sec_last_download_took, str_best_friend_name, list_se

4) Description of some processes underhood
--------------------------------------------------------------------------------------------------

Also this package can be used for saving some daily statistics (data) you see useful for yourself.

For more info check section: **Typical examples of Usage**

Installation
============

* Install via setup.py:

.. code-block:: bash

    git clone git@github.com:stas-prokopiev/local_simple_database.git
    cd local_simple_database
    python setup.py install

* Install via pip:

.. code-block:: bash

    pip install local_simple_database

Typical examples of Usage
=========================

The first thing you need to do is to initialize database in some directory.

To do so you need to replace "path_to_folder_1" from the code below on most parent folder of all files you want to analyze.


.. code-block:: python

    from local_simple_databaseimport class_local_simple_database
    DB = class_local_simple_database(
            str_path_to_your_database,
            bool_if_to_use_everyday_rolling=False
    )

Please note that first initialization can be a long process if the folders where you search for files are deep and wide.

But after finding all files they won't be downloaded again unless they were changed. So excellent performance is expected.

1) To find all occurrences of some code.
--------------------------------------------------------------------------------------------------

*E.G. You've changed a function signature and want to do necessary changes in the library.*

*To find all the places where this function was used use the code below*

.. code-block:: python

    code_searcher_obj.search_code_in_the_library(
        str_code_to_search="print_places_where_line_length_exceed_N",
        bool_is_to_search_case_sensitive=True,
    )

*Output:*

.. code-block:: console

    For folder: c:\users\stanislav\desktop\my_python_projects\code_search_engine\project\code_searcher\src\code_searcher

    --> For extension: .py
    ----> Found in:  code_searcher_class.py
    ------> 0) line: 93  Code_line: print_places_where_line_length_exceed_N(
    ------> 1) line: 444  Code_line: def print_places_where_line_length_exceed_N(

    --> For extension: ipynb
    ----> NOTHING FOUND.


2) To find all occurrences of some regular expression pattern
--------------------------------------------------------------------------------------------------


One example where it can be useful, let's say that you want to store time interval in which you got response from the server, then you can store it 


.. code-block:: python

    code_searcher_obj.search_code_in_the_library_with_re(
        str_code_to_search="^from __future__ import[\s]+"
    )

*Output:*

.. code-block:: console

    For folder: c:\users\stanislav\desktop\my_python_projects\code_search_engine\project\code_searcher\src\code_searcher

        --> For extension: .py
        ----> Found in:  additional_functions.py
        ------> 0) line: 12  Code_line: from __future__ import print_function
        ----> Found in:  code_searcher_class.py
        ------> 1) line: 11  Code_line: from __future__ import print_function
        ----> Found in:  decorators.py
        ------> 2) line: 12  Code_line: from __future__ import print_function
        ----> Found in:  working_with_files.py
        ------> 3) line: 12  Code_line: from __future__ import print_function

        --> For extension: ipynb
        ----> NOTHING FOUND.

4) To add new files to examine.
--------------------------------------------------------------------------------------------------

*If you've created a new file inside folder given to code_searcher then you should update files for code_searcher*

.. code-block:: python

    code_searcher_obj.update_files()


Links
=====

    * `Pypi <https://pypi.org/project/code-searcher/>`_
    * `readthedocs <https://code-searcher.readthedocs.io/en/latest/>`_
    * `GitHub <https://github.com/stas-prokopiev/code_searcher>`_

Releases
========

See `CHANGELOG <https://github.com/stas-prokopiev/code_searcher/blob/master/CHANGELOG.rst>`_.

Contributing
============

- Fork it (<https://github.com/stas-prokopiev/code_searcher/fork>)
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

inee a  sedimerom leileath herl beac