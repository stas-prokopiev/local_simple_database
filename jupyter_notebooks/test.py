

from local_simple_database import class_local_simple_database
from local_simple_database import class_local_dict_database



def func1():
    """"""
    print("Func1: STARTED")
    db = class_local_simple_database()
    #####
    for __ in range(1000):
        db["int_new_db"] += 1
    print("Func1: FINISHED")
    return None


def func2():
    """"""
    print("Func2: STARTED")
    db = class_local_simple_database()
    #####
    for __ in range(1000):
        db["int_new_db"] -= 1
    print("Func2: FINISHED")
    return None