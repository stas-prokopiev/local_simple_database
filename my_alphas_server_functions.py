import sys, os
from all_CONSTANTS import *

import datetime   # Для получения врямя логина в вебсим
from working_with_files import check_that_folder_exist_otherwise_create
from working_with_files import get_list_of_files_in_folder
from working_with_files import winapi_path
from working_with_files import save_dict_to_txt_file
from working_with_files import load_dict_from_txt_file
from working_with_files import get_max_number_of_filename_in_given_folder
from working_with_files import save_int_to_file

from scripts_USEFULL_EVERYWHERE import check_with_assert_that_type_is_correct
from working_with_lists import sort_list_according_to_list_of_orders
from server_conditions import check_whether_submittor_is_working
from server_dicts_with_results import load_dict_with_results_from_server


def read_number_of_submited_alphas_for_all_types_as_dict(int_number_of_days_delay=0):
    """Считываем число сабмитов для всех типов в словарь"""
    assert isinstance(int_number_of_days_delay, int), "variable 'int_number_of_days_delay' is not int"
    #####
    path_to_folder = (
        datetime.datetime.today() - datetime.timedelta(hours=8) - datetime.timedelta(days=int_number_of_days_delay)
    ).strftime(path_to_folder_with_someday_results)
    path_to_folder_with_todays_submission_results = path_to_folder + "SUBMISSION_RESULTS/"
    check_that_folder_exist_otherwise_create(path_to_folder_with_todays_submission_results)
    # Все файлы в папке результатов за сегодня
    list_all_files_in_folder = get_list_of_files_in_folder(path_to_folder_with_todays_submission_results)
    # Выделяем все файлы, в которых записа информация о числе сабмитов
    list_all_files_with_number_of_submits = [file for file in list_all_files_in_folder if (os.path.basename(file).startswith("number_of_submitted_alphas_on"))]
    list_str_order_of_types = ["alone", "top20_", "top60_", "top200_", "top500_", "top3000_", "top100_", "top400_", "top1200_"]
    list_all_files_with_number_of_submits = sort_list_according_to_list_of_orders(list_all_files_with_number_of_submits, list_str_order_of_types)
    dict_number_of_submitted_alphas_by_type = {}
    for file_num, file_with_number_of_submits in enumerate(list_all_files_with_number_of_submits):
        dict_with_results = load_dict_from_txt_file(file_with_number_of_submits)
        name_of_type = (os.path.basename(file_with_number_of_submits)).replace("number_of_submitted_alphas_on_", "").replace(".txt", "")
        dict_number_of_submitted_alphas_by_type[name_of_type] = dict_with_results["overall"]
    return dict_number_of_submitted_alphas_by_type


def check_is_submittor_today_already_finished_work():
    """Функция проверяем, проработал ли сегодня уже сабмиттор"""
    dict_number_of_submitted_alphas_by_type = read_number_of_submited_alphas_for_all_types_as_dict(int_number_of_days_delay=0)
    if (not check_whether_submittor_is_working()) and (len(dict_number_of_submitted_alphas_by_type) > 3):
        return 1
    return 0


