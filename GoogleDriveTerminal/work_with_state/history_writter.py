from custom_e2tts.GoogleDriveTerminal.data.constants import BASE_DIR


def get_history() -> list:
    with open(f'{BASE_DIR}/.drive_history', 'r') as history_file:
        all_history = [elem.replace('\n', '') for elem in history_file.readlines()]

    return all_history


def add_history(command: str) -> None:
    all_history = get_history()

    if len(all_history) < 50:
        with open(f'{BASE_DIR}/.drive_history', 'a') as history_file:
            history_file.write(f'{command}\n')
    else:
        all_history = all_history[1:]
        all_history.append(f'{command}')

        with open(f'{BASE_DIR}/.drive_history', 'w') as history_file:
            for command in all_history:
                history_file.write(f'{command}\n')
