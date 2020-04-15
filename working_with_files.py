import os




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
