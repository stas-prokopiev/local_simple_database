# -*- coding: utf-8 -*-
import os
from local_simple_database import class_local_dict_database


def test_class_local_dict_database():
    """"""
    DB = class_local_dict_database(str_path_database_dir="tests/tmp_database")
    DB["dict_random"] = {}
    DB["dict_random"][1] = 2
    DB["dict_random"].change_default_value(0)
    DB["dict_random"]["key"] += 1
    DB["dict_random"]["key"] += 10
    #####
    DB2 = DB.init_new_class_obj(str_path_database_dir="tests/tmp_database")
    DB2["dict_random_2"] = {}
    DB2["dict_random_2"] = {"hello": "hello2"}
    try:
        DB2["dict_random_2"][4]
    except KeyError:
        pass
    except:
        assert False, "ERROR: Wrong exception was raised"
    DB2.change_default_value(0)
    DB2["dict_random_2"].change_default_value(0)
    DB2["dict_random_2"][3] += 100
    DB2["dict_random_2"][4]
    #####
    DB["dict_random3"].get_value()
    #####
    return 0