def print_number_of_submits_for_every_settings(int_max_alphas_to_submit_on_all_settings=700):
    """Функция для печати статистики о количестве сабмитов, на каждом сете настроек"""
    assert isinstance(int_max_alphas_to_submit_on_all_settings, int), "variable 'int_max_alphas_to_submit_on_all_settings' is not int"
    #####
    from dashboard import get_simulation_time_necessary_for_all_submission
    from dashboard import get_time_multiplier_because_of_loss_results
    from dashboard import get_average_time_of_simulation_for_different_types
    from dashboard import get_average_time_necessary_for_ONE_FULL_SUBMISSION
    path_to_folder = (datetime.datetime.today() - datetime.timedelta(hours=8)).strftime(path_to_folder_with_someday_results)
    check_that_folder_exist_otherwise_create(path_to_folder)
    # Достаем словарь с числом альф доступных для сабмита для всех настроек
    dict_numbers_of_alphas_ready_for_submission = load_dict_with_results_from_server("overall_alphas_ready_for_submission", is_to_get_only_overall_result=False)
    dict_number_of_submitted_alphas_by_type = read_number_of_submited_alphas_for_all_types_as_dict()
    #####
    # Достаем общий словарь сколько альф было попробованно, на данном типе
    int_overall_alphas_tried_today = 0
    dict_with_numbers_of_tried_alphas = load_dict_with_results_from_server(
        type_of_server_to_read_stats='tried_alphas_by_SUBMITTOR',
        is_to_get_only_overall_result=False
    )
    # Подготавливаем настройки что и как сабмитеть
    dict_with_settings_what_and_how_to_submit = load_dict_from_txt_file('dict_settings_what_to_submit_by_type.txt')
    dict_number_max_alphas_to_submit_by_type = {}
    for str_key in dict_with_settings_what_and_how_to_submit:
        dict_number_max_alphas_to_submit_by_type[str_key] = dict_with_settings_what_and_how_to_submit[str_key]["min_alphas_to_submit"]
    # Загружаем Время симмуляции по типам
    dict_time_to_get_FULL_SUMBISSION_by_type = get_average_time_necessary_for_ONE_FULL_SUBMISSION(int_number_of_days_to_average_submission_ratio_with_decay=10)
    dict_time_multipliers_because_of_loss_results = get_time_multiplier_because_of_loss_results()
    dict_with_average_time_of_simulation_ready = get_average_time_of_simulation_for_different_types()
    # Печатаем время симмулирования необходимое на все сабмиты
    int_seconds_of_simulation_to_all_submissions, int_alphas_considered_as_submitted = get_simulation_time_necessary_for_all_submission(
        dict_number_max_alphas_to_submit_by_type,
        dict_time_to_get_FULL_SUMBISSION_by_type,
        int_max_alphas_to_submit=int_max_alphas_to_submit_on_all_settings
    )
    float_already_spend_simulation_time = 0.0
    for str_type in dict_with_numbers_of_tried_alphas:
        if str_type.lower() == "overall":
            continue
        if (str_type in dict_with_average_time_of_simulation_ready) and (str_type in dict_time_multipliers_because_of_loss_results):
            float_already_spend_simulation_time += (
                dict_with_numbers_of_tried_alphas[str_type] *
                dict_with_average_time_of_simulation_ready[str_type] *
                dict_time_multipliers_because_of_loss_results[str_type]
            )
        else:
            print("?" * 150 + "\nfor: ", str_type, " can't find avg_simulation_time or multiplier_because_of_lost_results.\n" + "?" * 150)
    float_hours_necessary_to_all_submissions_today = round(int_seconds_of_simulation_to_all_submissions / 3600.0, 2)
    float_hours_already_spend_of_simulation_time_today = round(float_already_spend_simulation_time / 3600.0, 2)
    with open(path_to_AUTORUN_SUBMITTOR_script + "simulation_time_spend_by_submittor.txt", 'w') as file:
        file.write(str(float_hours_already_spend_of_simulation_time_today))
    print(
        "For submitting today:", int_alphas_considered_as_submitted,
        " necessary simulation time: ", float_hours_necessary_to_all_submissions_today,
        "H. Already spend: ", float_hours_already_spend_of_simulation_time_today, "H."
    )

    #####
    # Высчитываем суммарные результаты, для словарей, которые выводятся
    if dict_number_of_submitted_alphas_by_type.values():
        dict_number_of_submitted_alphas_by_type.pop('overall', 0)
        dict_numbers_of_alphas_ready_for_submission.pop('overall', 0)
        dict_number_of_submitted_alphas_by_type["overall"] = sum(dict_number_of_submitted_alphas_by_type.values())
        dict_numbers_of_alphas_ready_for_submission["overall"] = sum(dict_numbers_of_alphas_ready_for_submission.values())
    else:
        dict_number_of_submitted_alphas_by_type["overall"] = 0
        dict_numbers_of_alphas_ready_for_submission["overall"] = 0

    dict_number_max_alphas_to_submit_by_type["overall"] = int_max_alphas_to_submit_on_all_settings
    dict_time_to_get_FULL_SUMBISSION_by_type["overall"] = round(int_seconds_of_simulation_to_all_submissions / int_max_alphas_to_submit_on_all_settings, 3)

    #####
    list_of_dict_of_table_rows = []
    # Достаем словарь результатов из каждого из файлов и печатаем общий результат
    for type_number, (name_of_type, number_of_submitted_alphas) in enumerate(dict_number_of_submitted_alphas_by_type.items()):
        str1 = str(type_number) + ") " + str(name_of_type) + "  "

        if name_of_type in dict_with_numbers_of_tried_alphas:
            str2 = "TRIED: " + str(dict_with_numbers_of_tried_alphas[name_of_type]) + "  "
            int_overall_alphas_tried_today += int(dict_with_numbers_of_tried_alphas[name_of_type])
        else:
            str2 = "TRIED: UNKNOWN:  "
        str3 = "SUBMITTED: " + str(number_of_submitted_alphas)
        # Добавляем информацию о том, сколько альф такого типа сабмитеть
        if name_of_type in dict_number_max_alphas_to_submit_by_type:
            str3 += " (max:" + str(dict_number_max_alphas_to_submit_by_type[name_of_type])
        else:
            str3 += " (max:LOST "
        # Добавляем информацию, сколько времени нужно на один сабмит для данного типа
        if name_of_type in dict_time_to_get_FULL_SUMBISSION_by_type:
            str3 += " SIMtime:" + str(dict_time_to_get_FULL_SUMBISSION_by_type[name_of_type]) + "S"
        else:
            str3 += " SIMtime:LOST"
        str3 += ")"
        if name_of_type in dict_numbers_of_alphas_ready_for_submission:
            str4 = " AVALIABLE to try: " + str(dict_numbers_of_alphas_ready_for_submission[name_of_type])
        else:
            str4 = "no information about avaliable number of alphas for:" + str(name_of_type)
        str_full_string = '{:<70}  {:<16}  {:<40}  {:<24}'.format(str1, str2, str3, str4)
        if type_number % 2:
            str_full_string = "   " + str_full_string
        print(str_full_string)
        list_of_dict_of_table_rows.append({"Type": str1, "Tried": str2, "Submitted": str3, "Avaliable": str4})
    # print("Overall:")
    # print("TRIED: ", int_overall_alphas_tried_today, "  SUBMITTED: ", load_dict_with_results_from_server("number_of_submits_done_on_all_settings"))
    #####
    msg_to_print = ""
    msg_to_print += "Resaved because:\n"
    msg_to_print += "-->Improve_sharpe: " + str(load_dict_with_results_from_server("improve_sharpe_alphas_added_to_combine_and_resimulate")) + "\n"
    msg_to_print += "-->Weight_failed: " + str(load_dict_with_results_from_server("weight_failed_alphas_added_to_filter_and_resimulate")) + "\n"
    msg_to_print += "-->Subuniverse_failed: " + str(load_dict_with_results_from_server("subuniverse_failed_alphas_added_to_combine_and_resimulate")) + "\n"
    msg_to_print += "-->To_high_selfcorr_so_to_modify: " + str(load_dict_with_results_from_server("new_alphas_for_modification_to_discorrelate_appened")) + "\n"
    msg_to_print += "-->Can't get selfcorr, so *1.0: " + str(load_dict_with_results_from_server("alphas_added_to_resimulate")) + "\n"
    print(msg_to_print)
    #####
    return 1


