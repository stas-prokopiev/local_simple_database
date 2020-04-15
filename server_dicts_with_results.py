import sys, os
from all_CONSTANTS import *
#####
import time  # time.time() для получения количества секунд, которые прошли с 1970 года
import datetime   # Для получения врямя логина в вебсим
from working_with_files import check_that_folder_exist_otherwise_create
from working_with_files import get_list_of_files_in_folder
from working_with_files import save_dict_to_txt_file
from working_with_files import load_dict_from_txt_file
from collections import defaultdict

list_of_avaliable_additional_names = ["from_my_myalphas_submittable_alone", "combinations_from_prod_decm"]


def save_dict_with_results_to_server(dict_numbers_of_alphas, type_of_server_to_read_stats='top500', int_days_of_delay=0):
    """Функция сохраняет в файл сколько альф засабмичено сегодня"""
    assert isinstance(dict_numbers_of_alphas, dict), "variable 'dict_numbers_of_alphas' is not dict"
    assert isinstance(type_of_server_to_read_stats, str), "variable 'type_of_server_to_read_stats' is not str"
    assert isinstance(int_days_of_delay, int), "variable 'int_days_of_delay' is not int"
    #####

    # path_to_folder_with_today_results = (datetime.datetime.today() - datetime.timedelta(hours = 8)).strftime(path_to_folder_with_someday_results)
    path_to_folder_with_today_results = (
        datetime.datetime.today() - datetime.timedelta(hours=8) - datetime.timedelta(days=int_days_of_delay)
    ).strftime(path_to_folder_with_someday_results)
    path_to_folder_with_todays_submission_results = path_to_folder_with_today_results + "SUBMISSION_RESULTS/"
    path_to_folder_with_todays_ERRORS_results = path_to_folder_with_today_results + "ERRORS_RESULTS/"
    check_that_folder_exist_otherwise_create(path_to_folder_with_today_results)
    check_that_folder_exist_otherwise_create(path_to_folder_with_todays_submission_results)
    check_that_folder_exist_otherwise_create(path_to_folder_with_todays_ERRORS_results)
    check_that_folder_exist_otherwise_create(path_to_folder_with_todays_scripts_statistics)
    #####
    # Выбираем имя для файла  на определенном типе альф
    if ((type_of_server_to_read_stats.lower().startswith("top")) or (type_of_server_to_read_stats.lower() in list_of_avaliable_additional_names)):
        str_path_to_file_where_to_save_some_results = (
            path_to_folder_with_todays_submission_results +
            "number_of_submitted_alphas_on_" +
            type_of_server_to_read_stats + ".txt"
        )
    # работаем с числом сабмитов ВЕЗДЕ
    elif (type_of_server_to_read_stats == "number_of_submits_done_on_all_settings"):
        str_path_to_file_where_to_save_some_results = path_to_folder_with_todays_submission_results + "number_of_submits_made_per_day.txt"
    # работаем с числом сабмитов по РЕГИОНУ
    elif (type_of_server_to_read_stats == "number_of_submits_done_by_region"):
        str_path_to_file_where_to_save_some_results = path_to_folder_with_todays_submission_results + "dict_number_of_submits_done_by_region.txt"

    #####
    # Работаем с файлам с числом ошибок сегодня
    elif (type_of_server_to_read_stats == "my_alphas_robot_errors"):
        str_path_to_file_where_to_save_some_results = path_to_folder_with_todays_ERRORS_results + "dict_number_of_my_alphas_robot_errors_by_script_type.txt"
    elif (type_of_server_to_read_stats == "fastest_simulator_errors"):
        str_path_to_file_where_to_save_some_results = path_to_folder_with_todays_ERRORS_results + "dict_number_of_fastest_simulator_errors_by_script_type.txt"
    #####

    # работаем с числом альф обработанных my_alphas robot для каждых из настроек
    elif (type_of_server_to_read_stats == "tried_alphas_by_SUBMITTOR"):
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "dict_tried_alphas_by_different_SUBMITTOR_types.txt"
    # работаем с числом логинов за сегодня
    elif type_of_server_to_read_stats == "number_of_logins":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "number_of_logins_made_per_day.txt"
    # работаем с числом симмуляций за день
    elif type_of_server_to_read_stats == "overall_alphas_simulated":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "number_of_simulations_today.txt"
    # работаем с числом сгенерированных корреляцией сегодня
    elif type_of_server_to_read_stats == "correlation_results":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "number_of_generated_correlations_today.txt"
    # работаем с числом check submissions
    elif type_of_server_to_read_stats == "check_submission_results":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "number_of_check_submissions_today.txt"
    # работаем с числом сгенерированных submissions
    elif type_of_server_to_read_stats == "submission_results":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "number_of_submission_results_got_today.txt"
    # работаем с числом обработанных альф с помощью my_alphas_robot
    elif type_of_server_to_read_stats == "my_alphas_robot_results":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "my_alphas_robot_statistics_today.txt"
    #####
    # работаем с числом доступных альф для попытки сабмита
    elif type_of_server_to_read_stats == "overall_alphas_ready_for_submission":
        str_path_to_file_where_to_save_some_results = path_start_for_every_script + "alphas_ready_for_submission_for_every_type_flows.txt"
    elif type_of_server_to_read_stats == "overall_alphas_ready_for_submission_flows":
        str_path_to_file_where_to_save_some_results = path_start_for_every_script + "alphas_ready_for_submission_for_every_type_flows.txt"
    # работаем с числом доступных результатов для работы retriever for my_myalphas
    elif type_of_server_to_read_stats == "results_ready_for_retrieving_for_my_myalphas":
        str_path_to_file_where_to_save_some_results = path_start_for_every_script + "results_ready_for_retrieving_for_my_myalphas.txt"

    # Работаем с числом результатов полученные для первых альф для шаблонов
    elif type_of_server_to_read_stats == "first_template_alphas_ready_for_retrieving":
        str_path_to_file_where_to_save_some_results = path_to_TEMPLATES_first_codes_parent_folder + "dict_first_template_alphas_ready_for_retrieving.txt"

    # Работаем с числом результатов полученные альф == EXPR value
    elif type_of_server_to_read_stats == "new_EXPRs_results":
        str_path_to_file_where_to_save_some_results = path_to_dict_exprs_results_statistic

    # работаем с числом доступных подальф для симмулирования, для получения результатов в my_myalphas
    elif type_of_server_to_read_stats == "subalphas_created_to_simulate_and_then_retrieve":
        str_path_to_file_where_to_save_some_results = path_start_for_every_script + "subalphas_created_to_simulate_and_then_retrieve.txt"
    # работаем с числом доступных альф для попытки сабмита
    elif type_of_server_to_read_stats == "average_time_of_one_result_for_dif_types":
        str_path_to_file_where_to_save_some_results = path_start_for_every_script + "dict_average_time_of_one_result_for_dif_types.txt"
    #####
    # работаем с числом альф для модифицирования
    elif type_of_server_to_read_stats == "new_alphas_for_modification_to_discorrelate_appened":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "dict_new_alphas_for_modification_appened_for_dif_types.txt"
    # работаем с числом альф weight failed_ для фильтрации и рессимулирования
    elif type_of_server_to_read_stats == "weight_failed_alphas_added_to_filter_and_resimulate":
        str_path_to_file_where_to_save_some_results = (
            path_to_folder_with_today_results +
            "dict_weight_failed_alphas_added_to_filter_and_resimulate_by_types.txt"
        )
    # работаем с числом альф weight failed_ для фильтрации и рессимулирования
    elif type_of_server_to_read_stats == "improve_sharpe_alphas_added_to_combine_and_resimulate":
        str_path_to_file_where_to_save_some_results = (
            path_to_folder_with_today_results +
            "dict_improve_sharpe_alphas_added_to_combine_and_resimulate_by_types.txt"
        )
    # работаем с числом альф weight failed_ для фильтрации и рессимулирования
    elif type_of_server_to_read_stats == "subuniverse_failed_alphas_added_to_combine_and_resimulate":
        str_path_to_file_where_to_save_some_results = (
            path_to_folder_with_today_results +
            "dict_subuniverse_failed_alphas_added_to_combine_and_resimulate_by_types.txt"
        )
    # работаем с числом альф для умножения на 1.0 и рессимулирования
    elif type_of_server_to_read_stats == "alphas_added_to_resimulate":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "dict_alphas_added_to_resimulate_for_dif_types.txt"
    #####
    elif type_of_server_to_read_stats == "pnls_saved_and_by_whom":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "dict_PNLS_saved_and_by_whom.txt"
    elif type_of_server_to_read_stats == "errors_in_saving_pnls_happened":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "dict_errors_in_saving_PNLS_happened.txt"
    #####
    # сохраняем, сколько корреляций было нажато различными скриптами
    elif type_of_server_to_read_stats == "correlation_button_pushed_by_diff_types_of_scripts":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "dict_correlation_button_pushed_by_type_of_scripts.txt"
    # работаем с статистиками всех величин для различных скриптов
    elif "statistic" in type_of_server_to_read_stats:
        str_path_to_file_where_to_save_some_results = path_to_folder_with_todays_scripts_statistics + type_of_server_to_read_stats + ".txt"
        # Проверяем не нужно ли удалить старые ститистики. (Делаем это в понедельник в 2 часа (Диверисификация))
        if (datetime.datetime.today().weekday() % 2 == 1):
            if (datetime.datetime.today().hour == 9 or datetime.datetime.today().hour == 22):
                list_file_paths_to_all_files_with_scripts_statistics = (
                    get_list_of_files_in_folder(
                        folder_where_to_look=path_to_folder_with_todays_scripts_statistics,
                        extension=".txt"
                    )
                )
                #####
                for str_full_path_to_file in list_file_paths_to_all_files_with_scripts_statistics:
                    str_filename_of_file_with_statistic = os.path.basename(str_full_path_to_file)
                    time_when_file_created = int(str_filename_of_file_with_statistic.replace(".txt", "").split("_")[-1])
                    # Удаляем статистики, которым более 2 дней
                    if int(time.time()) - time_when_file_created > 3600 * 24 * 2:
                        try:
                            os.remove(str_full_path_to_file)
                            print("STATISTIC WAS REMOVED: ", os.path.relpath(str_full_path_to_file))
                        except FileNotFoundError:
                            print("?" * 150)
                            print("ERROR: Unable to delete file: ", str_full_path_to_file)
                            print("Because can't find it")
                            print("?" * 150)
                #####
    else:
        print("Wrong type of request in 'save_dict_with_results_to_server': ", type_of_server_to_read_stats)
        sys.exit(6263)
    save_dict_to_txt_file(dict_numbers_of_alphas, path_to_file=str_path_to_file_where_to_save_some_results)
    return 1


