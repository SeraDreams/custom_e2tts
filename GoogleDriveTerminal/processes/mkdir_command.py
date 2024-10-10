from custom_e2tts.GoogleDriveTerminal.data.constants import SERVICE
from custom_e2tts.GoogleDriveTerminal.work_with_state.dir_content_writter import set_cur_dir_content, get_list_content
from custom_e2tts.GoogleDriveTerminal.work_with_state.id_cur_dir_writter import get_cur_dir_id


# создание пустой директории на диске
def make_new_dir(new_dir_name: str) -> str:
    # id родительской папки
    parent_dir_id = get_cur_dir_id()
    # все файлы и папки в текущем каталоге
    cur_content = get_list_content()

    # запрет создавать папку в корне
    if not parent_dir_id:
        return 'ERROR: cannot make dir in "root"'

    # юзер ввёл существующую директорию
    if new_dir_name in map(lambda sublist: sublist[1], cur_content):
        action = input('\033[33mWARNING: such dir already exist! Continue OR rename it and enter this command again. Continue? [y, n] \033[0m')
        if action != 'y':
            print('Command was canceled!')
            return 'OK: cancel command'
        else:
            print('Continue...')

    folder_metadata = {
        'name': new_dir_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_dir_id]
    }
    new_dir = SERVICE.files().create(body=folder_metadata, fields='id').execute()

    # обновляем список содержимого текущей папки
    cur_content.append(['dir', new_dir_name, new_dir.get("id")])
    set_cur_dir_content(content=cur_content)
    return f'OK: mkdir {new_dir_name}'
