# -*- coding: utf-8 -*-
import os
from local_simple_database import LocalSimpleDatabase


def test_LocalSimpleDatabase():
    """"""
    # Check
    DB = LocalSimpleDatabase(
        "",
        float_max_seconds_per_file_operation=0
    )
    #####
    # Check creating of new dir
    str_dir_tmp = os.path.abspath("tests/tmp_database/empty_dir")
    if os.path.isdir(str_dir_tmp):
        os.rmdir(str_dir_tmp)
    DB_tmp = LocalSimpleDatabase(
        str_path_database_dir=str_dir_tmp
    )
    #####

    DB2 = LocalSimpleDatabase("tests/tmp_database")

    DB2["int_please_delete_me"] += 1