def load_dict_with_results_from_server(
        type_of_server_to_read_stats='top500',
        is_to_get_only_overall_result=True,
        whether_to_get_yesterday_results=False,
        int_days_of_delay=0
):
    """Считываем сколько альф уже засабмичено сегодня"""
    assert isinstance(type_of_server_to_read_stats, str), "variable 'type_of_server_to_read_stats' is not str"
    assert isinstance(is_to_get_only_overall_result, bool), "variable 'is_to_get_only_overall_result' is not bool"
    assert isinstance(whether_to_get_yesterday_results, bool), "variable 'whether_to_get_yesterday_results' is not bool"
    assert isinstance(int_days_of_delay, int), "variable 'int_days_of_delay' is not int"
    #####
    # Если нужны результаты за вчера (нужно для my_alphas robots)
    if whether_to_get_yesterday_results:
        int_days_of_delay += 1
    #####
    path_to_folder_with_today_results = (
        datetime.datetime.today() - datetime.timedelta(hours=8) - datetime.timedelta(days=int_days_of_delay)
    ).strftime(path_to_folder_with_someday_results)
    path_to_folder_with_todays_submission_results = path_to_folder_with_today_results + "SUBMISSION_RESULTS/"
    path_to_folder_with_todays_ERRORS_results = path_to_folder_with_today_results + "ERRORS_RESULTS/"
    check_that_folder_exist_otherwise_create(path_to_folder_with_today_results)
    check_that_folder_exist_otherwise_create(path_to_folder_with_todays_submission_results)
    check_that_folder_exist_otherwise_create(path_to_folder_with_todays_ERRORS_results)
    check_that_folder_exist_otherwise_create(path_to_folder_with_todays_scripts_statistics)

    #####
    # работаем с числом сабмитов на определенном типе альф
    if ((type_of_server_to_read_stats.lower().startswith("top")) or (type_of_server_to_read_stats.lower() in list_of_avaliable_additional_names)):
        str_path_to_file_where_to_save_some_results = (
            path_to_folder_with_todays_submission_results +
            "number_of_submitted_alphas_on_" +
            type_of_server_to_read_stats + ".txt"
        )
        dict_empty_for_saving_results = {"already found as submitted": 0, "submitted by pushing submit button": 0, "overall": 0}
    # работаем с числом сабмитов ВЕЗДЕ
    elif (type_of_server_to_read_stats == "number_of_submits_done_on_all_settings"):
        str_path_to_file_where_to_save_some_results = path_to_folder_with_todays_submission_results + "number_of_submits_made_per_day.txt"
        dict_empty_for_saving_results = {"already found as submitted": 0, "submitted by pushing submit button": 0, "overall": 0}
    # работаем с числом сабмитов по РЕГИОНУ
    elif (type_of_server_to_read_stats == "number_of_submits_done_by_region"):
        str_path_to_file_where_to_save_some_results = path_to_folder_with_todays_submission_results + "dict_number_of_submits_done_by_region.txt"
        dict_empty_for_saving_results = {"USA": 0, "EUR": 0, "ASI": 0, "overall": 0}
    #####
    # Работаем с файлам с числом ошибок сегодня
    elif (type_of_server_to_read_stats == "my_alphas_robot_errors"):
        str_path_to_file_where_to_save_some_results = path_to_folder_with_todays_ERRORS_results + "dict_number_of_my_alphas_robot_errors_by_script_type.txt"
        dict_empty_for_saving_results = {"overall": 0}
    elif (type_of_server_to_read_stats == "fastest_simulator_errors"):
        str_path_to_file_where_to_save_some_results = path_to_folder_with_todays_ERRORS_results + "dict_number_of_fastest_simulator_errors_by_script_type.txt"
        dict_empty_for_saving_results = {"overall": 0}
    #####
    # работаем с числом альф обработанных my_alphas robot для каждых из настроек
    elif (type_of_server_to_read_stats == "tried_alphas_by_SUBMITTOR"):
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "dict_tried_alphas_by_different_SUBMITTOR_types.txt"
        dict_empty_for_saving_results = {"overall": 0}
    # работаем с числом логинов за сегодня
    elif type_of_server_to_read_stats == "number_of_logins":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "number_of_logins_made_per_day.txt"
        dict_empty_for_saving_results = {"number_of_logins": 0, "overall": 0}
    # работаем с числом симмуляций за день
    elif type_of_server_to_read_stats == "overall_alphas_simulated":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "number_of_simulations_today.txt"
        dict_empty_for_saving_results = {"overall_results_got": 0, "overall_timed_outs": 0, "overall": 0}
    # работаем с числом сгенерированных корреляцией сегодня
    elif type_of_server_to_read_stats == "correlation_results":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "number_of_generated_correlations_today.txt"
        dict_empty_for_saving_results = {
            "correlations_button_pushed": 0,
            "correlations_were_generated": 0,
            "correlation_was_to_high": 0,
            "correlations_werent_generated": 0,
            "overall": 0
        }
    # работаем с числом check submissions
    elif type_of_server_to_read_stats == "check_submission_results":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "number_of_check_submissions_today.txt"
        dict_empty_for_saving_results = {
            "check_submissions_button_pushed": 0,
            "reached_the_limit": 0,
            "check_submissions_were_generated": 0,
            "check_submissions_werent_generated": 0,
            "overall": 0
        }
    # работаем с числом сгенерированных submissions
    elif type_of_server_to_read_stats == "submission_results":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "number_of_submission_results_got_today.txt"
        dict_empty_for_saving_results = {
            "submissions_started": 0, "reached_the_limit": 0, "SUBMITTED": 0, "submit_button_pushed_times": 0,
            "submissions_werent_generated": 0, "submissions_werent_generated_after_all_itterations": 0, "overall": 0
        }
    # работаем с числом обработанных альф с помощью my_alphas_robot
    elif type_of_server_to_read_stats == "my_alphas_robot_results":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "my_alphas_robot_statistics_today.txt"
        dict_empty_for_saving_results = {
            "alphas_processed_by_submittor": 0,
            "alphas_processed_by_retrieving_results": 0,
            "alphas_processed_by_saving_new_alphas": 0,
            "alphas_processed_by_resave_negative_alphas": 0,
            "overall": 0
        }
    #####
    # работаем с числом доступных альф для попытки сабмита
    elif type_of_server_to_read_stats == "overall_alphas_ready_for_submission":
        # str_path_to_file_where_to_save_some_results = path_start_for_every_script + "alphas_ready_for_submission_for_every_Universe.txt"
        str_path_to_file_where_to_save_some_results = path_start_for_every_script + "alphas_ready_for_submission_for_every_type_flows.txt"
        dict_empty_for_saving_results = {"overall": 0}
    elif type_of_server_to_read_stats == "overall_alphas_ready_for_submission_flows":
        str_path_to_file_where_to_save_some_results = path_start_for_every_script + "alphas_ready_for_submission_for_every_type_flows.txt"
        dict_empty_for_saving_results = {"overall": 0}
    # работаем с числом доступных результатов для работы retriever for my_myalphas
    elif type_of_server_to_read_stats == "results_ready_for_retrieving_for_my_myalphas":
        str_path_to_file_where_to_save_some_results = path_start_for_every_script + "results_ready_for_retrieving_for_my_myalphas.txt"
        dict_empty_for_saving_results = {"overall": 0}
    # Работаем с числом результатов полученные для первых альф для шаблонов
    elif type_of_server_to_read_stats == "first_template_alphas_ready_for_retrieving":
        str_path_to_file_where_to_save_some_results = path_to_TEMPLATES_first_codes_parent_folder + "dict_first_template_alphas_ready_for_retrieving.txt"
        dict_empty_for_saving_results = {"overall": 0}

    # Работаем с числом результатов полученные альф == EXPR value
    elif type_of_server_to_read_stats == "new_EXPRs_results":
        str_path_to_file_where_to_save_some_results = path_to_dict_exprs_results_statistic

    # работаем с числом доступных подальф для симмулирования, для получения результатов в my_myalphas
    elif type_of_server_to_read_stats == "subalphas_created_to_simulate_and_then_retrieve":
        str_path_to_file_where_to_save_some_results = path_start_for_every_script + "subalphas_created_to_simulate_and_then_retrieve.txt"
        dict_empty_for_saving_results = {"overall": 0}
    # работаем с числом доступных альф для попытки сабмита
    elif type_of_server_to_read_stats == "average_time_of_one_result_for_dif_types":
        str_path_to_file_where_to_save_some_results = path_start_for_every_script + "dict_average_time_of_one_result_for_dif_types.txt"
        dict_empty_for_saving_results = {"overall": 0}
    #####
    # работаем с числом альф для модифицирования
    elif type_of_server_to_read_stats == "new_alphas_for_modification_to_discorrelate_appened":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "dict_new_alphas_for_modification_appened_for_dif_types.txt"
        dict_empty_for_saving_results = {"overall": 0}
    # работаем с числом альф weight failed_ для фильтрации и рессимулирования
    elif type_of_server_to_read_stats == "weight_failed_alphas_added_to_filter_and_resimulate":
        str_path_to_file_where_to_save_some_results = (
            path_to_folder_with_today_results +
            "dict_weight_failed_alphas_added_to_filter_and_resimulate_by_types.txt"
        )
        dict_empty_for_saving_results = {"overall": 0}
    # работаем с числом альф weight failed_ для фильтрации и рессимулирования
    elif type_of_server_to_read_stats == "improve_sharpe_alphas_added_to_combine_and_resimulate":
        str_path_to_file_where_to_save_some_results = (
            path_to_folder_with_today_results +
            "dict_improve_sharpe_alphas_added_to_combine_and_resimulate_by_types.txt"
        )
        dict_empty_for_saving_results = {"overall": 0}
    # работаем с числом альф weight failed_ для фильтрации и рессимулирования
    elif type_of_server_to_read_stats == "subuniverse_failed_alphas_added_to_combine_and_resimulate":
        str_path_to_file_where_to_save_some_results = (
            path_to_folder_with_today_results +
            "dict_subuniverse_failed_alphas_added_to_combine_and_resimulate_by_types.txt"
        )
        dict_empty_for_saving_results = {"overall": 0}
    # работаем с числом альф для умножения на 1.0 и рессимулирования
    elif type_of_server_to_read_stats == "alphas_added_to_resimulate":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "dict_alphas_added_to_resimulate_for_dif_types.txt"
        dict_empty_for_saving_results = {"overall": 0}
    #####
    elif type_of_server_to_read_stats == "pnls_saved_and_by_whom":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "dict_PNLS_saved_and_by_whom.txt"
        dict_empty_for_saving_results = {"overall": 0}
    elif type_of_server_to_read_stats == "errors_in_saving_pnls_happened":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "dict_errors_in_saving_PNLS_happened.txt"
        dict_empty_for_saving_results = {"overall": 0}
    # сохраняем, сколько корреляций было нажато различными скриптами
    elif type_of_server_to_read_stats == "correlation_button_pushed_by_diff_types_of_scripts":
        str_path_to_file_where_to_save_some_results = path_to_folder_with_today_results + "dict_correlation_button_pushed_by_type_of_scripts.txt"
        dict_empty_for_saving_results = {"overall": 0}
    # работаем с статистиками всех величин для различных скриптов
    elif "statistic" in type_of_server_to_read_stats:
        str_path_to_file_where_to_save_some_results = path_to_folder_with_todays_scripts_statistics + type_of_server_to_read_stats + ".txt"
        dict_empty_for_saving_results = {"overall": 0}
    else:
        print("Wrong type of request in 'load_dict_with_results_from_server': ", type_of_server_to_read_stats)
        sys.exit(6263)
    #####
    # Если файла такого сервера еще нет, то возвращаем пустой словарь
    if not os.path.exists(str_path_to_file_where_to_save_some_results):
        print(
            "For server: ", type_of_server_to_read_stats,
            " were created empty file-dictionary: ",
            os.path.relpath(str_path_to_file_where_to_save_some_results)
        )
        save_dict_with_results_to_server(dict_empty_for_saving_results, type_of_server_to_read_stats, int_days_of_delay=int_days_of_delay)
        if is_to_get_only_overall_result:
            return 0
        else:
            return {}
    # Файл есть, считываем из него информацию
    dict_numbers_of_alphas = load_dict_from_txt_file(str_path_to_file_where_to_save_some_results)
    if is_to_get_only_overall_result:
        if "overall" in dict_numbers_of_alphas:
            return int(dict_numbers_of_alphas["overall"])
        else:
            return 0
    else:
        return dict_numbers_of_alphas


