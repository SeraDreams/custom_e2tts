from custom_e2tts.GoogleDriveTerminal.data.constants import BASE_DIR


# запись id текущей директории
def set_cur_dir_id(dir_id: str) -> None:
    with open(f'{BASE_DIR}/state/id_cur_dir', 'w') as file_cur_dir_id:
        file_cur_dir_id.write(dir_id)


# получение id текущей директории
def get_cur_dir_id() -> str:
    with open(f'{BASE_DIR}/state/id_cur_dir', 'r') as file_cur_dir_id:
        cur_dir_id = file_cur_dir_id.read()
    return cur_dir_id
