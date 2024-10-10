from re import sub as re_sub, findall as re_findall

from work_with_state.current_dir_writter import get_cur_dir
from work_with_state.history_writter import get_history, add_history
from processes import (cd_command, ls_command, pwd_command,
                       mkdir_command, rename_command, rm_command,
                       system_interaction, help_command,
                       get_command, put_command)


def process_help(command: str) -> str:
    content = help_command.show_help_manual()
    print(content)

    return f'OK: {command}'


def process_sys(command: str) -> str:
    sys_com = command[1:]
    system_interaction.system_command_exec(command=sys_com)
    result = f'OK: system command "{command}"'

    return result


def process_cd(command: str) -> str:
    # требуемая директория
    need_dir = re_sub('\s', ' ', command[2:]).strip()
    # перемещение
    result = cd_command.main_cd(need_dir=need_dir)

    return result


def process_ls(command: str) -> str:
    filelist = ls_command.show_cur_dir_content()
    print(filelist)
    result = f'OK: {command}'

    return result


def process_pwd(command: str) -> str:
    dir_path = pwd_command.show_cur_dir_path()
    print(dir_path)
    result = f'OK: {command}'

    return result


def process_mkdir(command: str) -> str:
    # неподдерживаемые символы
    except_symbols = '[\/:*\\\<>+|\'\"?,]'

    name_new_dir = re_sub('\s', ' ', command[5:]).strip()
    if re_findall(except_symbols, name_new_dir):
        result = 'ERROR: your dirname contain unsupported symbols!'
    else:
        result = mkdir_command.make_new_dir(name_new_dir)

    return result


def process_rename(command: str) -> str:
    # неподдерживаемые символы
    except_symbols = '[\/:*\\\<>+|\'\"?,]'

    # извлекаем из команды старое и новое имя для директории
    names_list = re_sub('\s', ' ', command[6:]).split(' ./')[1:]

    if len(names_list) == 2:
        old_name = names_list[0].strip()
        new_name = names_list[1].strip()

        # если новое имя содержит неподдерживаемые символы
        if re_findall(except_symbols, new_name):
            result = 'ERROR: your new dirname contain unsupported symbols!'
        else:
            result = rename_command.rename_file(old_name=old_name, new_name=new_name)
    else:
        result = 'ERROR: invalid names count!'

    return result


def process_get(command: str) -> str:
    clear_command = re_sub('\s|(\./)', ' ', command[3:]).strip()

    result = get_command.main_get(clear_command=clear_command)

    return result


def process_put(command: str) -> str:
    clear_command = re_sub('\s', ' ', command[3:]).strip()

    result = put_command.main_put(clear_command=clear_command)

    if clear_command.startswith('-r') and result != 'OK: cancel command':
        print('Update current dir info...')
        ls_command.update_content_info()

    return result


def process_r(command: str) -> str:
    cur_dir = get_cur_dir()
    # если обновление происходит в корне
    if cur_dir == '/':
        return "ERROR: you haven't to update root dir, it's stable!"

    ls_command.update_content_info()
    return f"OK: {command}"


def process_rm(command: str) -> str:
    file_name = re_sub('\s|(\./)', ' ', command[2:]).strip()

    result = rm_command.remove_service_file(file_name=file_name)
    return result


def process_history(command: str) -> str:
    try:
        num = int(command.replace('history', '').strip())
    except ValueError:
        num = ''

    all_his = [f' {iter_num}  {elem}' for iter_num, elem in enumerate(get_history(), 0)]
    if not num:
        history = '\n'.join(all_his)
    else:
        history = '\n'.join(all_his[-num:])

    print(history)
    return f'OK: {command}'


# обработка команд и распределение задач
def process_manage(command: str) -> str:
    # словарь с доступными командами
    command_dir = {
        'help': process_help,
        '!': process_sys,
        'cd': process_cd,
        'ls': process_ls,
        'pwd': process_pwd,
        'mkdir': process_mkdir,
        'rename': process_rename,
        'get': process_get,
        'put': process_put,
        'r': process_r,
        'rm': process_rm,
        'history': process_history,
    }

    try:
        # название вызываемой команды
        command_word = ('!' if command.startswith('!') else command.split()[0].strip())
    # нажатый Enter
    except IndexError:
        return 'OK: Enter'

    # выполнение команды
    try:
        feedback = command_dir[command_word](command=command.strip())
    # если команды нет в словаре
    except KeyError:
        feedback = 'ERROR: invalid command!'
    except Exception as error:
        return f'FATAL!!!\nWhile processing command "{command}" you got error:\n{error}'

    # добавляем команду в историю
    add_history(command=command)

    return feedback