def increase_by_N_result_on_dict_server(str_type_of_server_to_read_dict_with_stats, str_key_to_increase, int_number_by_which_to_increase):
    """Функция для увеличения числа засабмиченных альф на N"""

    assert isinstance(str_type_of_server_to_read_dict_with_stats, str), "variable 'str_type_of_server_to_read_dict_with_stats' is not str"
    assert isinstance(str_key_to_increase, str), "variable 'str_key_to_increase' is not str"
    assert isinstance(int_number_by_which_to_increase, int), "variable 'int_number_by_which_to_increase' is not int"
    #####
    defaultdict_already_submitted = defaultdict(
        int,
        load_dict_with_results_from_server(
            str_type_of_server_to_read_dict_with_stats,
            is_to_get_only_overall_result=False
        )
    )
    defaultdict_already_submitted[str_key_to_increase] += int_number_by_which_to_increase
    defaultdict_already_submitted["overall"] += int_number_by_which_to_increase
    save_dict_with_results_to_server(dict(defaultdict_already_submitted), str_type_of_server_to_read_dict_with_stats)
    return 1


def write_value_by_type_to_dict_server(type_of_server_to_write, type_of_value_to_set, value_to_set):
    """Устанавливаем значение определенного типа, для определенного сервера"""
    assert isinstance(type_of_server_to_write, str), "variable 'type_of_server_to_write' is not str"
    #####
    dict_results_on_server = load_dict_with_results_from_server(type_of_server_to_write, is_to_get_only_overall_result=False)
    dict_results_on_server[type_of_value_to_set] = value_to_set
    save_dict_with_results_to_server(dict_results_on_server, type_of_server_to_write)
    return 1
