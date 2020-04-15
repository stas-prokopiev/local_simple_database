import sys, os
from all_CONSTANTS import *
#####
import time
from working_with_files import get_list_of_fields_in_file
from working_with_files import save_list_of_fields_in_file
from working_with_strings import leave_only_digits_in_string
from time import sleep
from random import randint   # Для рандомной задержки
from scripts_USEFULL_EVERYWHERE import check_with_assert_that_type_is_correct


# Все функции работы с различными серверами
MAX_NUMBER_OF_PARALLEL_CORELATION_CALCULATIONS = 2000
TIME_AFTER_WHICH_UNCALCULATED_CORRELATION_DELETED = 240
MAX_NUMBER_OF_PARALLEL_CHECK_SUBMISSIONS = 3
TIME_AFTER_WHICH_UNCALCULATED_CHECK_SUBMISSIONS_DELETED = 120
TIME_UPDATING_STATUS_OF_MY_ALPHAS_SERVER = 300
# Словарь с полными путями к файлам серверов
dict_path_to_server_file_by_server_name = {}
dict_path_to_server_file_by_server_name["my_alphas"] = path_to_servers_conditions + 'my_alphas_server_condition.txt'
dict_path_to_server_file_by_server_name["login"] = path_to_servers_conditions + 'login_server_condition.txt'
dict_path_to_server_file_by_server_name["correlation"] = path_to_servers_conditions + 'correlation_server_condition.txt'
dict_path_to_server_file_by_server_name["check submission"] = path_to_servers_conditions + 'check_submission_server_condition.txt'
dict_path_to_server_file_by_server_name["clipboard_is_using_now"] = path_to_servers_conditions + 'is_clipboard_using_now_server.txt'
dict_path_to_server_file_by_server_name["is_my_alphas_submittor_script_working_now"] = path_to_servers_conditions + 'my_alphas_submittor_script_condition.txt'
dict_path_to_server_file_by_server_name["is_simulator_one_last_tab_avaliable_for_fastest_simulator"] = path_to_servers_conditions + 'bool_is_last_tab_free.txt'
dict_path_to_server_file_by_server_name["my_correlation_matrix_server_condition"] = path_to_servers_conditions + 'my_correlation_matrix_server_condition.txt'


LIST_SERVERS_WITH_PARALLEL_REQUESTS = ["correlation", "check submission"]


def write_that_myalphas_server_is_free(
        str_which_server_to_check="my_alphas",
        int_value_to_delete_if_saving_list_of_times=0,
        bool_whether_to_print_info=True
):
    """Функция, которая сообщает, что сервер свободен"""
    check_with_assert_that_type_is_correct(str_which_server_to_check, str)
    check_with_assert_that_type_is_correct(int_value_to_delete_if_saving_list_of_times, int)
    check_with_assert_that_type_is_correct(bool_whether_to_print_info, bool)
    #####
    # Выбираем с каким сервером работать
    path_to_my_alphas_server_condition_file = dict_path_to_server_file_by_server_name[str_which_server_to_check]
    if str_which_server_to_check == "correlation":
        TIME_AFTER_WHICH_UNCALCULATED_VALUES_WILL_BE_DELETED = TIME_AFTER_WHICH_UNCALCULATED_CORRELATION_DELETED
    if str_which_server_to_check == "check submission":
        TIME_AFTER_WHICH_UNCALCULATED_VALUES_WILL_BE_DELETED = TIME_AFTER_WHICH_UNCALCULATED_CHECK_SUBMISSIONS_DELETED
    # Работаем
    # В случае сервера корреляции удаляем значение, которое передано в функцию
    if (str_which_server_to_check in LIST_SERVERS_WITH_PARALLEL_REQUESTS):
        list_times_generation_on_server_started = get_list_of_fields_in_file(path_to_my_alphas_server_condition_file, whether_to_print_information=False)
        # Если элемент не найден в списке и время, когда этот элемент еще должен быть активен не истекло, то
        if (
            (str(int_value_to_delete_if_saving_list_of_times) not in list_times_generation_on_server_started) and
            ((int(time.time()) - int(int_value_to_delete_if_saving_list_of_times)) <= TIME_AFTER_WHICH_UNCALCULATED_VALUES_WILL_BE_DELETED)
        ):
            if bool_whether_to_print_info:
                print("Element: ", str(int_value_to_delete_if_saving_list_of_times), " not in list:")
                print(list_times_generation_on_server_started)
            return 0
        elif ((int(time.time()) - int(int_value_to_delete_if_saving_list_of_times)) <= TIME_AFTER_WHICH_UNCALCULATED_VALUES_WILL_BE_DELETED):
            # На всякий случай проверяем, вдруг другой процесс удалит запись
            try:
                list_times_generation_on_server_started.remove(str(int_value_to_delete_if_saving_list_of_times))
            except:
                print("Unable to delete record from " + str_which_server_to_check + " server: ", int_value_to_delete_if_saving_list_of_times)
        else:
            pass
        # Сохранияем новый список
        save_list_of_fields_in_file(list_times_generation_on_server_started, path_to_my_alphas_server_condition_file)
        # Печатаем информацию
        if bool_whether_to_print_info:
            print(
                str_which_server_to_check + " record was deleted from txt, because " +
                str_which_server_to_check + " was calculated, now on server left: ",
                len(list_times_generation_on_server_started),
                " records"
            )
    # Для любого друго сервера просто пишем 1, как состояние
    else:
        save_list_of_fields_in_file(['1'], path_to_my_alphas_server_condition_file)
    return 1


