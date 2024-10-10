from data.constants import SERVICE
from work_with_state.current_dir_writter import get_cur_dir
from work_with_state.dir_content_writter import set_cur_dir_content, get_list_content
from work_with_state.id_cur_dir_writter import get_cur_dir_id


# вывод содержимого текущего каталога
def show_cur_dir_content() -> str:
    # список с папками и файлами
    list_content = get_list_content()

    # кол-во файлов и папок в данной директории
    num_dir = num_file = 0

    # преобразуем контент в строку
    str_content = ''
    for elem in list_content:
        str_content += '\n' + elem[0] + ' -- \033[34m' + elem[1] + '\033[0m'
        # подсчёт кол-ва папок и файлов
        if elem[0] == 'dir':
            num_dir += 1
        else:
            num_file += 1

    # объединяем основной контент с кол-вом элементов
    cool_table = f'All: {num_dir + num_file} || Dirs: {num_dir} || Files: {num_file}' + str_content

    return cool_table


# повторное считывание контента текущего каталога
def update_content_info() -> None:
    # id текущей папки
    folder_id = get_cur_dir_id()
    # путь к текущей папке
    dir_name = get_cur_dir()

    dir_files = SERVICE.files().list(q=f"'{folder_id}' in parents", fields="files(id, name, mimeType)").execute()
    dir_content = [
        (
            'dir' if file.get('mimeType') == 'application/vnd.google-apps.folder' else 'file',
            file.get('name'),
            file.get('id'),
        )
        for file in dir_files.get('files')
    ]

    set_cur_dir_content(content=dir_content)
    print(f'''\033[32m"{dir_name}" content was updated\033[0m''')
