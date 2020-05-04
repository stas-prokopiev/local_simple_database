# -*- coding: utf-8 -*-
import os
from multiprocessing import Process
from local_simple_database import class_local_simple_database



def func1():
    db = class_local_simple_database(str_path_database_dir="tests/tmp_database")
    #####
    for __ in range(100):
        db["int_new_db"] += 1
def func2():
    db = class_local_simple_database(str_path_database_dir="tests/tmp_database")
    #####
    for __ in range(100):
        db["int_new_db"] -= 1



def test_multiprocessing():
    """"""
    #####
    db = class_local_simple_database(str_path_database_dir="tests/tmp_database")
    # Test 1:
    db["int_new_db"] = 0
    p = Process(target=func1)
    p.start()
    p.join()
    assert db["int_new_db"] == 100, "ERROR: func1 is not working"
    # Test 2:
    db["int_new_db"] = 0
    p = Process(target=func1)
    p2 = Process(target=func2)
    p.start()
    p2.start()
    p.join()
    p2.join()
    assert db["int_new_db"] == 0, "ERROR: multiprocessing safety is lost"