def get_path_to_folder_with_results(str_type_of_result="new_top500_industry_alphas"):
    """Получаем путь к папке с результатами"""
    check_with_assert_that_type_is_correct(str_type_of_result, str)
    #####
    if str_type_of_result == "new_top500_industry_alphas":
        str_path_to_folder_with_results = path_to_LAST_RESULTS_of_NEW_alphas_for_combining
    elif str_type_of_result == "submitted_alphas_results":
        str_path_to_folder_with_results = path_to_results_of_SUBMITTED_alphas
    # elif str_type_of_result == "new_top500_industry_WEIGHT_FAILED_alphas":
    #     str_path_to_folder_with_results = path_to_LAST_RESULTS_of_NEW_alphas_WEIGHT_FAILED
    else:
        print("ERROR: Unknown type of results: ", str_type_of_result)
        sys.exit(1712)
    return str_path_to_folder_with_results


def get_number_for_next_result(str_type_of_result="new_top500_industry_alphas"):
    """Получаем номер, под которым нужно добавить новую альфу к ПОСЛЕДНИМ РЕЗУЛЬТАТАМ"""
    check_with_assert_that_type_is_correct(str_type_of_result, str)
    #####
    """Получаем путь к папке с результатами"""
    str_path_to_folder_with_results = get_path_to_folder_with_results(str_type_of_result=str_type_of_result)
    str_path_to_file_with_last_max_result_number = str_path_to_folder_with_results + "int_last_result_number.txt"
    #####
    # Проверяем что файл уже создан сегодня и там есть хоть что-то, иначе создаем
    if not os.path.isfile(winapi_path(str_path_to_file_with_last_max_result_number)):
        save_int_to_file(str_path_to_file_with_last_max_result_number, 0)
        return 1
    with open(winapi_path(str_path_to_file_with_last_max_result_number), 'r') as f:
        content = f.read()
        # Проверяем, что возвращаем число, а не что-то другое
        if content.isdigit():
            return int(content) + 1
        else:
            print("Can't find number of last result for: ", str_type_of_result)
            print("content of file with number is: ", content)
            return get_max_number_of_filename_in_given_folder(str_path_to_folder_with_results) + 1


