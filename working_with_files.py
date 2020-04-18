import os
import logging

def read_whole_file(str_path_to_file):
    """Reading whole file as string in utf-8"""
    with open(str_path_to_file, 'r', encoding="utf8", errors='ignore') as f:
        str_whole_file = f.read()
    return str_whole_file


def save_whole_file(str_path_to_file, str_what_to_write, str_write_mode='w'):
    """Saving whole file"""
    with open(
            str_path_to_file,
            str_write_mode,
            encoding="utf8",
            errors='ignore'
    ) as file_stream:
        file_stream.write(str_what_to_write)
    return 1


def check_that_folder_exist_otherwise_create(str_path_to_folder):
    """Check if folder exists if not then create it"""
    if (not os.path.isdir(str_path_to_folder)):
        os.makedirs(str_path_to_folder)
        return 1
    return 0


def get_list_names_of_folders_in_folder(str_path_where_to_look):
    """Get names of all folders in the folder"""
    if os.path.exists(str_path_where_to_look):
        list_alphas_folders = [
            f.path
            for f in os.scandir(str_path_where_to_look)
            if f.is_dir()
        ]
    else:
        list_alphas_folders = []
    return list_alphas_folders


def get_list_of_fields_in_file(str_path_to_file):
    """
    """
    # Check that file exists
    if(not os.path.exists(str_path_to_file)):
        return []
    list_of_fields = []
    str_whole_file = read_whole_file(str_path_to_file)
    # Delete empty lines
    list_file_splitted_by_lines = [
        str_one_line
        for str_one_line in str_whole_file.splitlines()
        if str_one_line
    ]
    for line in list_file_splitted_by_lines:
        list_of_fields += [elem for elem in line.split(" ") if elem]
    return list_of_fields


def save_list_of_fields_in_file(
        list_of_fields,
        str_path_to_file,
        endl="\n",
):
    """Функция Сохраняем в файл список полей"""
    str_whole_file_to_save = ""
    for elem in list_of_fields:
        str_whole_file_to_save += str(elem) + endl
    save_whole_file(str_path_to_file, str_whole_file_to_save)
    return 1

