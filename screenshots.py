import sys, os
from all_CONSTANTS import *


from working_with_files import check_that_folder_exist_otherwise_create
from working_with_files import winapi_path
from working_with_files import get_max_number_of_filename_in_given_folder
from time import sleep
from working_with_telegram import send_message_to_my_telegram_bot

from scripts_USEFULL_EVERYWHERE import check_with_assert_that_type_is_correct


def read_number_of_screenshots_created():
    """Считываем из файла число уже сделанных скриншотов, чтобы создать уникальные скриншоты"""
    check_that_folder_exist_otherwise_create("screens/")
    file_name = "screens/overall_screenshots_made.txt"
    # Проверяем что файл уже создан сегодня и там есть хоть что-то, иначе создаем
    if not os.path.isfile(winapi_path(file_name)):
        save_number_of_screenshots_made(0)
        return 0
    with open(winapi_path(file_name), 'r') as f:
        content = f.read()
        # Проверяем, что возвращаем число, а не что-то другое
        if content.isdigit():
            return int(content)
        else:
            print("Can't find  max number of screenshots!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("content of file with number is: ", content)
            return get_max_number_of_filename_in_given_folder("screens/")


def save_number_of_screenshots_made(int_number_of_screenshots):
    """Функция сохраняет в файл число скриншотов"""
    check_with_assert_that_type_is_correct(int_number_of_screenshots, int)
    #####
    check_that_folder_exist_otherwise_create("screens/")
    file_name = "screens/overall_screenshots_made.txt"
    with open(winapi_path(file_name), 'w') as f:
        f.write(str(int_number_of_screenshots))
    return 1


def increase_by_1_number_of_screenshots():
    """Функция для увеличения числа скриншотов на 1"""
    # file_name = "screens/overall_screenshots_made.txt"
    already_done_screenshots = read_number_of_screenshots_created()
    save_number_of_screenshots_made(already_done_screenshots + 1)
    return 1


def remove_old_screenshots_if_there_are_too_much():
    """Функция для удаления старых скриншотов, когда их становится слишком много"""
    number_of_screens_to_delete_them = 50
    how_many_screens_to_delete_per_step = 30
    # Получаем имена всех скриншотов в папке
    # get_list_of_files_in_folder(folder_where_to_look = "screens/", extension = ".png")
    list_all_screenshot_names = [f for f in os.listdir(winapi_path("screens/")) if "png" in f]
    # Если не набралось еще достаточно, то выходим
    if len(list_all_screenshot_names) < number_of_screens_to_delete_them:
        return 1
    # Переводим все имена файлов в словарь (номерь: имя_скриншота)
    dict_screenshot_name_by_number = {}
    for screenshot_name in list_all_screenshot_names:
        screenshot_number = int(screenshot_name.split(")")[0])
        dict_screenshot_name_by_number[screenshot_number] = screenshot_name
    # Получаем список всех доступных номеров скриншотов
    list_of_sorted_screenshot_numbers = sorted(list(dict_screenshot_name_by_number.keys()))
    # Удаляем старые скриншоты
    for screenshot_number in list_of_sorted_screenshot_numbers[:how_many_screens_to_delete_per_step]:
        full_path = "screens/" + dict_screenshot_name_by_number[screenshot_number]
        os.remove(winapi_path(full_path))
    print("Were removed: ", how_many_screens_to_delete_per_step, " screenshots")
    return 1


def full_proccess_of_creating_new_screenshot(webdriver, str_decription_of_screenshot):
    """Весь процесс создания нового скриншота"""
    check_with_assert_that_type_is_correct(str_decription_of_screenshot, str)
    #####

    print("\n" + "ERROR: " + str_decription_of_screenshot)
    # Обрабатываем переданную строку ошибки
    "You have reached the limit of concurrent Check Submission/Submit Alpha. Please wait for the previous to finish."
    # str_decription_of_screenshot = str_decription_of_screenshot.lower() # Переводим в нижний регистр
    str_decription_of_screenshot = str_decription_of_screenshot.replace(" ", "_")  # Заменяем пробелы на знак подчеркивания
    str_decription_of_screenshot = str_decription_of_screenshot.replace("'", "")  # Заменяем символ ' (в can't например) на пустоту
    str_decription_of_screenshot = str_decription_of_screenshot.replace(":", "")  # Заменяем символ: (number: ) на пустоту
    str_decription_of_screenshot = str_decription_of_screenshot.replace(",", "")  # Заменяем символ: (number: ) на пустоту
    str_decription_of_screenshot = str_decription_of_screenshot.replace(".", "")  # Заменяем символ: (number: ) на пустоту
    str_decription_of_screenshot = str_decription_of_screenshot.replace("/", "_")  # Заменяем символ '/': на пустоту
    #####
    # Если имя слишком длинное то оставляем только первые 50 символов
    if len(str_decription_of_screenshot) > 70:
        str_decription_of_screenshot = str_decription_of_screenshot[:70]
    # Создаем путь до файла, куда положим скриншот
    number_of_screenshots_already_made = read_number_of_screenshots_created()
    path_to_new_screenshot = "screens/" + str(number_of_screenshots_already_made) + ")" + str_decription_of_screenshot + ".png"
    print("SCREENSHOT CREATED: ", number_of_screenshots_already_made, "    with path: ", path_to_new_screenshot)
    # Пытаемся сделать скриншот
    int_max_number_of_itterations_to_try_to_create_screenshot = 10
    int_current_itteration_number = 0
    bool_screenshot_was_created = False
    while int_current_itteration_number < int_max_number_of_itterations_to_try_to_create_screenshot:
        int_current_itteration_number += 1
        try:
            webdriver.get_screenshot_as_file(path_to_new_screenshot)  # Сохраняем скриншот происходяшего
            bool_screenshot_was_created = True
            break
        except TimeoutException:
            print("WARNING: Unable to create screenshot, waiting and trying once again", flush=True)
            print("str_decription_of_screenshot: ", str_decription_of_screenshot)
            try:
                webdriver.refresh()
            except TimeoutException:
                pass
            sleep(30)
    # Если скриншот не был создан даже после большего числа иттераций, то отправляем об этом сообщение в телеграм
    if not bool_screenshot_was_created:
        str_message_to_send = (
            "ERROR: unable to create screenshot even after: " +
            str(int_max_number_of_itterations_to_try_to_create_screenshot) +
            " itterations"
        )
        send_message_to_my_telegram_bot(str_message_to_send, type_of_bot="urgent_messages_bot")
        sys.exit(2352)
    increase_by_1_number_of_screenshots()
    # Удаляем старые скриншоты, если накопилось слишком много
    remove_old_screenshots_if_there_are_too_much()
    return 1