def delete_too_old_results(int_max_number_of_file_to_try_to_delete, str_type_of_result="new_top500_industry_alphas"):
    """Удаляем слишком старые результаты, чтобы корреляция считалась за разумное время"""

    check_with_assert_that_type_is_correct(int_max_number_of_file_to_try_to_delete, int)
    check_with_assert_that_type_is_correct(str_type_of_result, str)
    #####
    """Получаем путь к папке с результатами"""
    str_path_to_folder_with_results = get_path_to_folder_with_results(str_type_of_result=str_type_of_result)
    #####
    print("_" * 150)
    print("Deleting too old results for: ", str_type_of_result)
    int_files_deleted = 0
    list_all_files_with_results_in_folder = (
        get_list_of_files_in_folder(
            folder_where_to_look=str_path_to_folder_with_results,
            extension=".txt",
            not_consider_files_with_such_string_in_basename="int_last_NEW_alpha_number"
        )
    )
    print("In folder which files consider for deleting found results: ", len(list_all_files_with_results_in_folder))
    list_filenames_of_all_files_to_delete = [
        os.path.basename(str_full_file_path).replace(".txt", "")
        for str_full_file_path in list_all_files_with_results_in_folder
    ]
    for int_alpha_number in range(1, int_max_number_of_file_to_try_to_delete):
        if str(int_alpha_number) in list_filenames_of_all_files_to_delete:
            os.remove(str_path_to_folder_with_results + str(int_alpha_number) + ".txt")
            int_files_deleted += 1
    print("Old files with results deleted: ", int_files_deleted)
    print("_" * 150)


