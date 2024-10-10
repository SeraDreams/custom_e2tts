from data.constants import SERVICE, ROOT_CONTENT
from work_with_state.current_dir_writter import set_cur_dir, get_cur_dir
from work_with_state.dir_content_writter import set_cur_dir_content, get_list_content
from work_with_state.recent_dir_id_writter import set_id_recent_dirs, get_id_recent_dir
from work_with_state.id_cur_dir_writter import set_cur_dir_id


# переход в корень диска
def move_to_root() -> str:
    set_id_recent_dirs(dir_id='', clear=True)
    set_cur_dir(directory='/')
    set_cur_dir_id(dir_id='')
    set_cur_dir_content(content=ROOT_CONTENT)

    return 'OK: cd /'


# переход в другую папку на диске
def move_to_dir(dir_name: str) -> str:
    # путь к прошлой папке
    recent_dir = get_cur_dir()
    # все файлы и папки в текущем каталоге
    cur_content = get_list_content()

    # юзер ввёл неверную директорию
    if dir_name not in map(lambda sublist: sublist[1], cur_content):
        return 'ERROR: such dir not found!'
    elif list(filter(lambda sublist: sublist[1] == dir_name, cur_content))[0][0] == 'file':
        return 'ERROR: cannot go to file!'
    else:
        # ID папки, из которой нужно получить файлы
        folder_id = list(filter(lambda sublist: sublist[1] == dir_name, cur_content))[0][-1]

    dir_files = SERVICE.files().list(q=f"'{folder_id}' in parents", fields="files(id, name, mimeType)").execute()
    dir_content = [
        (
            'dir' if file.get('mimeType') == 'application/vnd.google-apps.folder' else 'file',
            file.get('name'),
            file.get('id'),
        )
        for file in dir_files.get('files')
    ]

    # новый путь к текущей директории
    new_dir = (recent_dir if recent_dir != '/' else '') + '/' + dir_name

    # id родительской папки
    id_parent = SERVICE.files().get(fileId=folder_id, fields='parents').execute().get('parents', [''])[0]

    set_id_recent_dirs(dir_id=id_parent)
    set_cur_dir(directory=new_dir)
    set_cur_dir_id(dir_id=folder_id)
    set_cur_dir_content(content=dir_content)

    return f'OK: cd {new_dir}'


# переход в каталог на уровень ниже (cd ..)
def move_one_step_down() -> str:
    # путь к текущей папке
    recent_dir_path = get_cur_dir()

    # id прошлой папки
    try:
        recent_dir_id = get_id_recent_dir()
    # если в корне ввести команду "cd .."
    except IndexError:
        return 'WARNING: cannot go down (you are in "root")'

    # если id прошлой папки нет, то идём в корень
    if not recent_dir_id:
        move_to_root()
        return 'OK: cd ..'

    dir_files = SERVICE.files().list(q=f"'{recent_dir_id}' in parents", fields="files(id, name, mimeType)").execute()
    dir_content = [
        (
            'dir' if file.get('mimeType') == 'application/vnd.google-apps.folder' else 'file',
            file.get('name'),
            file.get('id'),
        )
        for file in dir_files.get('files')
    ]

    # новый путь к текущей директории
    new_dir = recent_dir_path[:recent_dir_path.rfind('/')]

    set_cur_dir(directory=new_dir)
    set_cur_dir_id(dir_id=recent_dir_id)
    set_cur_dir_content(content=dir_content)
    return 'OK: cd ..'


# главная функция cd, распределяющая множественные перемещения
def main_cd(need_dir: str) -> str:
    # разбиваем данный путь на части (убираем из пути точку, если она есть)
    path_to_need_dir = list(filter(lambda elem: elem != '.', need_dir.split('/')))

    # print(path_to_need_dir)

    if need_dir == '/':
        # идём в рута
        feedback = move_to_root()

    else:
        for part_path in path_to_need_dir:
            if part_path == '':
                # идём в рута
                one_feedback = move_to_root()
            elif part_path == '..':
                # идём на уровень ниже
                one_feedback = move_one_step_down()
            else:
                # идём в следующий указанный каталог
                one_feedback = move_to_dir(dir_name=part_path)

            if one_feedback.startswith('ERROR'):
                feedback = f'ERROR: invalid path part "{part_path}" of path "{need_dir}"'
                break
        else:
            feedback = f'OK: cd {need_dir}'

    return feedback
