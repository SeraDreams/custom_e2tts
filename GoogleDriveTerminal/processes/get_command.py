import io
from os import getcwd, makedirs

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from custom_e2tts.GoogleDriveTerminal.data.constants import SERVICE
from custom_e2tts.GoogleDriveTerminal.work_with_state.dir_content_writter import get_list_content


def download_file(file_name: str) -> str:
    try:
        # все файлы и папки в текущем каталоге
        cur_content = get_list_content()

        # юзер ввёл неверный файл
        if file_name not in map(lambda sublist: sublist[1], cur_content):
            return 'ERROR: such file not found!'
        elif list(filter(lambda sublist: sublist[1] == file_name, cur_content))[0][0] == 'dir':
            return 'ERROR: to upload dir add key "-r"'
        else:
            # ID файла, который нужно скачать
            file_id = list(filter(lambda sublist: sublist[1] == file_name, cur_content))[0][-1]

        # вывод начала загрузки
        print(f'Downloading "{file_name}"')

        request = SERVICE.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        # загрузка байт в локальный файл
        with open(file_name, 'wb') as local_file:
            local_file.write(file.getvalue())

        # вывод успеха
        print('\033[32mSuccessfully\033[0m')
        return f'OK: file "{file_name}" was downloaded'

    # если нужно загрузить Google документ/таблицу/презентацию
    except HttpError:
        try:
            request = SERVICE.files().export_media(fileId=file_id, mimeType='application/pdf')

            # загрузка байт в локальный файл
            with open(f'{file_name}.pdf', 'wb') as local_file:
                downloader = MediaIoBaseDownload(local_file, request)

                done = False
                while not done:
                    status, done = downloader.next_chunk()

            # вывод успеха
            print('\033[32mSuccessfully\033[0m')
            return f'OK: file "{file_name}" was downloaded'
        except HttpError as error:
            return f'ERROR: you got HttpError while processing "get" command: {error}'


def download_file_custom_dir(file_id: str, file_name: str, need_local_dir: str) -> None:
    # вывод начала загрузки
    print(f'Downloading "{file_name}"', end='')

    request = SERVICE.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    # загрузка байт в локальный файл
    with open(f'{need_local_dir}/{file_name}', 'wb') as local_file:
        local_file.write(file.getvalue())

    # вывод успеха
    print('\033[32m: successfully\033[0m')


def download_dir(dir_name: str, path: str, content: list) -> None:
    # id папки, которую нужно скачать
    dir_id = list(filter(lambda sublist: sublist[1] == dir_name, content))[0][-1]

    dir_files = SERVICE.files().list(q=f"'{dir_id}' in parents", fields="files(id, name, mimeType)").execute()
    content = [
        (
            'dir' if file.get('mimeType') == 'application/vnd.google-apps.folder' else 'file',
            file.get('name'),
            file.get('id'),
        )
        for file in dir_files.get('files')
    ]

    for elem in content:
        if elem[0] == 'file':
            download_file_custom_dir(file_id=elem[-1], file_name=elem[1], need_local_dir=path)
        else:
            dir_name = elem[1]
            next_dir = path + '/' + dir_name

            # создание новой директории
            makedirs(name=next_dir, exist_ok=True)

            download_dir(dir_name=dir_name, path=next_dir, content=content)


def main_get(clear_command: str) -> str:
    if clear_command.startswith('-r'):
        # все файлы и папки в текущем каталоге
        cur_content = get_list_content()
        # имя нужной папки
        dir_name = clear_command[3:].strip()

        # юзер ввёл неверную директорию
        if dir_name not in map(lambda sublist: sublist[1], cur_content):
            return 'ERROR: such file not found!'
        elif list(filter(lambda sublist: sublist[1] == dir_name, cur_content))[0][0] == 'file':
            return 'ERROR: to upload file remove key "-r"'
        else:
            local_path = getcwd() + '/' + dir_name
            # создание новой директории
            makedirs(name=dir_name, exist_ok=True)
            # получение файлов с диска
            print('START:')
            download_dir(dir_name=dir_name, path=local_path, content=cur_content)
            print(':FINISHED')
            return f'OK: put {clear_command}'
    else:
        # требуемый файл
        need_file = clear_command
        # скачивание
        result = download_file(file_name=need_file)

    return result
