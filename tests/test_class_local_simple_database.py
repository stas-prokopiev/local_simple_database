# -*- coding: utf-8 -*-
import os
from local_simple_database import LocalSimpleDatabase


def test_LocalSimpleDatabase():
    """"""
    DB = LocalSimpleDatabase(
        str_path_database_dir="tests/tmp_database"
    )
    DB2 = DB.init_new_class_obj(
        str_path_database_dir="tests/tmp_database"
    )
    #####
    DB["int_random_name_do_not_use_it_more"]
    DB["int_tmp"] = 1
    DB["int_tmp"] += 1
    assert DB["int_tmp"] == 2, "ERROR, something wrong with DB"
    #####
    DB2["float_random_name_do_not_use_it_more"]
    DB2["float_tmp"] = 1.0
    DB2["float_tmp"] += 2
    DB2["float_tmp"] /= 3
    assert DB2["float_tmp"] == 1.0, "ERROR, something wrong with DB2"
    #####
    DB2["str_random_name_do_not_use_it_more"]
    DB2["str_tmp"] = "empty"


    #####
    try:
        DB["wrong_name"]
    except KeyError:
        pass
    except:
        assert False, "Something is wrong"
    #####

    return 0


