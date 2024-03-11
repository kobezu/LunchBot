import os

#return path to file in files folder
def path_to_file(file_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), '..', 'files', file_name)

LOG_FP = path_to_file('bot.log')
USERS_FP = path_to_file('users.json')
TOKEN_FP = path_to_file('token.txt')
ADMINS_FP = path_to_file('admins.txt')
LOTTERY_FP = path_to_file('lottery.json')

#return message text as string from given file
def message_txt(file_name: str, language_fin: bool) -> str:
    folder_name = 'FIN' if language_fin else 'ENG'
    file = open(path_to_file(os.path.join(path_to_file('message_txt'), folder_name, file_name)), encoding="utf-8")
    lines = [line.strip().replace('\\n', '\n') for line in file]
    return ' '.join(lines)