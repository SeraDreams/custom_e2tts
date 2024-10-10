from os import system


# команда системы
def system_command_exec(command: str) -> str:
    system(command)
    return 'BASH: command was executed'