def write_time_of_last_request_to_server(which_server_to_check="my_alphas"):
    """Пишем на сервер время последнего запроса"""
    assert isinstance(which_server_to_check, str), "variable 'which_server_to_check' is not str"
    #####
    # Выбираем с каким сервером работать
    path_to_my_alphas_server_condition_file = dict_path_to_server_file_by_server_name[which_server_to_check]
    # Работаем
    # В случае сервера корреляции добавляем новый элемент в список
    int_time_of_request_to_server = (int(time.time()))  # str
    if (which_server_to_check in LIST_SERVERS_WITH_PARALLEL_REQUESTS):
        list_times_generation_on_server_started = get_list_of_fields_in_file(path_to_my_alphas_server_condition_file, whether_to_print_information=False)
        list_times_generation_on_server_started.append(int_time_of_request_to_server)
        # Сохранияем новый список
        save_list_of_fields_in_file(list_times_generation_on_server_started, path_to_my_alphas_server_condition_file)
    else:
        # Для любого друго сервера просто пишем время запроса, как состояние
        save_list_of_fields_in_file([int_time_of_request_to_server], path_to_my_alphas_server_condition_file)
    return int_time_of_request_to_server


def check_that_myalphas_server_is_free(
        time_to_make_new_request_to_myalphas_server=3600 * 24 * 2,
        which_server_to_check="my_alphas",
        whether_to_print_info=True
):
    """Функция проверки, что сервер свободен"""
    from working_with_files import check_that_txt_file_exist_otherwise_create
    assert isinstance(time_to_make_new_request_to_myalphas_server, int), "variable 'time_to_make_new_request_to_myalphas_server' is not int"
    assert isinstance(which_server_to_check, str), "variable 'which_server_to_check' is not str"
    assert isinstance(whether_to_print_info, bool), "variable 'whether_to_print_info' is not bool"
    #####
    # Выбираем с каким сервером работать
    path_to_my_alphas_server_condition_file = dict_path_to_server_file_by_server_name[which_server_to_check]
    if which_server_to_check == "my_alphas":
        time_to_make_new_request_to_myalphas_server = TIME_UPDATING_STATUS_OF_MY_ALPHAS_SERVER
    if which_server_to_check == "correlation":
        MAX_NUMBER_OF_PARALLEL_CALCULATIONS = MAX_NUMBER_OF_PARALLEL_CORELATION_CALCULATIONS
        TIME_AFTER_WHICH_UNCALCULATED_VALUES_WILL_BE_DELETED = TIME_AFTER_WHICH_UNCALCULATED_CORRELATION_DELETED
    if which_server_to_check == "check submission":
        MAX_NUMBER_OF_PARALLEL_CALCULATIONS = MAX_NUMBER_OF_PARALLEL_CHECK_SUBMISSIONS
        TIME_AFTER_WHICH_UNCALCULATED_VALUES_WILL_BE_DELETED = TIME_AFTER_WHICH_UNCALCULATED_CHECK_SUBMISSIONS_DELETED
    # Работаем
    check_that_txt_file_exist_otherwise_create(path_to_my_alphas_server_condition_file)
    list_of_server_conditions = get_list_of_fields_in_file(path_to_my_alphas_server_condition_file, whether_to_print_information=False)
    int_time_now = int(time.time())
    # В случае сервера корреляции проверяем количество и время последнего элемента (если время истекло, то удаляем его)
    if (which_server_to_check in LIST_SERVERS_WITH_PARALLEL_REQUESTS):
        new_list_of_server_conditions = []
        # Удаляем все элементы у которых истекло время
        number_of_deleted_correlation_server_conditions_because_of_time_out = 0
        for server_condition_elem in list_of_server_conditions:
            try:
                if int_time_now - int(server_condition_elem) < TIME_AFTER_WHICH_UNCALCULATED_VALUES_WILL_BE_DELETED:
                    new_list_of_server_conditions.append(server_condition_elem)
                else:
                    number_of_deleted_correlation_server_conditions_because_of_time_out += 1
            except:
                print("ERROR ERROR in deleting record from server: ", which_server_to_check, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", flush=True)
                print("server condition element that is UNPREDICTED: ", server_condition_elem, flush=True)
        # Если удаляются какие-то записи о генерации корреляции из-за того, что закончилось время, то пишем об этом в консоль
        if number_of_deleted_correlation_server_conditions_because_of_time_out and whether_to_print_info:
            print(
                "Because of time out from " + which_server_to_check.upper() +
                " SERVER were deleted: ",
                number_of_deleted_correlation_server_conditions_because_of_time_out,
                " records",
                flush=True
            )
        # Сохранияем новый список
        save_list_of_fields_in_file(new_list_of_server_conditions, path_to_my_alphas_server_condition_file)
        if (len(new_list_of_server_conditions) < MAX_NUMBER_OF_PARALLEL_CALCULATIONS):
            if whether_to_print_info:
                print("Now on " + which_server_to_check + " server is: ", len(new_list_of_server_conditions), " alphas calculating", flush=True)
            return 1
    # Для любого друго сервера проверяем только первый элемент
    else:
        # Оставляем только цифры
        digit_content = leave_only_digits_in_string(list_of_server_conditions[0], with_sign=False)
        # Проверяем, что хоть что-то считали
        if(len(digit_content) < 1):
            print("!!!Server condition file is empty!!!", flush=True)
            write_that_myalphas_server_is_free(str_which_server_to_check=which_server_to_check)
            return 1
        int_server_condition = int(digit_content)
        # Если прошло достаточно времени с прошлого запроса, то сервер свободен
        if(int_time_now - int_server_condition > time_to_make_new_request_to_myalphas_server):
            return 1
    return 0


def full_wait_that_my_alphas_server_is_free(
        which_server_to_check="my_alphas",
        time_between_two_requests_to_server=300,
        whether_to_print_info=True,
        max_time_to_wait=1200
):
    """Полный процесс ожидания пока сервер не освободится"""
    assert isinstance(which_server_to_check, str), "variable 'which_server_to_check' is not str"
    assert isinstance(time_between_two_requests_to_server, int), "variable 'time_between_two_requests_to_server' is not int"
    assert isinstance(whether_to_print_info, bool), "variable 'whether_to_print_info' is not bool"
    assert isinstance(max_time_to_wait, int), "variable 'max_time_to_wait' is not int"
    #####

    path_to_my_alphas_server_condition_file = dict_path_to_server_file_by_server_name[which_server_to_check]
    if not os.path.exists(path_to_my_alphas_server_condition_file):
        return 1
    ##
    int_overall_seconds_waited = 0
    int_seconds_waited_when_last_time_printed_info = -1000
    bool_is_first_busy_mesage_printed = False
    while(True):
        if check_that_myalphas_server_is_free(
                time_to_make_new_request_to_myalphas_server=time_between_two_requests_to_server,
                which_server_to_check=which_server_to_check,
                whether_to_print_info=whether_to_print_info
        ):
            break

        if not bool_is_first_busy_mesage_printed:
            bool_is_first_busy_mesage_printed = True
            print(which_server_to_check + " SERVER is busy, seconds_waited=", flush=True)

        # Проверяем не истекло ли максимальное время ожидания
        if int_overall_seconds_waited > max_time_to_wait:
            print("\n" + which_server_to_check + " server didn't become free even after " + str(max_time_to_wait) + " seconds", flush=True)
            return 0
        if int_overall_seconds_waited - int_seconds_waited_when_last_time_printed_info > 20:
            print(str(int_overall_seconds_waited) + ",", end=" ", flush=True)
            int_seconds_waited_when_last_time_printed_info = int_overall_seconds_waited
        seconds_to_wait = randint(6, 20)
        sleep(seconds_to_wait)
        int_overall_seconds_waited += seconds_to_wait
        # int_seconds_waited_when_last_time_printed_info = int_overall_seconds_waited

    if whether_to_print_info:
        if int_overall_seconds_waited:
            print("\n" + which_server_to_check + " server READY in seconds: ", int_overall_seconds_waited, flush=True)
        else:
            print(which_server_to_check + " server READY", flush=True)
    return 1


def check_whether_submittor_is_working():
    """Проверяем работает ли сабмиттор"""
    time_to_make_new_request_to_server = 3600 * 24 * 7
    bool_result = check_that_myalphas_server_is_free(
        time_to_make_new_request_to_server,
        which_server_to_check="is_my_alphas_submittor_script_working_now",
        whether_to_print_info=False
    )
    return not bool_result


