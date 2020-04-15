import sys, os
from all_CONSTANTS import *
#####
import datetime   # Для получения врямя логина в вебсим
from working_with_files import get_list_of_fields_in_file
from working_with_files import append_one_item_to_list_in_file


def choose_type_of_server_with_list_results(server_where_to_add_item, int_days_delay=0):
    """Получаем имя файла куда сохранять или откуда загружать результаты, которые представляют из себя список каждый день"""
    assert isinstance(server_where_to_add_item, str), "variable 'server_where_to_add_item' is not str"
    assert isinstance(int_days_delay, int), "variable 'int_days_delay' is not int"
    #####
    datetime_date_for_given_delay = (datetime.datetime.today() - datetime.timedelta(hours=8) - datetime.timedelta(days=int_days_delay))
    path_to_folder_with_today_results = datetime_date_for_given_delay.strftime(path_to_folder_with_someday_results)
    if server_where_to_add_item == "correlation":
        path_to_file_with_list_results = path_to_folder_with_today_results + "list_times_in_which_correlation_were_generated.txt"
    elif server_where_to_add_item == "times_of_check_submission":
        path_to_file_with_list_results = path_to_folder_with_today_results + "list_times_in_which_check_submission_was_generated.txt"
    elif server_where_to_add_item == "times_of_submission_status":
        path_to_file_with_list_results = path_to_folder_with_today_results + "list_times_in_which_submission_status_was_generated.txt"
    elif server_where_to_add_item == "correlation_of_alphas_that_submitted":
        path_to_file_with_list_results = path_to_folder_with_today_results + "list_correlation_of_alphas_that_submitted.txt"

    elif server_where_to_add_item == "turnover_of_alphas_that_submitted":
        path_to_file_with_list_results = path_to_folder_with_today_results + "list_turnover_of_alphas_that_submitted.txt"

    elif server_where_to_add_item == "sharpe_of_alphas_that_submitted":
        path_to_file_with_list_results = path_to_folder_with_today_results + "list_sharpe_of_alphas_that_submitted.txt"
    elif server_where_to_add_item == "fitness_of_alphas_that_submitted":
        path_to_file_with_list_results = path_to_folder_with_today_results + "list_fitness_of_alphas_that_submitted.txt"
    else:
        print("Wrong type of server, where to add value to list:", server_where_to_add_item)
        sys.exit(2523)
    return path_to_file_with_list_results


def append_item_to_list_of_todays_results(item_to_add, server_where_to_add_item="correlation"):
    """Добавляем элементы к списку, в котором сохраняем результаты за сегодня"""
    assert isinstance(server_where_to_add_item, str), "variable 'server_where_to_add_item' is not str"
    #####
    path_to_file_with_list_results = choose_type_of_server_with_list_results(server_where_to_add_item, int_days_delay=0)
    append_one_item_to_list_in_file(path_to_file_with_list_results, item_to_add)
    return 1


def get_mean_of_list_of_todays_results(
        server_from_which_to_take_mean="correlation",
        int_days_delay=0,
        bool_is_to_filter_zeros=False
):
    """Получаем среднее значение, для какого либо сервера"""
    assert isinstance(server_from_which_to_take_mean, str), "variable 'server_from_which_to_take_mean' is not str"
    assert isinstance(int_days_delay, int), "variable 'int_days_delay' is not int"
    assert isinstance(bool_is_to_filter_zeros, bool), "variable 'bool_is_to_filter_zeros' is not bool"
    #####
    path_to_file_with_list_results = choose_type_of_server_with_list_results(server_from_which_to_take_mean, int_days_delay=int_days_delay)
    if not os.path.exists(path_to_file_with_list_results):
        # print("ERROR: file: ", path_to_file_with_list_results, " don't exist")
        return 0.0
    list_elements_which_to_mean = get_list_of_fields_in_file(path_to_file_with_list_results)
    if not list_elements_which_to_mean:
        return 0.0
    try:
        list_of_items_on_server_now = list(map(float, list_elements_which_to_mean))
        if bool_is_to_filter_zeros:
            list_of_items_on_server_now = [elem for elem in list_of_items_on_server_now if elem]
        if list_of_items_on_server_now:
            return round(sum(list_of_items_on_server_now) / len(list_of_items_on_server_now), 3)
        else:
            return 0.0
    except:
        print("ERROR: can't get mean time for server: ", server_from_which_to_take_mean, " For date with delay: ", int_days_delay)
        return 0.0


def get_list_of_element_of_someday_results_for_some_type_of_value(server_from_which_to_take_mean="correlation", int_days_delay=0):
    """"""
    assert isinstance(server_from_which_to_take_mean, str), "variable 'server_from_which_to_take_mean' is not str"
    assert isinstance(int_days_delay, int), "variable 'int_days_delay' is not int"
    #####
    path_to_file_with_list_results = choose_type_of_server_with_list_results(server_from_which_to_take_mean, int_days_delay=int_days_delay)
    return get_list_of_fields_in_file(path_to_file_with_list_results, whether_to_print_information=False)



