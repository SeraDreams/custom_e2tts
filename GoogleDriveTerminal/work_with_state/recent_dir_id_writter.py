from custom_e2tts.GoogleDriveTerminal.data.constants import BASE_DIR


# запись id последней директории (не учитывая текущую)
def set_id_recent_dirs(dir_id: str, clear: bool = False) -> None:
    if clear:
        with open(f'{BASE_DIR}/state/recent_dirs_id', 'w') as file_recent_dir:
            file_recent_dir.write(dir_id)
        return

    with open(f'{BASE_DIR}/state/recent_dirs_id', 'a') as file_recent_dir:
        file_recent_dir.write(dir_id + '\n')


# получение id последней директории (не учитывая текущую) и перезапись файла с последними директориями
def get_id_recent_dir() -> str:
    with open(f'{BASE_DIR}/state/recent_dirs_id', 'r') as file_recent_dir:
        id_dirs = file_recent_dir.readlines()

    last_dir = id_dirs[-1].replace('\n', '')
    with open(f'{BASE_DIR}/state/recent_dirs_id', 'w') as file_recent_dir:
        file_recent_dir.write(''.join(id_dirs[:-1]))
    return last_dir
