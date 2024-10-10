from custom_e2tts.GoogleDriveTerminal.data.constants import BASE_DIR


# запись текущей директории
def set_cur_dir(directory: str) -> None:
    with open(f'{BASE_DIR}/state/current_dir', 'w') as file_cur_dir:
        file_cur_dir.write(directory)


# получение текущей директории
def get_cur_dir() -> str:
    with open(f'{BASE_DIR}/state/current_dir', 'r') as file_cur_dir:
        cur_dir = file_cur_dir.read()
    return cur_dir
