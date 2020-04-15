import sys, os
from all_CONSTANTS import *
#####
from working_with_files import save_dict_to_txt_file
from working_with_files import load_dict_from_txt_file
from scripts_USEFULL_EVERYWHERE import check_with_assert_that_type_is_correct





dict_types_transform = {}
dict_types_transform[""] = "times_alpha_used_in_combinations"
# dict_types_transform["None"] = "times_alpha_used_in_combinations"
# dict_types_transform["any"] = "times_alpha_used_in_combinations"
dict_types_transform["quantile"] = "times_alpha_used_in_combinations_with_quantiles"
dict_types_transform["one_side_quantiles"] = "times_alpha_used_in_combinations_with_one_side_quantiles"
dict_types_transform["rank_with_power"] = "times_alpha_used_in_combinations_with_rank_with_power"
dict_types_transform["minirank"] = "times_alpha_used_in_combinations_with_minirank"
dict_types_transform["developed"] = "times_alpha_developed"


def read_number_how_many_times_alpha_used_in_combinations(
        str_path_to_sabalpha,
        str_type_of_combination="overall",
        str_which_quality_alphas_to_work_with="",
        bool_is_alpha_used_in_MEGA_alpha=False
):
    """Функции для работы с числом сколько раз альфа (из my_myalphas) была использованна в комбинациях"""
    check_with_assert_that_type_is_correct(str_path_to_sabalpha, str)
    check_with_assert_that_type_is_correct(str_type_of_combination, str)
    check_with_assert_that_type_is_correct(str_which_quality_alphas_to_work_with, str)
    check_with_assert_that_type_is_correct(bool_is_alpha_used_in_MEGA_alpha, bool)
    #####
    path_to_file_with_dict_submission_results = str_path_to_sabalpha + "dict_all_submission_in_combinations_results.txt"
    if not os.path.exists(path_to_file_with_dict_submission_results):
        return 0
    dict_with_submission_results = load_dict_from_txt_file(path_to_file_with_dict_submission_results)
    if str_type_of_combination == "overall":
        int_overall_times_alpha_were_submitted = sum([int(dict_with_submission_results[str_key_type]) for str_key_type in dict_with_submission_results])
        return int_overall_times_alpha_were_submitted
    else:
        type_of_combination_mod = dict_types_transform[str_type_of_combination]
        if str_which_quality_alphas_to_work_with:
            type_of_combination_mod += "_" + str_which_quality_alphas_to_work_with.upper() + "_alphas_only"
        if bool_is_alpha_used_in_MEGA_alpha:
            type_of_combination_mod += "_MEGA"
        if type_of_combination_mod not in dict_with_submission_results:
            return 0
        return int(dict_with_submission_results[type_of_combination_mod])


def save_number_how_many_times_alpha_used_in_combinations(
        str_path_to_sabalpha,
        int_number_of_times_alpha_used_in_combinations,
        str_type_of_combination,
        str_which_quality_alphas_to_work_with="",
        bool_is_alpha_used_in_MEGA_alpha=False
):
    """Функция сохраняет в файл сколько альф засабмичено сегодня"""
    check_with_assert_that_type_is_correct(str_path_to_sabalpha, str)
    check_with_assert_that_type_is_correct(int_number_of_times_alpha_used_in_combinations, int)
    check_with_assert_that_type_is_correct(str_type_of_combination, str)
    check_with_assert_that_type_is_correct(str_which_quality_alphas_to_work_with, str)
    check_with_assert_that_type_is_correct(bool_is_alpha_used_in_MEGA_alpha, bool)
    #####
    path_to_file_with_dict_submission_results = str_path_to_sabalpha + "dict_all_submission_in_combinations_results.txt"
    # Если файла со словарем еще нет то испольльзуем пустой словарь
    if not os.path.exists(path_to_file_with_dict_submission_results):
        dict_with_submission_results = {}
    else:
        dict_with_submission_results = load_dict_from_txt_file(path_to_file_with_dict_submission_results)
    type_of_combination_mod = dict_types_transform[str_type_of_combination]
    if str_which_quality_alphas_to_work_with:
        type_of_combination_mod += "_" + str_which_quality_alphas_to_work_with.upper() + "_alphas_only"
    if bool_is_alpha_used_in_MEGA_alpha:
        type_of_combination_mod += "_MEGA"
    dict_with_submission_results[type_of_combination_mod] = int_number_of_times_alpha_used_in_combinations
    save_dict_to_txt_file(dict_with_submission_results, path_to_file=path_to_file_with_dict_submission_results)
    return 1


def increase_by_N_how_many_times_alpha_used_in_combinations(
        str_path_to_sabalpha,
        int_number_of_new_usage_in_combinations,
        str_type_of_combination="",
        str_which_quality_alphas_to_work_with="",
        bool_is_alpha_used_in_MEGA_alpha=False
):
    """Функция для увеличения числа засабмиченных альф на 1"""
    check_with_assert_that_type_is_correct(str_path_to_sabalpha, str)
    check_with_assert_that_type_is_correct(int_number_of_new_usage_in_combinations, int)
    check_with_assert_that_type_is_correct(str_type_of_combination, str)
    check_with_assert_that_type_is_correct(str_which_quality_alphas_to_work_with, str)
    check_with_assert_that_type_is_correct(bool_is_alpha_used_in_MEGA_alpha, bool)
    #####
    int_times_already_submitted = read_number_how_many_times_alpha_used_in_combinations(
        str_path_to_sabalpha=str_path_to_sabalpha,
        str_type_of_combination=str_type_of_combination,
        str_which_quality_alphas_to_work_with=str_which_quality_alphas_to_work_with,
        bool_is_alpha_used_in_MEGA_alpha=bool_is_alpha_used_in_MEGA_alpha
    )
    save_number_how_many_times_alpha_used_in_combinations(
        str_path_to_sabalpha=str_path_to_sabalpha,
        int_number_of_times_alpha_used_in_combinations=int_times_already_submitted + int_number_of_new_usage_in_combinations,
        str_type_of_combination=str_type_of_combination,
        str_which_quality_alphas_to_work_with=str_which_quality_alphas_to_work_with,
        bool_is_alpha_used_in_MEGA_alpha=bool_is_alpha_used_in_MEGA_alpha
    )
    return 1

