from os import listdir
from os.path import abspath, isfile, isdir, exists

from googleapiclient.http import MediaFileUpload

from custom_e2tts.GoogleDriveTerminal.data.constants import SERVICE
from custom_e2tts.GoogleDriveTerminal.work_with_state.id_cur_dir_writter import get_cur_dir_id
from custom_e2tts.GoogleDriveTerminal.work_with_state.dir_content_writter import get_list_content, set_cur_dir_content


def upload_file(file_name: str, path: str) -> str:
    # id родительской директории
    parent_dir_id = get_cur_dir_id()
    # контент текущей директории
    cur_content = get_list_content()

    # юзер пытается загрузить файл с именем, которое уже есть у другого файла на диске
    if file_name in map(lambda sublist: sublist[1], cur_content):
        action = input('\033[33mWARNING: such file already exist! Continue OR rename it and enter this command again. Continue? [y, n] \033[0m')
        if action != 'y':
            print('Command was canceled!')
            return 'OK: cancel command'
        else:
            print('Continue...')

    # вывод начала загрузки
    print(f'Uploading "{file_name}"')

    file_metadata = {
        'name': file_name,
        'parents': [parent_dir_id]
    }
    media = MediaFileUpload(path, resumable=True)
    new_file = SERVICE.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # обновляем список содержимого текущей папки
    cur_content.append(['file', file_name, new_file.get("id")])
    set_cur_dir_content(content=cur_content)

    # вывод успеха
    print('\033[32mSuccessfully\033[0m')
    return f'OK: file "{file_name}" was uploaded'


def upload_file_custom_parent(file_name: str, path: str, parent_dir_id: str) -> None:
    # вывод начала загрузки
    print(f'Uploading "{file_name}"', end='')

    file_metadata = {
        'name': file_name,
        'parents': [parent_dir_id]
    }
    media = MediaFileUpload(path, resumable=True)
    SERVICE.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # вывод успеха
    print('\033[32m: successfully\033[0m')


def upload_dir(dir_name: str, path: str, parent_id: str = get_cur_dir_id()) -> None:
    # контент текущей директории
    cur_content = get_list_content()

    # юзер пытается загрузить директорию с именем, которое уже есть у другой директории на диске
    if dir_name in map(lambda sublist: sublist[1], cur_content):
        action = input('\033[33mWARNING: such dir already exist! Continue OR rename it and enter this command again. Continue? [y, n] \033[0m')
        if action != 'y':
            print('Command was canceled!')
            return 'OK: cancel command'
        else:
            print('Continue...')

    # создание новой директории в Google Drive для дальнейшего копирования файлов туда
    folder_metadata = {
        'name': dir_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    new_dir = SERVICE.files().create(body=folder_metadata, fields='id').execute()
    new_dir_id = new_dir.get("id")

    # обход файлов каталога
    for file in listdir(path):
        path_to_elem = path + '/' + file

        # проверка на файл
        if isfile(path_to_elem):
            # загрузка
            upload_file_custom_parent(file_name=file, path=path_to_elem, parent_dir_id=new_dir_id)
        else:
            # загрузка следующей директории
            upload_dir(path=path_to_elem, dir_name=file, parent_id=new_dir_id)


def main_put(clear_command: str) -> str:
    # запрет загружать каталог в корень
    if not get_cur_dir_id():
        return 'ERROR: cannot upload dir/files in "root"'

    if clear_command.startswith('-r'):
        # полный путь с именем каталога
        path = abspath(clear_command[3:])

        # если такого каталога не существует
        if not exists(path):
            return 'ERROR: such file not exists!'

        # проверка на каталог
        if isdir(path):
            # извлечение имени директории из пути
            dir_name = path.split('/')[-1]
            # загрузка каталога
            print('START:')
            upload_dir(dir_name=dir_name, path=path)
            print(':FINISHED')
            result = f'OK: put {clear_command}'
        else:
            return 'ERROR: to upload file remove key "-r"'
    else:
        # требуемый файл
        need_file_with_path = clear_command
        # полный путь с именем файла
        path = abspath(need_file_with_path)

        # если такого файла не существует
        if not exists(path):
            return 'ERROR: such file not exists!'

        # проверка на файл
        if isfile(path):
            file_name = path.split('/')[-1]
            # загрузка файла
            result = upload_file(file_name=file_name, path=path)
        else:
            return 'ERROR: to upload dir add key "-r"'

    return result
