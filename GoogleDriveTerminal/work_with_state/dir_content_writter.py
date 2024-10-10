from custom_e2tts.GoogleDriveTerminal.data.constants import BASE_DIR


# запись содержимого текущей директории
def set_cur_dir_content(content: list) -> None:
    with open(f'{BASE_DIR}/state/dir_content', 'w') as content_cur_dir:
        for elem in content:
            content_cur_dir.write(elem[0] + ' -- ')
            content_cur_dir.write(elem[1] + ' -- ')
            content_cur_dir.write(elem[2] + '\n')


# получение содержимого текущей директории (список со списками)
def get_list_content() -> list:
    with open(f'{BASE_DIR}/state/dir_content', 'r') as content_cur_dir:
        row_dir_content = content_cur_dir.readlines()
    clear_content = [elem.replace('\n', '').split(' -- ') for elem in row_dir_content]
    return clear_content
