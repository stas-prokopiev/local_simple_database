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
    if not os.path.exists(str_path_where_to_look):
        logging.warning(
            "Folder to get dir names inside doesn't exist: " +
            str_path_where_to_look
        )
        return []
    list_alphas_folders = [
        os.path.basename(f.path)
        for f in os.scandir(str_path_where_to_look)
        if f.is_dir()
    ]
    return list_alphas_folders


def get_names_of_files_in_the_folder(
        str_folder_where_to_look="",
        str_extension=".txt"
):
    """Get names of all files in folder with asked extension"""
    assert isinstance(str_folder_where_to_look, str), (
        "ERROR: path to folder where to look for files should have type STR" +
        ", Now it has type: " +
        str(type(str_folder_where_to_look))
    )
    if not os.path.exists(str_folder_where_to_look):
        logging.warning(
            "Folder to get filenames doesn't exist: " +
            str_folder_where_to_look
        )
        return []
    #####
    list_all_filenames_in_the_folder = [
        str_filename
        for str_filename in os.listdir(str_folder_where_to_look)
        if os.path.isfile(os.path.join(str_folder_where_to_look, str_filename))
    ]
    if str_extension:
        list_all_filenames_in_the_folder = [
            str_filename
            for str_filename in list_all_filenames_in_the_folder
            if str_filename.endswith(str_extension)
        ]
    return list_all_filenames_in_the_folder