def download_all_last_results(
        int_last_alpha_results_to_get=999999,
        str_type_of_result="new_top500_industry_alphas",
        bool_is_to_delete_too_old_results=True
):
    """Загружаем результаты всех new top500 industry альф в специальные словари"""
    check_with_assert_that_type_is_correct(int_last_alpha_results_to_get, int)
    check_with_assert_that_type_is_correct(str_type_of_result, str)
    check_with_assert_that_type_is_correct(bool_is_to_delete_too_old_results, bool)
    #####
    """Получаем путь к папке с результатами"""
    str_path_to_folder_with_results = get_path_to_folder_with_results(str_type_of_result=str_type_of_result)
    #####
    print("=" * 150)
    print("download_all_last_results_for: ", str_type_of_result)
    dict_returns_of_last_alphas = {}
    dict_sharpe_of_last_alphas = {}
    int_alphas_lost_because_of_missed_file_with_results = 0
    ##
    int_number_for_last_new_alpha = get_number_for_next_result(str_type_of_result=str_type_of_result) - 1
    int_min_number_of_file_to_got = max(0, int_number_for_last_new_alpha - int_last_alpha_results_to_get)
    #####
    # Удаляем слишком старые результаты
    if int_min_number_of_file_to_got > 0 and bool_is_to_delete_too_old_results:
        delete_too_old_results(int_min_number_of_file_to_got, str_type_of_result=str_type_of_result)
        # delete_too_old_results(int_min_number_of_file_to_got)
    #####
    for int_file_number in range(int_min_number_of_file_to_got, int_number_for_last_new_alpha, 1):
        str_path_to_file_with_current_alpha_results = str_path_to_folder_with_results + str(int_file_number) + ".txt"
        if os.path.exists(str_path_to_file_with_current_alpha_results):
            dict_results_of_current_alpha = load_dict_from_txt_file(str_path_to_file_with_current_alpha_results)
            dict_returns_of_last_alphas[int_file_number] = dict_results_of_current_alpha["dict_with_returns_of_alpha"]
            dict_sharpe_of_last_alphas[int_file_number] = dict_results_of_current_alpha["float_average_sharpe_of_alpha"]
        else:
            int_alphas_lost_because_of_missed_file_with_results += 1
    if int_alphas_lost_because_of_missed_file_with_results:
        print("WARNING: int_alphas_lost_because_of_missed_file_with_results: ", int_alphas_lost_because_of_missed_file_with_results)
    print("Found results for ", str_type_of_result, " alphas: ", len(dict_returns_of_last_alphas))
    print("=" * 150)
    return dict_returns_of_last_alphas, dict_sharpe_of_last_alphas


def add_new_alpha_to_results(
        str_alpha_code,
        dict_with_returns_of_alpha,
        float_average_sharpe_of_alpha,
        str_type_of_result="new_top500_industry_alphas"
):
    """Добавляем альфу, к последним альфам, с которыми потом проверяем результаты"""
    check_with_assert_that_type_is_correct(str_alpha_code, str)
    check_with_assert_that_type_is_correct(dict_with_returns_of_alpha, dict)
    check_with_assert_that_type_is_correct(float_average_sharpe_of_alpha, float)
    check_with_assert_that_type_is_correct(str_type_of_result, str)
    #####
    """Получаем путь к папке с результатами"""
    str_path_to_folder_with_results = get_path_to_folder_with_results(str_type_of_result=str_type_of_result)
    #####
    int_number_for_new_alpha = get_number_for_next_result(str_type_of_result=str_type_of_result)
    str_path_to_dict_where_to_save_alpha_results = str_path_to_folder_with_results + str(int_number_for_new_alpha) + ".txt"
    dict_results_of_alpha_to_save = {"float_average_sharpe_of_alpha": float_average_sharpe_of_alpha, "dict_with_returns_of_alpha": dict_with_returns_of_alpha}
    save_dict_to_txt_file(dict_results_of_alpha_to_save, path_to_file=str_path_to_dict_where_to_save_alpha_results)
    save_int_to_file(str_path_to_folder_with_results + "int_last_result_number.txt", int_number_for_new_alpha)
    return int_number_for_new_alpha



