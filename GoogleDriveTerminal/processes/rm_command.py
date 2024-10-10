from googleapiclient.errors import HttpError

from data.constants import SERVICE
from work_with_state.dir_content_writter import set_cur_dir_content, get_list_content


# удаление файла (если он создан сервисным аккаунтом)
def remove_service_file(file_name: str) -> str:
    # все файлы и папки в текущем каталоге
    cur_content = get_list_content()

    # юзер ввёл неверную директорию
    if file_name not in map(lambda sublist: sublist[1], cur_content):
        return 'ERROR: such file not found!'
    elif list(filter(lambda sublist: sublist[1] == file_name, cur_content))[0][0] == 'dir':
        return 'ERROR: cannot remove dir!'
    else:
        # id файла, который нужно удалить
        file_id_to_delete = list(filter(lambda sublist: sublist[1] == file_name, cur_content))[0][-1]

    try:
        # Выполнение запроса на удаление файла
        SERVICE.files().delete(fileId=file_id_to_delete).execute()
    except HttpError:
        return f'ERROR: cannot remove "{file_name}", permission denied!'

    print(f'\033[32mFile "{file_name}" was deleted\033[0m')
    # обновляем список содержимого текущей папки
    cur_content.remove(['file', file_name, file_id_to_delete])
    set_cur_dir_content(content=cur_content)
    return f'OK: rm {file_name}'
