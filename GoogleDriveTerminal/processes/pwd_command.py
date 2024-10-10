from work_with_state.current_dir_writter import get_cur_dir


# вывод полного пути текущего каталога
def show_cur_dir_path() -> str:
    dir_path = get_cur_dir()

    return dir_path
