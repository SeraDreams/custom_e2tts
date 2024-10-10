#!/home/danil/anaconda3/envs/stable/bin/python

import readline

from work_with_state.current_dir_writter import get_cur_dir
from processes import cd_command, process_manager


def main() -> None:
    # Отключение обработки управляющих символов (для корректной работы стрелок клавиатуры в терминале)
    readline.parse_and_bind("")

    # по дефолту переходим в корень диска
    cd_command.move_to_root()

    while True:
        try:
            # считывание введённой команды
            command = input(f'drive{":" + get_cur_dir()}> ').strip()
        # выход из программы
        except KeyboardInterrupt:
            print('\n\033[31mGoodbye!\033[0m')
            break

        # выход из программы
        if command == 'exit' or command == 'quit':
            print('\033[31mGoodbye!\033[0m')
            break

        # если в строке несколько команд (указаны через "&&"), то они выполнятся по отдельности
        # если команда одна (нет знака "&&"), то она просто выполнится
        for subcommand in command.split('&&'):
            # обработка команды и получение ответа выполнения
            feedback = process_manager.process_manage(command=subcommand)

            # печатаем только ошибки
            if feedback.startswith('ERROR') or feedback.startswith('FATAL'):
                print(f'\033[31m{feedback}\033[0m')


if __name__ == '__main__':
    main()
